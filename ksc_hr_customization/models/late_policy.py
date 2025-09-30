from odoo import _, api, fields, models


class LatePolicy(models.Model):
    _name = "late.policy"
    _description = "late policy"

    job_position_id = fields.Many2one("hr.job", string="Job Position")

    late_duration = fields.Selection(
        [("30", "30"), ("60", "60")],
        string="Late Duration In Mins",
    )

    deduction = fields.Selection(
        [("absent", "Absent"), ("present", "Present")],
        string="Deduction",
    )
