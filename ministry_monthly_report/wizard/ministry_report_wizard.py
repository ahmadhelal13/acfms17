from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, time


class MinistryReportPhysician(models.Model):
    _name = "ministry.report.physician"
    _description = "a model for Ministry Report storage"
    
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    ministry_report_ids = fields.One2many("ministry.report.line", "ministry_report_physician_id")


class MinistryReportLine(models.Model):
    _name = "ministry.report.line"
    _description = "a model for Ministry Report storage"


    clinic = fields.Char(string="Department/Physician")
    new_kw_m = fields.Integer(string="New Kuwaiti Male")
    new_kw_f = fields.Integer(string="New Kuwaiti Female")
    review_kw_m = fields.Integer(string="Review Kuwaiti Male")
    review_kw_f = fields.Integer(string="Review Kuwaiti Female")
    new_expt_m = fields.Integer(string="New Expat Male")
    new_expt_f = fields.Integer(string="New Expat Female")
    review_expt_m = fields.Integer(string="Review Expat Male")
    review_expt_f = fields.Integer(string="Review Expat Female")
    total = fields.Integer(string="Total")
    ministry_report_physician_id = fields.Many2one("ministry.report.physician")


class MinistryReportWizard(models.TransientModel):
    _name = "ministry.report.wizard"
    _description = "Ministry Report Wizard"

    from_date = fields.Date(string="From Date", required=True, default="2025-03-01")
    to_date = fields.Date(string="To Date", required=True, default="2025-03-31")
    def print_report(self):
        start_datetime = datetime.combine(self.from_date, time.min)
        end_datetime = datetime.combine(self.to_date, time.max)
        domain = [
            ("state", "=", "done"),
            ("start_date", ">=", start_datetime),
            ("end_date", "<=", end_datetime),
        ]

        clinics = {
            "ksc.dental.appointment": self.env["ksc.dental.appointment"].search(domain),
            "ksc.dermatology.appointment": self.env["ksc.dermatology.appointment"].search(domain),
            "ksc.practitioner.appointment": self.env["ksc.practitioner.appointment"].search(domain),
            "ksc.medicine.appointment": self.env["ksc.medicine.appointment"].search(domain),
            "ksc.nose_and_ear.appointment": self.env["ksc.nose_and_ear.appointment"].search(domain),
            "ksc.nutrition.appointment": self.env["ksc.nutrition.appointment"].search(domain),
            "ksc.obstetrics_and_gynecology.appointment": self.env["ksc.obstetrics_and_gynecology.appointment"].search(domain),
            "ksc.ophthalmology.appointment": self.env["ksc.ophthalmology.appointment"].search(domain),
            "ksc.orthopedic.appointment": self.env["ksc.orthopedic.appointment"].search(domain),
            "ksc.pediatric.appointment": self.env["ksc.pediatric.appointment"].search(domain),
            "ksc.physiotherapy.appointment": self.env["ksc.physiotherapy.appointment"].search(domain),
            "ksc.radiology.appointment": self.env["ksc.radiology.appointment"].search(domain),
            "ksc.urology.appointment": self.env["ksc.urology.appointment"].search(domain),
        }

        done_appointments = []

        def process_appointments(appointments, clinic_name):
            new_kw_m, new_kw_f, review_kw_m, review_kw_f, new_expt_m, new_expt_f, review_expt_m, review_expt_f = 0, 0, 0, 0, 0, 0, 0, 0
            patients = appointments.mapped("patient_id").filtered(lambda p: p)
            if patients:
                for patient in patients:
                    patient_appointment = self.env[clinic_name].search([("patient_id", "=", patient.id), ("start_date", "<", start_datetime), ("state", "=", "done")], limit=1)

                    if patient_appointment:
                        if str(patient.nationality).lower() == "kwt":
                            if patient.gender == "male":
                                review_kw_m += 1
                            else:
                                review_kw_f += 1
                        else:
                            if patient.gender == "male":
                                review_expt_m += 1
                            else:
                                review_expt_f += 1
                    else:
                        patient_appointments = self.env[clinic_name].search([("patient_id", "=", patient.id)] + domain)
                        if len(patient_appointments) > 1:
                            if str(patient.nationality).lower() == "kwt":
                                if patient.gender == "male":
                                    new_kw_m += 1
                                    review_kw_m += 1
                                else:
                                    new_kw_f += 1
                                    review_kw_f += 1
                            else:
                                if patient.gender == "male":
                                    new_expt_m += 1
                                    review_expt_m += 1
                                else:
                                    new_expt_f += 1
                                    review_expt_f += 1
                        elif len(patient_appointments) == 1:
                            if str(patient.nationality).lower() == "kwt":
                                if patient.gender == "male":
                                    new_kw_m += 1
                                else:
                                    new_kw_f += 1
                            else:
                                if patient.gender == "male":
                                    new_expt_m += 1
                                else:
                                    new_expt_f += 1

            return {
                "clinic": clinic_name.split(".")[1].replace("_", " ").title(),
                "new_kw": {"male": new_kw_m, "female": new_kw_f},
                "review_kw": {"male": review_kw_m, "female": review_kw_f},
                "new_exp": {"male": new_expt_m, "female": new_expt_f},
                "review_exp": {"male": review_expt_m, "female": review_expt_f},
                "total": new_kw_m + new_kw_f + review_kw_m + review_kw_f + new_expt_m + new_expt_f + review_expt_m + review_expt_f,
            }

        for clinic, appointments in clinics.items():
            clinic_data = process_appointments(appointments, clinic)
            done_appointments.append(clinic_data)

        if not any(appointment["total"] > 0 for appointment in done_appointments):
            raise UserError(_("No appointments found for the selected date range."))

        data = {
            "from_date": f"{self.from_date}",
            "to_date": f"{self.to_date}",
            "vals": done_appointments,
        }
        return self.env.ref("ministry_monthly_report.ministry_general_report_action").report_action([], data=data)

    def print_phyician_statistics_report(self):
        start_datetime = datetime.combine(self.from_date, time.min)
        end_datetime = datetime.combine(self.to_date, time.max)
        domain = [
            ("state", "=", "done"),
            ("start_date", ">=", start_datetime),
            ("end_date", "<=", end_datetime),
        ]

        clinics = {
            "ksc.dental.appointment": self.env["ksc.dental.appointment"].search(domain),
            "ksc.dermatology.appointment": self.env["ksc.dermatology.appointment"].search(domain),
            "ksc.practitioner.appointment": self.env["ksc.practitioner.appointment"].search(domain),
            "ksc.medicine.appointment": self.env["ksc.medicine.appointment"].search(domain),
            "ksc.nose_and_ear.appointment": self.env["ksc.nose_and_ear.appointment"].search(domain),
            "ksc.nutrition.appointment": self.env["ksc.nutrition.appointment"].search(domain),
            "ksc.obstetrics_and_gynecology.appointment": self.env["ksc.obstetrics_and_gynecology.appointment"].search(domain),
            "ksc.ophthalmology.appointment": self.env["ksc.ophthalmology.appointment"].search(domain),
            "ksc.orthopedic.appointment": self.env["ksc.orthopedic.appointment"].search(domain),
            "ksc.pediatric.appointment": self.env["ksc.pediatric.appointment"].search(domain),
            "ksc.physiotherapy.appointment": self.env["ksc.physiotherapy.appointment"].search(domain),
            "ksc.radiology.appointment": self.env["ksc.radiology.appointment"].search(domain),
            "ksc.urology.appointment": self.env["ksc.urology.appointment"].search(domain),
        }

        done_appointments = []

        def process_appointments(appointments, clinic_name):
            physician_data = []
            physicians = appointments.mapped("physician_id").filtered(lambda p: p)

            for physician in physicians:
                physician_appointments = appointments.filtered(lambda a: a.physician_id.id == physician.id)

                new_kw_m, new_kw_f, review_kw_m, review_kw_f = 0, 0, 0, 0
                new_expt_m, new_expt_f, review_expt_m, review_expt_f = 0, 0, 0, 0

                for appointment in physician_appointments:
                    patient = appointment.patient_id
                    previous_appointment = self.env[clinic_name].search([
                        ("patient_id", "=", patient.id), 
                        ("start_date", "<", start_datetime), 
                        ("state", "=", "done")
                    ], limit=1)

                    is_kuwaiti = str(patient.nationality).lower() == "kwt"
                    is_male = patient.gender == "male"

                    if previous_appointment:
                        # Review case
                        if is_kuwaiti:
                            if is_male:
                                review_kw_m += 1
                            else:
                                review_kw_f += 1
                        else:
                            if is_male:
                                review_expt_m += 1
                            else:
                                review_expt_f += 1
                    else:
                        # New case
                        if is_kuwaiti:
                            if is_male:
                                new_kw_m += 1
                            else:
                                new_kw_f += 1
                        else:
                            if is_male:
                                new_expt_m += 1
                            else:
                                new_expt_f += 1

                total = new_kw_m + new_kw_f + review_kw_m + review_kw_f + new_expt_m + new_expt_f + review_expt_m + review_expt_f

                if total > 0:
                    physician_data.append({
                        "clinic": clinic_name.split(".")[1].replace("_", " ").title() + f" ({physician.name})",
                        "new_kw": {"male": new_kw_m, "female": new_kw_f},
                        "review_kw": {"male": review_kw_m, "female": review_kw_f},
                        "new_exp": {"male": new_expt_m, "female": new_expt_f},
                        "review_exp": {"male": review_expt_m, "female": review_expt_f},
                        "total": total,
                    })

            return physician_data

        for clinic, appointments in clinics.items():
            clinic_physicians_data = process_appointments(appointments, clinic)
            done_appointments.extend(clinic_physicians_data)

        if not done_appointments:
            raise UserError(_("No appointments found for the selected date range."))

        data = {
            "from_date": f"{self.from_date}",
            "to_date": f"{self.to_date}",
            "vals": done_appointments,
        }
        return self.env.ref("ministry_monthly_report.ministry_phyicians_report_action").report_action([], data=data)
