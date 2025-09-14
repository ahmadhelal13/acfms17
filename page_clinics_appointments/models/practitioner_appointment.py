from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.practitioner.appointment"
    _inherit = 'ksc.base.appointment'

    pract_app_id = fields.Many2one('ksc.practitioner.appointment',readonly=True)
   


class InheritlPractitionerApp(models.Model):
    _inherit = 'ksc.practitioner.appointment'

    def consultation_done(self):
        res = super(InheritlPractitionerApp, self).consultation_done()
        self.env['ksc.line.practitioner.appointment'].create({
            'pract_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

