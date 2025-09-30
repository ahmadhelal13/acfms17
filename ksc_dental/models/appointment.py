# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_dental = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_dental = fields.Boolean()


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    dental_appt_id = fields.Many2one(
        'ksc.dental.appointment', ondelete="cascade", string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.dental_appt_id:
                rec.patient_id = rec.dental_appt_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.dental_appt_id:
                rec.clinic_name = rec.dental_appt_id.get_clinic_name()


class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"
    _description = 'Diseases Lines'

    #
    dental_appt_id = fields.Many2one(
        'ksc.dental.appointment', ondelete="cascade", string='Dental Appointment')


class KscDentalAppointment(models.Model):
    _name = 'ksc.dental.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc Dental Appointment'
    _order = "start_date desc"

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}

    service_line_ids = fields.One2many('ksc.service.line', 'dental_appt_id', string='Service Line', copy=False)
    teeth_treatment_ids = fields.One2many(
        'medical.teeth.treatment', 'appt_id', 'Operations', readonly=True)
    diseases_ids = fields.One2many('ksc.diseases.line', 'dental_appt_id')
    # diseases_ids = fields.One2many('ksc.diseases', 'dental_appt_id')

    clinic_name = fields.Char(default="dental")

    def get_receptionist_clinic_group(self):
        return "ksc_dental.ksc_dental_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_dental.ksc_dental_nurse"

    def get_manager_clinic_group(self):
        return "ksc_dental.ksc_dental_manager"

    def get_doctor_clinic_group(self):
        return "ksc_dental.ksc_dental_doctor"

    def name_of_clinic(self):
        return "dental"

    def get_available(self):
        return "avalibel_in_dental"

    @api.model
    def create(self, values):
        if values.get('name', 'New Appointment') == 'New Appointment':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'ksc.dental.appointment') or 'New Appointment'
        return super(KscDentalAppointment, self).create(values)

    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.dental_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.dental_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.dental_consultation_product_id:
            consultation = self.env.user.company_id.dental_consultation_product_id.id
        return consultation

    # Methods to open the dental
    def action_dental_client_view(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self._get_dental_base_url() + '?patient_id=%d' % self.patient_id.id,
            'name': self.name,
            'target': 'self',
        }

    def _get_dental_base_url(self):
        return '/dental/web'

    def print_dental_patient_file(self):

        app_ids = self.search(
            [('patient_id', '=', self.patient_id.id)], order="start_date asc").ids
        return self.env.ref('ksc_dental.dental_patient_file_action').report_action([app_ids])
        if app_ids:
            raise UserError(app_ids)
        else:
            raise UserError('no ideas')

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'dental_appt_id': self.id,
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
