# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(selection_add=[('urology', 'Urology')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('urology', 'Urology')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('urology'):
            ids = self.env.company.urology_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_urology = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_urology = fields.Boolean()


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    urology_appt_id = fields.Many2one(
        'ksc.urology.appointment', ondelete="cascade", string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.urology_appt_id:
                rec.patient_id = rec.urology_appt_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.urology_appt_id:
                rec.clinic_name = rec.urology_appt_id.get_clinic_name()


class KSCSessionServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Session Services"

    urology_session_service_id = fields.Many2one('ksc.urology.appointment', ondelete="cascade",
                                                 string='Sessions Service')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.urology_session_id:
                rec.patient_id = rec.urology_session_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.urology_session_id:
                rec.clinic_name = rec.urology_session_id.get_clinic_name()


# class KSCDiseases(models.Model):
#     _inherit = 'ksc.diseases'

#     urology_appt_id = fields.Many2one('ksc.urology.appointment', ondelete="cascade", string='Appointment')

class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"
    _description = 'Diseases Lines'
    urology_appt_id = fields.Many2one(
        'ksc.urology.appointment', ondelete="cascade", string='Urology Appointment')


class KscurologyAppointment(models.Model):
    _name = 'ksc.urology.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc urology Appointment'
    _order = "start_date desc"

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}
    service_line_ids = fields.One2many('ksc.service.line', 'urology_appt_id', string='Service Line', copy=False)

    # diseases_ids = fields.One2many('ksc.diseases', 'urology_appt_id')
    diseases_ids = fields.One2many('ksc.diseases.line', 'urology_appt_id')
    clinic_name = fields.Char(default="urology")

    def get_receptionist_clinic_group(self):
        return "ksc_urology.ksc_urology_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_urology.ksc_urology_nurse"

    def get_manager_clinic_group(self):
        return "ksc_urology.ksc_urology_manager"

    def get_doctor_clinic_group(self):
        return "ksc_urology.ksc_urology_doctor"

    def action_whats_app_api(self):
        msg = 'Hi ya handsa el message de mn free api whats app'
        whats_app_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (
            self.patient_id.mobile, msg)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whats_app_url,
        }

    def name_of_clinic(self):
        return "urology"

    def get_available(self):
        return "avalibel_in_urology"

    @api.model
    def create(self, values):
        if values.get('name', 'New Appointment') == 'New Appointment':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'ksc.urology.appointment') or 'New Appointment'
        return super(KscurologyAppointment, self).create(values)

    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.urology_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.urology_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.urology_consultation_product_id:
            consultation = self.env.user.company_id.urology_consultation_product_id.id
        return consultation

    def create_invoice(self):
        product_id = self.product_id
        product_data = []
        if not product_id:
            raise UserError(_("Please Set Consultation Service first."))
        else:
            if not self.is_invoiced:
                product_data.append({'product_id': product_id})
                self.is_invoiced = True
        for service in self.service_line_ids:
            if not service.is_invoiced:
                product_data.append({
                    'product_id': service.product_id,
                })
                service.is_invoiced = True

        inv_data = {
            'physician_id': self.physician_id and self.physician_id.id or False,
            'partner_id': self.patient_id.id,
            'clinic': self.get_clinic_name(),
            'appointment_name': self.name,
        }
        if product_data or not self.is_invoiced:
            invoice = self.ksc_create_invoice(
                partner=self.patient_id, product_data=product_data, inv_data=inv_data)
            # invoice.action_post()
            self.invoice_id = invoice.id
            return self.view_invoice()

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'urology_appt_id': self.id,
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

    patient_actual_complains = fields.Text(string="Patient actual complains")
    medical_record = fields.Text(string="Medical Record")
    surgical_record = fields.Text(string="Surgical Record")
    familial_Antecedents = fields.Text(string="Familial Antecedents")
    request_laboratory = fields.Text(string="Request-laboratory")
    imagistic = fields.Text(string="Imagistic")
    diagnose = fields.Text(string="Diagnose")
    treatment = fields.Text(string="Treatment")
    tip_of_incontinence = fields.Text(string="Tip of incontinence")
    no_of_stages = fields.Text(string="No. of stages")
    stage = fields.Text(string="Stage")

    # ==============================
    # =====Abdominal ultrasound=====
    # ==============================

    # Left kidney
    lf_shape_value1 = fields.Char(
        string="Normal in site shape and echopathern measuring")
    lf_shape_value2 = fields.Char(
        string="Normal in site shape and echopathern measuring")
    lf_shape_value3 = fields.Char(
        string="Normal in site shape and echopathern measuring")
    lf_aspect_of_acute_pyelonephritis = fields.Boolean(
        string="Aspect of acute pyelonephritis")
    lf_aspect_of_chronic_pyelonephritis = fields.Boolean(
        string="Aspect of chronic pyelonephritis.")
    lf_visible_stone = fields.Selection(
        [('1', 'SUP. Calycal'), ('2', 'MED.Calycal'), ('3', 'LUF.Calical')], string="Visible stone")

    # right kidney
    rt_shape_value1 = fields.Char(
        string="Normal in site shape and echopathern measuring")
    rt_shape_value2 = fields.Char(
        string="Normal in site shape and echopathern measuring")
    rt_shape_value3 = fields.Char(
        string="Normal in site shape and echopathern measuring")
    rt_aspect_of_acute_pyelonephritis = fields.Boolean(
        string="Aspect of acute pyelonephritis")
    rt_aspect_of_chronic_pyelonephritis = fields.Boolean(
        string="Aspect of chronic pyelonephritis.")
    rt_visible_stone = fields.Selection(
        [('1', 'SUP. Calycal'), ('2', 'MED.Calycal'), ('3', 'LUF.Calical')], string="Visible stone")

    # Bladder:-

    well_conturated = fields.Selection(
        [('1', 'No stones'), ('2', 'Stones')], string="Well conturated")
    well_conturated_value = fields.Char(string='Well conturated In MM')
    masses = fields.Selection(
        [('1', 'Yes'), ('2', 'No')], default="2", string="Masses")
    diverticulae = fields.Selection(
        [('1', 'Yes'), ('2', 'No')], default="2", string="Diverticulae")
    pvr = fields.Char(string="PVR")
    Aspect = fields.Selection(
        [('1', 'Acute Cystits'), ('2', 'Chronic Cystits')], string="Aspect")

    # PROSTATE
    normal_size_and_shape = fields.Char(string="Normal size and shape")
    aspect_of_acute_prostatitis = fields.Char(
        string="Aspect of acute prostatitis")
    aspect_of_chronic_prostatitis = fields.Char(
        string="Aspect of chronic prostatitis")
    enlarged_in_volume_measure = fields.Char(
        string="Enlarged in volume measure")


class UrologyPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_urology_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.urology.appointment'].search(domain , order="start_date asc").ids
        # raise UserError(lab_ids)
        if lab_ids:
            return self.env.ref(
                'ksc_urology.urology_patient_file_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
