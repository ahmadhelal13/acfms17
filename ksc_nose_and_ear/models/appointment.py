# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(selection_add=[('nose_and_ear', 'Nose and Ear')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('nose_and_ear', 'Nose and Ear')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('nose_and_ear'):
            ids = self.env.company.nose_and_ear_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_nose_and_ear = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_nose_and_ear = fields.Boolean()


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    nose_and_ear_appt_id = fields.Many2one(
        'ksc.nose_and_ear.appointment', ondelete="cascade", string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.nose_and_ear_appt_id:
                rec.patient_id = rec.nose_and_ear_appt_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.nose_and_ear_appt_id:
                rec.clinic_name = rec.nose_and_ear_appt_id.get_clinic_name()

# class KSCDiseases(models.Model):
#     _inherit = 'ksc.diseases'

#     nose_and_ear_appt_id = fields.Many2one('ksc.nose_and_ear.appointment', ondelete="cascade", string='Appointment')


class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"
    _description = 'Diseases Lines'
    nose_and_ear_appt_id = fields.Many2one(
        'ksc.nose_and_ear.appointment', ondelete="cascade", string='N&E Appointment')


class KscNoseAndEarAppointment(models.Model):
    _name = 'ksc.nose_and_ear.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc Nose And Ear Appointment'
    _order = "start_date desc"

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}

    service_line_ids = fields.One2many(
        'ksc.service.line', 'nose_and_ear_appt_id', string='Service Line', copy=False)
    # diseases_ids = fields.One2many('ksc.diseases', 'nose_and_ear_appt_id')
    diseases_ids = fields.One2many('ksc.diseases.line', 'nose_and_ear_appt_id')
    clinic_name = fields.Char(default="nose_and_ear")

    def get_receptionist_clinic_group(self):
        return "ksc_nose_and_ear.ksc_nose_and_ear_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_nose_and_ear.ksc_nose_and_ear_nurse"

    def get_manager_clinic_group(self):
        return "ksc_nose_and_ear.ksc_nose_and_ear_manager"

    def get_doctor_clinic_group(self):
        return "ksc_nose_and_ear.ksc_nose_and_ear_doctor"

    def name_of_clinic(self):
        return "nose_and_ear"

    def get_available(self):
        return "avalibel_in_nose_and_ear"

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get('name', 'New Appointment') == 'New Appointment':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'ksc.nose_and_ear.appointment') or 'New Appointment'
        return super(KscNoseAndEarAppointment, self).create(vals_list)

    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.nose_and_ear_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.nose_and_ear_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.nose_and_ear_consultation_product_id:
            consultation = self.env.user.company_id.nose_and_ear_consultation_product_id.id
        return consultation

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'nose_and_ear_appt_id': self.id,
                })
        if self.service_line_ids:
            for service in self.service_line_ids:
                if not service.is_invoiced:
                    self.state = 'to_invoice'
                else:
                    self.state = 'done'
                    self.set_values_for_price_list()
        else:
            self.state = 'done'


class NoseEarPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_nose_ear_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.nose_and_ear.appointment'].search(
            domain, order="start_date asc").ids
        # raise UserError(lab_ids)
        if lab_ids:
            return self.env.ref(
                'ksc_nose_and_ear.nose_and_ear_patient_file_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
