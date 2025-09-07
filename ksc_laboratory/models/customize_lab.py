from odoo import api, fields, models

class CustomizeLabTest(models.Model):
    _inherit = "patient.laboratory.test"

    is_urine_routine_without_micorscopy = fields.Boolean(default=False,compute='func_is_urine_routine_without_microscopy_test')

    def func_is_urine_routine_without_microscopy_test(self):
        for rec in self:
            if rec.test_id.has_special_test and rec.test_id.special_test == 'urine_routine_without_microscopy':
                rec.is_urine_routine_without_micorscopy = True
            else:
                rec.is_urine_routine_without_micorscopy = False

