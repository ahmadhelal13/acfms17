from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PatientWizard(models.TransientModel):
    _name = "patient.wizard"
    _description = "patient wizard"

    patient_id = fields.Many2one('res.partner', readonly=True)

    # def print_general_info(self):
    #     return self.env.ref(
    #         'ksc_patient_report.patient_file_general_report_action').report_action(self.patient_id.id)

    # def print_lab_result_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['patient.laboratory.test'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_laboratory.lab_result_report_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_radio_result_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     radio_ids = self.env['ksc.radiology.appointment'].search(
    #         domain).ids
    #     if radio_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.radio_result_report_action').report_action([radio_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_dental_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.dental.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.dental_patient_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_derma_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.dermatology.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.derma_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_practitioner_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.practitioner.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.practitioner_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_inter_medicin_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.medicine.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.medicine_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_nose_ear_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.nose_and_ear.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.nose_and_ear_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_nutrition_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.nutrition.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.nutrition_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_gnecology_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.genetics.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.genetics_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_opthamology_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.ophthalmology.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.ophthalmology_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_orthopedic_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.orthopedic.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.orthopedic_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_pediratic_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.pediatric.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.pediatric_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_physiotheriby_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.physiotherapy.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.physiotherapy_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")

    # def print_urology_info_for_this_patient(self):
    #     domain = [('patient_id', '=', self.patient_id.id)]
    #     lab_ids = self.env['ksc.urology.appointment'].search(
    #         domain).ids
    #     if lab_ids:
    #         return self.env.ref(
    #             'ksc_patient_report.urology_patient_file_action').report_action([lab_ids])
    #     else:
    #         raise UserError("There's Nothing To Print")
