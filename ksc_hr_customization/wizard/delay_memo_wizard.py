from odoo import models, fields, api
from datetime import datetime

WEEKDAYS = [
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
]


class DelayMemoWizard(models.TransientModel):
    _name = "delay.memo.wizard"
    _description = "Delay Memo Wizard"
    # this wizard for Late Latter Report
    date = fields.Date(string="Date", default=fields.Date.context_today)
    day = fields.Selection(WEEKDAYS, string="Day")
    # weekday = fields.Selection(WEEKDAYS, string="Weekday")
    employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    position = fields.Char(
        string="Position", related="employee_id.job_id.name", store=True
    )
    reason_for_delay = fields.Text(string="Reason for Delay", required=True)
    manager_opinion = fields.Text(string="Direct Manager's Opinion")

    def action_generate_report(self):
        data = {
            "date": self.date,
            "day": self.day,
            "employee_id": self.employee_id.id,
            "position": self.position,
            "reason_for_delay": self.reason_for_delay,
            "manager_opinion": self.manager_opinion,
        }
        return self.env.ref(
            "ksc_hr_customization.late_latter_report_action"
        ).report_action(self)
