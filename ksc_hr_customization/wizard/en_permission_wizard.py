from odoo import models, fields, api
from datetime import datetime
import math

class PermissionWizard(models.TransientModel):
    _name = "permission.wizard"
    _description = "Permission Wizard"

    # this wizard for En - Late or Leave Latter Report

    employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    permission_type = fields.Selection(
        [("late", "تأخير"), ("permission", "استئذان")], required=True
    )

    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    leave_type = fields.Selection(
        [("return", "Return"), ("without_return", "Without Return")]
    )
    time_from = fields.Datetime(string="Time From", required=True)
    time_to = fields.Datetime(string="Time To")
    # hours = fields.Selection(
    #     [("1", "1"), ("2", "2"), ("3", "3"), ("4", "Without Return")],
    #     string="Hours",
    #     readonly=True,
    # )
    hours = fields.Float(
        readonly=True,
    )
    reason = fields.Text(string="Leaving Reason")

    administrator_opinion = fields.Selection(
        [("acceptable", "Acceptable"), ("not_acceptable", "Not Acceptable")],
        string="Administrator Opinion",
        required=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    # employee_signature = fields.Char(string="Employee Signature")
    # administrator_signature = fields.Char(string="Administrator Signature")

    @api.onchange("time_from", "time_to")
    def onchange_time_from_and_time_to(self):
        if self.time_from and self.time_to:
            self.hours = (self.time_to - self.time_from).total_seconds() / 3600
        else:
            self.hours = 0

        # else:
        #     self.hours = 0

    def print_permission_report(self):
        data = {
            "employee_id": self.employee_id.id,
            "date": self.date,
            "time_from": self.time_from,
            "time_to": self.time_to,
            "hours": self.hours,
            "reason": self.reason,
            "administrator_opinion": self.administrator_opinion,
        }
        return self.env.ref(
            "ksc_hr_customization.en_late_leave_request_latter_report_action"
        ).report_action(self)
        # ).report_action(self, data=data)
