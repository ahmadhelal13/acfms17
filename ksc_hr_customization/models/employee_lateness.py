from odoo import _, api, fields, models


class EmployeeLateness(models.Model):
    _inherit = "hr.attendance"

    lateness_duration = fields.Float(
        string="Lateness Duration"
        # string="Lateness Duration", compute="_compute_lateness_duration", store=True
    )

    # @api.depends('employee_id','check_in')
    # def _compute_lateness_duration(self):
    #     # roster_obj =self.env['rec.change'].search([('','=',self.)])
    #     check_in = "08/25/2024 15:40:20"
    #     working_start = "08/25/2024 12:00:00"
    #     working_end = "08/25/2024 21:00:00"
    #     for record in self:
    #         record.lateness_duration = 1
