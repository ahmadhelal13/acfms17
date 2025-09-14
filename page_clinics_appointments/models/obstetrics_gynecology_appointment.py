from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.obstetrics_and_gynecology.appointment"
    _inherit = 'ksc.base.appointment'

    obs_app_id = fields.Many2one('ksc.obstetrics_and_gynecology.appointment',readonly=True)
   


class InheritlObstetricsGynecologyApp(models.Model):
    _inherit = 'ksc.obstetrics_and_gynecology.appointment'

    def consultation_done(self):
        res = super(InheritlObstetricsGynecologyApp, self).consultation_done()
        self.env['ksc.line.obstetrics_and_gynecology.appointment'].create({
            'obs_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

