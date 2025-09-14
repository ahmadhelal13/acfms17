from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import time, datetime, timedelta


class CliniQueue(models.Model):
    _inherit = 'ksc.appointment'

    def print_clinic_queue(self):
        self.get_queue_number()
        current_id = self._origin.id
        queue_id = self.env[f'ksc.{self.get_clinic_name()}.appointment'].search([
            ('id', '=', current_id)])
        if queue_id:
            return self.env.ref(f"{self.get_clinic_queue_report_id()}").report_action(queue_id)
        else:
            raise UserWarning('empty')

    def get_clinic_queue_report_id(self):
        return ""


class DentalCliniQueue(models.Model):
    _inherit = 'ksc.dental.appointment'
    hospital_name = fields.Char(default="الأسنان")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.dental_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_dental.ksc_dental_doctor"


class DermaQueue(models.Model):
    _inherit = 'ksc.dermatology.appointment'
    hospital_name = fields.Char(default="الجلدية",)

    def get_clinic_queue_report_id(self):
        return "clinic_queue.derma_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_dermatology.ksc_dermatology_doctor"


class PactitionerCliniQueue(models.Model):
    _inherit = 'ksc.practitioner.appointment'
    hospital_name = fields.Char(default="الممارس العام")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.practitioner_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_general_practitioner.ksc_practitioner_doctor"


class PactitionerCliniQueue(models.Model):
    _inherit = 'ksc.genetics.appointment'
    hospital_name = fields.Char(default="الأجنة")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.genetics_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_genetics.ksc_genetics_doctor"


class InternalMedQueue(models.Model):
    _inherit = 'ksc.medicine.appointment'
    hospital_name = fields.Char(default="الباطنية")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.medicine_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_medicine.ksc_medicine_doctor"


class NoseEarQueue(models.Model):
    _inherit = 'ksc.nose_and_ear.appointment'
    hospital_name = fields.Char(default="الأنف و الأذن")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.nose_and_ear_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_nose_and_ear.ksc_nose_and_ear_doctor"


class NutritionQueue(models.Model):
    _inherit = 'ksc.nutrition.appointment'
    hospital_name = fields.Char(default="التغذية")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.nutrition_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_nutrition.ksc_nutrition_doctor"


class ObsGYNQueue(models.Model):
    _inherit = 'ksc.obstetrics_and_gynecology.appointment'
    hospital_name = fields.Char(default="النساء والتوليد")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.obstetrics_and_gynecology_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_obstetrics_and_gynecology.ksc_obstetrics_and_gynecology_doctor"


class OphthalmologyQueue(models.Model):
    _inherit = 'ksc.ophthalmology.appointment'

    hospital_name = fields.Char(default="العيون")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.ophthalmology_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_ophthalmology.ksc_ophthalmology_doctor"


class OrthopedicQueue(models.Model):
    _inherit = 'ksc.orthopedic.appointment'

    hospital_name = fields.Char(default="العظام")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.orthopedic_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_orthopedic.ksc_orthopedic_doctor"


class PediatricQueue(models.Model):
    _inherit = 'ksc.pediatric.appointment'

    hospital_name = fields.Char(default="الأطفال")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.pediatric_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_pediatric.ksc_pediatric_doctor"


class PhysiotherapyQueue(models.Model):
    _inherit = 'ksc.physiotherapy.appointment'

    hospital_name = fields.Char(default="العلاج الطبيعي")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.physiotherapy_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_physiotherapy.ksc_physiotherapy_doctor"


class UrologyQueue(models.Model):
    _inherit = 'ksc.urology.appointment'

    hospital_name = fields.Char(default="المسالك البولية")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.urology_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_urology.ksc_urology_doctor"


class RadiologyQueue(models.Model):
    _inherit = 'ksc.radiology.appointment'

    hospital_name = fields.Char(default="الأشعة")

    def get_clinic_queue_report_id(self):
        return "clinic_queue.radiology_queue_number_report_action"

    def get_doctor_clinic_group(self):
        return "ksc_radiology.ksc_radiology_doctor"


class LabRequestQueue(models.Model):
    _inherit = 'ksc.laboratory.request'

    hospital_name = fields.Char(default="المعمل")
    queue_number = fields.Integer(readonly=True)
    start_date = fields.Datetime(string='Start Date', readonly=True, copy=False,
                                 default=lambda self: datetime.now() - timedelta(hours=3))
    end_date = fields.Datetime(string='End Date', readonly=True, copy=False,
                               default=lambda self: datetime.now() - timedelta(hours=3, minutes=-20))

    def print_lab_queue(self):
        self.get_queue_number()
        current_id = self._origin.id
        queue_id = self.env['ksc.laboratory.request'].search(
            [('id', '=', current_id)])
        if queue_id:
            return self.env.ref('clinic_queue.lab_queue_number_report_action').report_action(queue_id)
        else:
            raise UserWarning('empty')

    def get_queue_number(self):
        start_of_day = self.start_date.strftime('%m/%d/%Y 00:00:00')
        end_of_day = self.start_date.strftime('%m/%d/%Y 23:59:59')
        prev_app_id = self.env['ksc.laboratory.request'].search([('start_date', '>=', start_of_day), ('start_date', '<', end_of_day),
                                                                 ('queue_number', '!=', 0)], order="start_date desc", limit=1)
        app_id = self.env['ksc.laboratory.request'].search([('start_date', '>=', start_of_day), (
            'start_date', '<', end_of_day), ('queue_number', '=', 0)], order="start_date desc", limit=1)
        if app_id:
            if prev_app_id:
                app_id[0].queue_number = prev_app_id[0].queue_number + 1
            else:
                app_id[0].queue_number = 1
