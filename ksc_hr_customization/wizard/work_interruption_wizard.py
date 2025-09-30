from odoo import models, fields, api


class WorkInterruptionWizard(models.TransientModel):
    _name = "work.interruption.wizard"
    _description = "Work Interruption Wizard"

    #  this wizard for Interruption From Work Report

    employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    civil_id = fields.Char(related="employee_id.identification_id", string="Civil ID")
    leave_end_date = fields.Date(string="Leave End Date", required=True)
    interruption_date = fields.Date(string="Interruption Date", required=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    def action_generate_report(self):
        data = {
            "recipient_name": self.employee_id.name,
            "civil_id": self.civil_id,
            "leave_end_date": self.leave_end_date,
            "interruption_date": self.interruption_date,
        }
        return self.env.ref(
            "ksc_hr_customization.interruption_from_work_report_action"
        ).report_action(self)
