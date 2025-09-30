from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, time


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
        # Create the main report record
        self.env["ministry.report.physician"].search([]).unlink()
        report = self.env["ministry.report.physician"].create(
            {
                "from_date": self.from_date,
                "to_date": self.to_date,
            }
        )

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
        clinic_display_names = {
        "ksc.dental.appointment": "Dental",
        "ksc.dermatology.appointment": "Dermatology",
        "ksc.practitioner.appointment": "Practitioner",
        "ksc.medicine.appointment": "Medicine",
        "ksc.nose_and_ear.appointment": "Nose and Ear",
        "ksc.nutrition.appointment": "Nutrition",
        "ksc.obstetrics_and_gynecology.appointment": "Obstetrics and Gynecology",
        "ksc.ophthalmology.appointment": "Ophthalmology",
        "ksc.orthopedic.appointment": "Orthopedic",
        "ksc.pediatric.appointment": "Pediatric",
        "ksc.physiotherapy.appointment": "Physiotherapy",
        "ksc.radiology.appointment": "Radiology",
        "ksc.urology.appointment": "Urology",
    }
        # Process data in batches to avoid memory issues
        batch_size = 500
        for clinic_model, clinic_display in clinics.items():
            appointments = self.env[clinic_model].search(domain)
            clinic_display = clinic_display_names.get(clinic_model, clinic_model)
            physicians = appointments.mapped("physician_id")

            for physician in physicians:
                physician_appointments = appointments.filtered(lambda a: a.physician_id == physician)

                counts = {"new_kw_m": 0, "new_kw_f": 0, "review_kw_m": 0, "review_kw_f": 0, "new_expt_m": 0, "new_expt_f": 0, "review_expt_m": 0, "review_expt_f": 0}

                for i in range(0, len(physician_appointments), batch_size):
                    batch = physician_appointments[i : i + batch_size]
                    for appointment in batch:
                        patient = appointment.patient_id
                        is_new = not self.env[clinic_model].search([("patient_id", "=", patient.id), ("start_date", "<", start_datetime), ("state", "=", "done")], limit=1)

                        # Determine category
                        prefix = "new" if is_new else "review"
                        nationality = "kw" if str(patient.nationality).lower() == "kwt" else "expt"
                        gender = "m" if patient.gender == "male" else "f"
                        counts[f"{prefix}_{nationality}_{gender}"] += 1

                # Create report line if data exists
                total = sum(counts.values())
                if total > 0:
                    self.env["ministry.report.line"].create(
                        {
                            "ministry_report_physician_id": report.id,
                            "clinic": f"{clinic_display} ({physician.name})",
                            "new_kw_m": counts["new_kw_m"],
                            "new_kw_f": counts["new_kw_f"],
                            "review_kw_m": counts["review_kw_m"],
                            "review_kw_f": counts["review_kw_f"],
                            "new_expt_m": counts["new_expt_m"],
                            "new_expt_f": counts["new_expt_f"],
                            "review_expt_m": counts["review_expt_m"],
                            "review_expt_f": counts["review_expt_f"],
                            "total": total,
                        }
                    )

        if not report.ministry_report_ids:
            raise UserError(_("No appointments found for the selected date range."))

        # Return PDF report using the stored data
        return self.env.ref("ministry_monthly_report.ministry_phyicians_report_action").report_action(report)
