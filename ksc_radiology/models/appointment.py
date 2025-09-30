# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(selection_add=[('radiology', 'Radiology')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('radiology', 'Radiology')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('radiology'):
            ids = self.env.company.radiology_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_radiology = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_radiology = fields.Boolean()


class radiologyRequestLines(models.Model):
    _name = 'radiology.request.lines'
    _description = 'Radiology Request Lines'

    test_id = fields.Many2one('radio.lines', string='Test', required=True)
    product_price = fields.Float('Sale Price')
    notes = fields.Char('Special instructions')
    test_result = fields.Char('Radio Result')
    radio_appointment_id = fields.Many2one('ksc.radiology.appointment')
    is_invoiced = fields.Boolean()

    @api.onchange('test_id')
    def get_product_price(self):
        self.product_price = self.test_id.product_id.lst_price


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    radiology_appt_id = fields.Many2one(
        'ksc.radiology.appointment', ondelete="cascade", string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.radiology_appt_id:
                rec.patient_id = rec.radiology_appt_id.patient_id

# class KSCDiseases(models.Model):
#     _inherit = 'ksc.diseases'

#     radiology_appt_id = fields.Many2one('ksc.radiology.appointment', ondelete="cascade", string='Appointment')


class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"
    _description = 'Diseases Lines'
    radiology_appt_id = fields.Many2one(
        'ksc.radiology.appointment', ondelete="cascade", string='Radio Appointment')


class KscradiologyAppointment(models.Model):
    _name = 'ksc.radiology.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc radiology Appointment'
    _order = "start_date desc"

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}
    service_line_ids = fields.One2many('ksc.service.line', 'radiology_appt_id', string='Service Line', copy=False)
    radio_type_id = fields.Many2one(
        'radio.test.type', string='Radio Type', required=True)
    lines_ids = fields.One2many(
        'radiology.request.lines', 'radio_appointment_id', string='Lines')
    invoice_id = fields.Many2one('account.move', string='Invoice', copy=False)
    radio_notes = fields.Text(string='Radio Notes')
    # diseases_ids = fields.One2many('ksc.diseases', 'radiology_appt_id')
    diseases_ids = fields.One2many('ksc.diseases.line', 'radiology_appt_id')
    clinic_name = fields.Char(default="radiology")

    def get_receptionist_clinic_group(self):
        return "ksc_radiology.ksc_radiology_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_radiology.ksc_radiology_nurse"

    def get_manager_clinic_group(self):
        return "ksc_radiology.ksc_radiology_manager"

    def get_doctor_clinic_group(self):
        return "ksc_radiology.ksc_radiology_doctor"

    def name_of_clinic(self):
        return "radiology"

    def get_available(self):
        return "avalibel_in_radiology"

    def create_invoice(self):
        if not self.lines_ids:
            raise UserError(_("Please add lab Tests first."))
        product_data = []
        for line in self.lines_ids:
            if not line.is_invoiced:
                product_data.append({
                    'product_id': line.test_id.product_id,
                    'price_unit': line.product_price,
                })
                line.is_invoiced = True
        inv_data = {
            'invoice_date': self.start_date,
            'clinic': self.get_clinic_name(),
            'appointment_name': self.name,
        }
        if product_data:
            invoice = self.ksc_create_invoice(
                partner=self.patient_id, product_data=product_data, inv_data=inv_data)
            invoice.action_post()
            self.invoice_id = invoice.id
            return self.view_invoice()

    @api.model
    def create(self, values):
        if values.get('name', 'New Appointment') == 'New Appointment':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'ksc.radiology.appointment') or 'New Appointment'
        return super(KscradiologyAppointment, self).create(values)

    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.radiology_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.radiology_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.radiology_consultation_product_id:
            consultation = self.env.user.company_id.radiology_consultation_product_id.id
        return consultation

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'radiology_appt_id': self.id,
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


class Partner(models.Model):
    _inherit = "res.partner"

    radio_test_count = fields.Integer(
        string='Radio Test', compute='count_of_radio_test')

    def count_of_radio_test(self):
        for rec in self:
            rec.radio_test_count = self.env['ksc.radiology.appointment'].search_count(
                [('patient_id', '=', self.id)])

    def action_view_radio_test(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_radiology.action_ksc_radiology_consultation")
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action


class RadiologyPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_radiology_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.radiology.appointment'].search(
            domain, order="start_date asc").ids
        # raise UserError(lab_ids)
        if lab_ids:
            return self.env.ref(
                'ksc_radiology.radio_result_report_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
