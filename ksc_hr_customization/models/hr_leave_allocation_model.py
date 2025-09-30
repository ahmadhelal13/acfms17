from odoo import _, api, fields, models

from odoo.exceptions import UserError


class HrLeaveAllocationInherit(models.Model):
    _inherit = "hr.leave.allocation"

    leaves_taken = fields.Float(readonly=False)

    def update_employee_allocation_monthly(self):
        records = self.search([])
        for rec in records:
            if rec.holiday_status_id and rec.holiday_status_id.is_multi_permsission:
                rec.leaves_taken = 6.0
            else:
                pass


class HrleavetypeInherit(models.Model):
    _inherit = "hr.leave.type"

    is_multi_permsission = fields.Boolean(
        string="اذن بداية الدوام او نتصف او نهاية الدوام"
    )
