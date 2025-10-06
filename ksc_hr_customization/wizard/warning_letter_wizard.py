from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class WarningLetterWizard(models.TransientModel):
    _name = 'warning.letter.wizard'
    _description = 'Warning Letter Wizard'
    # this wizard for Warning Latter Report

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    acts = fields.Text(string="Acts", required=True)
    decision = fields.Text(string="Decision", required=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    def generate_warning_letter_report(self):
        data = {
            'employee_id': self.employee_id.id,
            'date': self.date,
            'acts': self.acts,
            'decision': self.decision,
        }
        _logger.info("Generating report with data: %s", data)
        return self.env.ref('ksc_hr_customization.warning_latter_report_action').report_action(self)
