from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.orthopedic.appointment"
    _description = "Orthopedic Appointment"
    _inherit = 'ksc.base.appointment'

    orth_app_id = fields.Many2one('ksc.orthopedic.appointment',readonly=True)


class InheritlOrthopedicApp(models.Model):
    _inherit = 'ksc.orthopedic.appointment'
    _description = "Orthopedic Appointment Inherit"

    def consultation_done(self):
        res = super(InheritlOrthopedicApp, self).consultation_done()
        self.env['ksc.line.orthopedic.appointment'].create({
            'orth_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res
