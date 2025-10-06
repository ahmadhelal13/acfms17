# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(selection_add=[('pediatric', 'Pediatric')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('pediatric', 'Pediatric')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('pediatric'):
            ids = self.env.company.pediatric_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_pediatric = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_pediatric = fields.Boolean()


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    pediatric_appt_id = fields.Many2one(
        'ksc.pediatric.appointment', ondelete="cascade", string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.pediatric_appt_id:
                rec.patient_id = rec.pediatric_appt_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.pediatric_appt_id:
                rec.clinic_name = rec.pediatric_appt_id.get_clinic_name()

# class KSCDiseases(models.Model):
#     _inherit = 'ksc.diseases'

#     pediatric_appt_id = fields.Many2one('ksc.pediatric.appointment', ondelete="cascade", string='Appointment')


class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"
    _description = 'Diseases Lines'
    pediatric_appt_id = fields.Many2one(
        'ksc.pediatric.appointment', ondelete="cascade", string='Pediatric Appointment')


class KscpediatricAppointment(models.Model):
    _name = 'ksc.pediatric.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc pediatric Appointment'
    _order = "start_date desc"

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}
    service_line_ids = fields.One2many('ksc.service.line', 'pediatric_appt_id', string='Service Line',copy=False)
    # diseases_ids = fields.One2many('ksc.diseases', 'pediatric_appt_id')
    diseases_ids = fields.One2many('ksc.diseases.line', 'pediatric_appt_id')
    clinic_name = fields.Char(default="pediatric")

    def name_of_clinic(self):
        return "pediatric"

    def get_available(self):
        return "avalibel_in_pediatric"


    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get("name", "New Appointment") == "New Appointment":
                vals["name"] = self.env["ir.sequence"].next_by_code("ksc.pediatric.appointment") or "New Appointment"

        return super(KscpediatricAppointment, self).create(vals_list)
    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.pediatric_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.pediatric_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.pediatric_consultation_product_id:
            consultation = self.env.user.company_id.pediatric_consultation_product_id.id
        return consultation

    def get_receptionist_clinic_group(self):
        return "ksc_pediatric.ksc_pediatric_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_pediatric.ksc_pediatric_nurse"

    def get_manager_clinic_group(self):
        return "ksc_pediatric.ksc_pediatric_manager"

    def get_doctor_clinic_group(self):
        return "ksc_pediatric.ksc_pediatric_doctor"

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'pediatric_appt_id': self.id,
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

    presenting_symptoms = fields.Text(string="PRESENTING SYMPTOMS")
    current_drug_therapy = fields.Text(string="CURRENT DRUG THERAPY")
    history_or_allergy = fields.Text(string="HISTORY OR ALLERGY")
    test_history = fields.Text(string="TEST HISTORY")
    development_history = fields.Text(string="DEVELOPMENT HISTORY")
    family_history = fields.Text(string="FAMILY HISTORY")
    immunization_history = fields.Text(string="IMMUNIZATION HISTORY")
    diet_history = fields.Text(string="DIET HISTORY")

    # =======physical exam====

    weight = fields.Char(string="Weight")
    height = fields.Char(string="Height")
    plus = fields.Char(string="Plus")
    head_cicumeerance = fields.Char(string="HEAD CICUMEERANCE")
    temp = fields.Char(string="Temp")
    bp = fields.Char(string="BP")

    skin = fields.Char(string="Skin")
    eyes = fields.Char(string="Eyes")
    far = fields.Char(string="FAR")
    nose = fields.Char(string="NOSE")
    teeth = fields.Char(string="TEETH")
    throat = fields.Char(string="THROAT")
    neck = fields.Char(string="NECK")
    tongue = fields.Char(string="Tongue")
    pallor = fields.Char(string="Pallor")
    icterus = fields.Char(string="ICTERUS")
    chest = fields.Char(string="Chest")
    heart = fields.Char(string="Heart")
    abdomen = fields.Text(string="Abdomen")

    nervoussystem = fields.Text(string="NERVOUSSYSTEM")
    muscul_oskeletal_system = fields.Text(string="MUSCUL OSKELETAL SYSTEM")
    genitalia = fields.Text(string="GENITALIA")
    investigation = fields.Text(string="Investigation")
    treatment = fields.Text(string="TREATMENT")


class PediatricPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_pediatric_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.pediatric.appointment'].search(
            domain, order="start_date asc").ids
        # raise UserError(lab_ids)
        if lab_ids:
            return self.env.ref(
                'ksc_pediatric.pediatric_patient_file_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
