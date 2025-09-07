
from odoo import api, fields, models, _


class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'

    pdf_link = fields.Char()

    def print_patient_all_reports(self):
        return {
            'name': ("Patient Reports"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'patient.wizard',
            'target': 'new',
            'context': {'default_patient_id': self.id}
        }
