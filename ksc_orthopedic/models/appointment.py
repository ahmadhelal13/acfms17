# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(selection_add=[('orthopedic', 'Orthopedic')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('orthopedic', 'Orthopedic')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('orthopedic'):
            ids = self.env.company.orthopedic_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_orthopedic = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_orthopedic = fields.Boolean()


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    orthopedic_appt_id = fields.Many2one(
        'ksc.orthopedic.appointment', ondelete="cascade", string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.orthopedic_appt_id:
                rec.patient_id = rec.orthopedic_appt_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.orthopedic_appt_id:
                rec.clinic_name = rec.orthopedic_appt_id.get_clinic_name()

# class KSCDiseases(models.Model):
#     _inherit = 'ksc.diseases'

#     orthopedic_appt_id = fields.Many2one('ksc.orthopedic.appointment', ondelete="cascade", string='Appointment')


class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"

    orthopedic_appt_id = fields.Many2one(
        'ksc.orthopedic.appointment', ondelete="cascade", string='Orthopedic Appointment')


class KscOrthopedicAppointment(models.Model):
    _name = 'ksc.orthopedic.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc Orthopedic Appointment'
    _order = "start_date desc"

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}
    service_line_ids = fields.One2many('ksc.service.line', 'orthopedic_appt_id', string='Service Line', copy=False)
    # diseases_ids = fields.One2many('ksc.diseases', 'orthopedic_appt_id')
    diseases_ids = fields.One2many('ksc.diseases.line', 'orthopedic_appt_id')
    clinic_name = fields.Char(default="orthopedic")

    def name_of_clinic(self):
        return "orthopedic"

    def get_available(self):
        return "avalibel_in_orthopedic"

    @api.model
    def create(self, values):
        if values.get('name', 'New Appointment') == 'New Appointment':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'ksc.orthopedic.appointment') or 'New Appointment'
        return super(KscOrthopedicAppointment, self).create(values)

    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.orthopedic_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.orthopedic_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.orthopedic_consultation_product_id:
            consultation = self.env.user.company_id.orthopedic_consultation_product_id.id
        return consultation
    weight = fields.Char(string="Weight")
    height = fields.Char(string="Height")
    bp = fields.Char(string="BP")

    present_complain = fields.Text(string="Present Complain")
    clinical_examination = fields.Text(string="Clinical Examination")
    followup_treatment_advice = fields.Text(
        string="Followup, Treatment & Advice:")

    def get_receptionist_clinic_group(self):
        return "ksc_orthopedic.ksc_orthopedic_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_orthopedic.ksc_orthopedic_nurse"

    def get_manager_clinic_group(self):
        return "ksc_orthopedic.ksc_orthopedic_manager"

    def get_doctor_clinic_group(self):
        return "ksc_orthopedic.ksc_orthopedic_doctor"

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'orthopedic_appt_id': self.id,
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


class OrthopedicPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_orthopedic_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.orthopedic.appointment'].search(domain, order="start_date asc"
                                                                ).ids
        # raise UserError(lab_ids)
        if lab_ids:
            return self.env.ref(
                'ksc_orthopedic.orthopedic_patient_file_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
