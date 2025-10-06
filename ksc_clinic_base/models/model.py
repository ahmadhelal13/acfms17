# -*- coding: utf-8 -*-
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv.expression import get_unaccent_wrapper


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Res Partner"
    _rec_name = "name"

    def _rec_count(self):
        for rec in self:
            rec.evaluation_count = len(rec.evaluation_ids)

    # def count_of_prescription(self):
    #     for rec in self:
    #         rec.prescription_count = len(rec.prescription_ids)

    is_patient = fields.Boolean()
    is_physician = fields.Boolean()
    is_vendor = fields.Boolean()

    name = fields.Char("Name", required=True, translate=True)
    first_name = fields.Char("First Name", compute="auto_save_name")
    sec_name = fields.Char("Second Name", compute="auto_save_name")
    third_name = fields.Char("Third Name", compute="auto_save_name")
    forth_name = fields.Char("Forth Name", compute="auto_save_name")
    arabic_first_name = fields.Char("Arabic First Name", compute="auto_save_arabic_name")
    arabic_sec_name = fields.Char("Arabic Second Name", compute="auto_save_arabic_name")
    arabic_third_name = fields.Char("Arabic Third Name", compute="auto_save_arabic_name")
    arabic_forth_name = fields.Char("Arabic Forth Name", compute="auto_save_arabic_name")
    arabic_name = fields.Char()
    code = fields.Char(string="Identification Code", default="/", help="Identifier provided by the Health Center.", copy=False, tracking=True, readonly=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", default="male", compute="gender_type", readonly=False, tracking=True, store=True)
    birthday = fields.Date(string="Date of Birth", tracking=True)
    age = fields.Char(string="Age", compute="_get_age")
    blood_group = fields.Selection([("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-")], string="blood group")
    new_blood_group = fields.Char("Blood Group")
    marital_status = fields.Selection(
        [
            ("single", "Single"),
            ("married", "Married"),
            ("widowed", "Widowed"),
            ("divorced", "Divorced"),
        ],
        string="Marital Status",
        default="single",
    )
    nationality = fields.Char()
    civil = fields.Char()
    diseases_ids = fields.One2many("ksc.diseases.line", "patient_id")

    evaluation_count = fields.Integer(compute="_rec_count", string="# Evaluations")
    evaluation_ids = fields.One2many("ksc.patient.evaluation", "patient_id", "Evaluations", index=True)  # Add index for better performance
    # prescription_count = fields.Integer(string='Prescription', compute='count_of_prescription')
    # prescription_ids = fields.One2many('prescription.creation', 'patient_id', 'Prescription')

    last_evaluation_id = fields.Many2one("ksc.patient.evaluation", string="Last Appointment", compute="_get_last_evaluation", readonly=True, store=True)
    weight = fields.Float(related="last_evaluation_id.weight", string="Weight", help="Weight in KG", readonly=True)
    height = fields.Float(related="last_evaluation_id.height", string="Height", help="Height in cm", readonly=True)
    temp = fields.Float(related="last_evaluation_id.temp", string="Temp", readonly=True)
    hr = fields.Float(related="last_evaluation_id.hr", string="HR", help="Heart Rate", readonly=True)
    rr = fields.Float(related="last_evaluation_id.rr", string="RR", readonly=True, help="Respiratory Rate")
    systolic_bp = fields.Integer(related="last_evaluation_id.systolic_bp", string="Systolic BP")
    diastolic_bp = fields.Integer(related="last_evaluation_id.diastolic_bp", string="Diastolic BP")
    spo2 = fields.Float(related="last_evaluation_id.spo2", string="SpO2", readonly=True, help="Oxygen Saturation, percentage of oxygen bound to hemoglobin")
    bmi = fields.Float(related="last_evaluation_id.bmi", string="Body Mass Index", readonly=True)
    bmi_state = fields.Selection(related="last_evaluation_id.bmi_state", string="BMI State", readonly=True)
    years = fields.Float(compute="_get_age")
    months = fields.Float(compute="_get_age")
    days = fields.Float(compute="_get_age")
    civil_gender = fields.Char()

    display_name = fields.Char(compute="compute_display_name", translate=True, store=False)

    _sql_constraints = [("civil_unique", "UNIQUE(civil)", "The civil must be unique")]

    # ===========================medical history=========================
    heart_disease = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Heart disease - أمراض قلبية")
    bleeding = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Bleeding - النزف")
    hypertension = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Hypertension - أرتفاع")
    diabetes = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Diabetes - السكري")
    asthma = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Asthma - الربو ")
    thyroid_disease = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Thyroid disease - أمراض الغده الدرقية")
    rheumatoid_arthritis = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Rheumatoid arthritis - التهاب مفاصل رثيوي")
    others_diseases = fields.Text(string="Others - أمراض اخرى")

    do_you_take_any_medicine_now = fields.Selection([("1", "Yes"), ("2", "No")], default="2", string="Do you take any medicine now ? هل تأخذ أدويه حاليا؟ ")
    are_you_allergic_to_any_medicine = fields.Selection(
        [("1", "Penicilli - بنسلين"), ("2", "Codeine - الكودنين"), ("3", "Aspirin - الأسبرين"), ("4", "Loc,Anase - المخدر الموضعي")],
        default="1",
        string="Are you allergic to any medicine ? هل لديك حساسيه للأدوية",
    )
    others_drugs = fields.Text(string="Others - أدوية اخرى")
    for_ladies = fields.Selection([("1", "pregnancy - حمل"), ("2", " Breast feeding - إرضاع")], default="2", string="For ladies - للسيدات")
    remarks = fields.Text(string="Remarks - ملاحظات ")
    extra_oral_exam = fields.Text(string="Extra Oral Exam")
    intra_oral_exam = fields.Text(string="Intra Oral Exam")
    x_ray_investigation = fields.Text(string="X-Ray Investigation")
    periaplcal = fields.Text(string="Periaplcal")
    occlusal = fields.Text(string="Occlusal")
    b_w = fields.Text(string="B.W")
    o_p_g = fields.Text(string="O.P.G")
    other_investigations = fields.Text(string="Other Investigations")
    diagnosis = fields.Text(string="Diagnosis.")
    treatment_procedures = fields.Text("Treatment Procedures")
    # ====================================================================

    @api.depends("civil_gender")
    def gender_type(self):
        for rec in self:
            if rec.civil_gender == "M":
                rec.gender = "male"
            elif rec.civil_gender == "F":
                rec.gender = "female"
            else:
                rec.gender = "male"

    def compute_display_name(self):
        for rec in self:
            rec.display_name = rec.name

    def auto_arabic_name(self):
        translable_name = self.env["ir.translation"]
        for rec in self:
            name_record = translable_name.search([("src", "=", rec.name), ("lang", "=", "ar_001")], limit=1)
            if name_record and rec.arabic_name:
                name_record.value = rec.arabic_name

    def index_exists(self, ls, i):
        return (0 <= i < len(ls)) or (-len(ls) <= i < 0)

    @api.depends("name")
    def auto_save_name(self):
        for rec in self:
            if rec.name:
                full_name_list = (rec.name).split(" ")
                if rec.index_exists(full_name_list, 0):
                    rec.first_name = full_name_list[0]
                else:
                    rec.first_name = ""
                if rec.index_exists(full_name_list, 1):
                    rec.sec_name = full_name_list[1]
                else:
                    rec.sec_name = ""
                if rec.index_exists(full_name_list, 2):
                    rec.third_name = full_name_list[2]
                else:
                    rec.third_name = ""
                if rec.index_exists(full_name_list, 3):
                    rec.forth_name = full_name_list[3]
                else:
                    rec.forth_name = ""
            else:
                rec.first_name = ""
                rec.sec_name = ""
                rec.third_name = ""
                rec.forth_name = ""

    @api.depends("arabic_name")
    def auto_save_arabic_name(self):
        for rec in self:
            if rec.arabic_name:
                full_name_list = (rec.arabic_name).split(" ")
                if rec.index_exists(full_name_list, 0):
                    rec.arabic_first_name = full_name_list[0]
                else:
                    rec.arabic_first_name = ""
                if rec.index_exists(full_name_list, 1):
                    rec.arabic_sec_name = full_name_list[1]
                else:
                    rec.arabic_sec_name = ""
                if rec.index_exists(full_name_list, 2):
                    rec.arabic_third_name = full_name_list[2]
                else:
                    rec.arabic_third_name = ""
                if rec.index_exists(full_name_list, 3):
                    rec.arabic_forth_name = full_name_list[3]
                else:
                    rec.arabic_forth_name = ""
            else:
                rec.arabic_first_name = ""
                rec.arabic_sec_name = ""
                rec.arabic_third_name = ""
                rec.arabic_forth_name = ""

    @api.depends("evaluation_ids", "evaluation_ids.state", "evaluation_ids.create_date")
    def _get_last_evaluation(self):
        for rec in self:
            evaluation_ids = rec.evaluation_ids.filtered(lambda x: x.state == "done")

            if evaluation_ids:
                rec.last_evaluation_id = evaluation_ids[0].id if evaluation_ids else False
            else:
                rec.last_evaluation_id = False

    def action_evaluation(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ksc_clinic_base.action_ksc_patient_evaluation")
        action["domain"] = [("patient_id", "=", self.id)]
        action["context"] = {"default_patient_id": self.id}
        return action

    # def action_prescription(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("ksc_prescription_model.prescription_form_view")
    #     action['domain'] = [('patient_id', '=', self.id)]
    #     # action['context'] = {'default_patient_id': self.id}
    #     return action

    def calculate_age_weekly(self):
        records = self.search([("is_patient", "=", True)])
        for rec in records:
            rec.age = rec._get_age

    def _get_age(self):
        for rec in self:
            rec.age = 0
            rec.years = 0
            rec.months = 0
            rec.days = 0
            if rec.birthday:
                end_data = fields.Datetime.now()
                delta = relativedelta(end_data, rec.birthday)
                rec.years = delta.years
                rec.months = delta.months + delta.years * 12
                rec.days = delta.years * 365 + delta.months * 30 + delta.days
                rec.age = "%s %s %s %s %s %s" % (delta.years, _("years"), delta.months, _("months"), delta.days, _("days"))

    @api.model
    def create(self, values):
        if values.get("code", "/") == "/":
            if values.get("is_patient"):
                values["code"] = self.env["ir.sequence"].next_by_code("patient") or ""
            elif values.get("is_physician"):
                values["code"] = self.env["ir.sequence"].next_by_code("physician") or ""
            elif values.get("is_vendor"):
                values["code"] = self.env["ir.sequence"].next_by_code("vendor") or ""
            else:
                values["code"] = self.env["ir.sequence"].next_by_code("other") or ""
            if not values.get("civil"):
                values["civil"] = values["code"] or ""
        return super(ResPartner, self).create(values)

    @api.model
    def _name_search(self, name="", args=None, operator="ilike", limit=100, order=None):
        args = args or []
        domain = []

        if name:
            domain = [
                "|",
                "|",
                "|",
                "|",
                "|",
                "|",
                "|",
                "|",
                ("email", operator, name),
                ("arabic_name", operator, name),
                ("name", operator, name),
                ("code", operator, name),
                ("civil", operator, name),
                ("phone", operator, name),
                ("mobile", operator, name),
                ("ref", operator, name),
                ("vat", operator, name),
            ]

        return self._search(domain + args, limit=limit, order=order)

    def action_patient_barcode_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "barcode.patient.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_patient_id": self.id,
            },
        }


class KscDiseasesLine(models.Model):
    _name = "ksc.diseases.line"
    _description = "Diseases lines"

    name = fields.Char(
        string="Name",
        translate=True,
        help="Disease name",
    )
    appointments_id = fields.Many2one("ksc.appointment")
    disease_id = fields.Many2one("ksc.diseases")
    patient_id = fields.Many2one("res.partner")


class PatientGeneraltWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_patient_info_for_this_patient(self):
        if self.patient_id:
            return self.env.ref("ksc_clinic_base.patient_file_report_action").report_action(self.patient_id.id)
        else:
            raise UserError("There's Nothing To Print")
