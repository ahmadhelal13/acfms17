from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.pediatric.appointment"
    _description = "Pediatric Appointment"
    _inherit = 'ksc.base.appointment'

    pediat_app_id = fields.Many2one('ksc.pediatric.appointment',readonly=True)
   


class InheritlPediatricApp(models.Model):
    _inherit = 'ksc.pediatric.appointment'
    _description = "Pediatric Appointment Inherit"

    def consultation_done(self):
        res = super(InheritlPediatricApp, self).consultation_done()
        self.env['ksc.line.pediatric.appointment'].create({
            'pediat_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

