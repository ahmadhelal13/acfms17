# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class medication(models.Model):
    _name = 'ksc.medication'

    name = fields.Char()


class medicationLines(models.Model):
    _name = 'line.medication'
    _description = 'Lines of medication'

    medication_name = fields.Many2one('ksc.medication')
    dosage = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], string='Dosage')
    hourly = fields.Selection(
        [('1', '1 H'), ('2', '2 H'), ('3', '3 H'), ('4', '4 H'), ('5', '5 H'), ('6', '6 H'), ('7', '7 H'), ('8', '8 H'),
         ('9', '9 H'),
         ('10', '10 H'), ('11', '11 H'), ('12', '12 H'), ('13',
                                                          '13 H'), ('14', '14 H'), ('15', '15 H'), ('16', '16 H'),
         ('17', '17 H'),
         ('18', '18 H'),
         ('19', '19 H'), ('20', '20 H'), ('21', '21 H'), ('22', '22 H'), ('23', '23 H'), ('24', '24 H')],
        string='Hourly')
    notes = fields.Text()
    prescription_id = fields.Many2one(
        'prescription.creation', string='Prescription')
# prescription_creation_id_manager,prescription_creation_name,model_prescription_creation,,1,1,1,1
# prescription_creation_id_reciption,prescription_creation_name,model_prescription_creation,ksc_prescription_receptionist,1,1,1,1
# prescription_creation_id_doctor,prescription_creation_name,model_prescription_creation,ksc_prescription_doctor,1,1,1,1
# prescription_creation_id_nuse,prescription_creation_name,model_prescription_creation,ksc_prescription_nurse,1,1,1,1


class createPrescription(models.Model):
    _name = 'prescription.creation'
    _description = 'the creation of prescription'

    name_of_appointment = fields.Char(string='Name')
    name = fields.Char(string='Prescription Id',
                       readonly=True, copy=False, tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done')], default='draft')
    patient_id = fields.Many2one(
        'res.partner', domain='[("is_patient", "=", True)]', string='Patient')
    physician_id = fields.Many2one(
        'res.partner', domain='[("is_physician", "=", True)]', string='Physician')
    date = fields.Date(
        string='Date', default=lambda self: fields.Datetime.now(), readonly=True)
    medication_line_ids = fields.One2many(
        'line.medication', 'prescription_id', string='Medication Lines')

    @api.model
    def create(self, values):
        if values.get('name', 'New Prescription') == 'New Prescription':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'prescription.creation') or 'New Prescription'
        return super(createPrescription, self).create(values)

    def write(self, vals):
        for res in self:
            if res.physician_id.user_id.id != res.env.user.id:
                raise UserError(
                    "You are not allowed to edit a prescription created by another doctor!!")
        return super(createPrescription, self).write(vals)

    def action_done(self):
        self.state = 'done'

    def print_prescription(self):
        return self.env.ref('ksc_prescription_model.prescription_print').report_action(self)

    def _valid_field_parameter(self, field, name):
        # Allow 'tracking' parameter for fields
        if name == "tracking":
            return True
        return super()._valid_field_parameter(field, name)


class Partner(models.Model):
    _inherit = "res.partner"

    prescription_count = fields.Integer(
        string='Prescription', compute='count_of_prescription')

    @api.onchange("phone")
    def remove_spaces_from_phone_number(self):
        if self.phone:
            self.phone = self.phone.replace(' ', '')

    @api.constrains('phone')
    def change_phone(self):
        if self.phone:
            self.phone.replace(' ', '')

    @api.onchange("mobile")
    def remove_spaces_from_mobile_number(self):
        if self.mobile:
            self.mobile = self.mobile.replace(' ', '')

    @api.constrains('mobile')
    def change_mobile(self):
        if self.mobile:
            self.mobile.replace(' ', '')

    def count_of_prescription(self):
        for rec in self:
            rec.prescription_count = self.env['prescription.creation'].search_count(
                [('patient_id', '=', self.id)])

    def action_view_prescription(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_prescription_model.ksc_prescription_mode_ksc")
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action


class PediatricPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_prescription_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        prescription_ids = self.env['prescription.creation'].search(
            domain, order="date asc").ids
        if prescription_ids:
            return self.env.ref(
                'ksc_prescription_model.prescription_patient_file_action').report_action([prescription_ids])
        else:
            raise UserError("There's Nothing To Print")
