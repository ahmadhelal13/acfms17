from odoo import _, api, fields, models


class BarcodeWizard(models.TransientModel):
    _name = 'barcode.wizard'
    _description = 'Barcode Wizard'

    request_id = fields.Many2one('ksc.laboratory.request', required=True)
    quantity = fields.Integer(default=1)

    def print(self):
        data = {
            'request_id': self.request_id.id,
            'quantity': self.quantity,
        }
        return self.env.ref('ksc_laboratory.barcodelabels_report').report_action([], data=data)
