from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.nose_and_ear.appointment"
    _inherit = 'ksc.base.appointment'

    nose_ear_app_id = fields.Many2one('ksc.nose_and_ear.appointment',readonly=True)
   


class InheritlNoseEarApp(models.Model):
    _inherit = 'ksc.nose_and_ear.appointment'

    def consultation_done(self):
        res = super(InheritlNoseEarApp, self).consultation_done()
        self.env['ksc.line.nose_and_ear.appointment'].create({
            'nose_ear_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

