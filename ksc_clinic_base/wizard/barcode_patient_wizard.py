from odoo import _, api, fields, models


class BarcodeWizard(models.TransientModel):
    _name = 'barcode.patient.wizard'
    _description = 'Barcode Wizard'
    
    patient_id = fields.Many2one('res.partner', required=True)
    quantity = fields.Integer(default=1)

    def print(self):
        data = {
            'patient_id': self.patient_id.id,
            'quantity': self.quantity,
        }
        return self.env.ref('ksc_clinic_base.patient_barcodelabels_report').report_action([], data=data)