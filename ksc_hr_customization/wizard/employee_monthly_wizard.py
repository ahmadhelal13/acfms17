from odoo import api, fields, models
from datetime import datetime, time


class EmployeeMonthlyWizard(models.TransientModel):
    _name = "employee.monthly.wizard"
    _description = "Employee Monthly Wizard"

    employee_id = fields.Many2one("hr.employee", required=True, string="Employee")
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)

    def print_employee_monthly_report(self):
        # Convert from_date and to_date to datetime objects
        from_datetime = datetime.combine(self.from_date, time.min)
        to_datetime = datetime.combine(self.to_date, time.max)

        # Fetch attendance records within the specified date range for the selected employee
        attendance_records = self.env["hr.attendance"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("check_in", ">=", from_datetime),
                ("check_in", "<=", to_datetime),
            ]
        )

        # raise UserWarning(attendance_records)

        if attendance_records:

            # Optionally, you can pass these records to the report if needed
            data = {
                "employee_id": self.employee_id.id,
                "from_date": self.from_date,
                "to_date": self.to_date,
                "attendance_ids": attendance_records.ids,  # Pass the IDs to the report
            }
            attendance_records.write(
                {"from_date": self.from_date, "to_date": self.to_date}
            )

            return self.env.ref(
                "ksc_hr_customization.employee_latness_monthly_report_action"
            ).report_action(attendance_records)
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "No Records Found",
                    "message": "No attendance records found for the specified period.",
                    "type": "warning",
                    "sticky": False,
                },
            }
