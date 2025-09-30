from odoo import models, fields, api


class DeductionLetterWizard(models.TransientModel):
    _name = "deduction.letter.wizard"
    _description = "Deduction Letter Wizard"
    # this wizard for deduction_latter_report

    employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    date = fields.Date(string="Date", required=True)
    reason = fields.Text(string="Reason", required=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    def action_generate_report(self):
        self.ensure_one()
        return self.env.ref(
            "ksc_hr_customization.deduction_latter_report_action"
        ).report_action(self)
