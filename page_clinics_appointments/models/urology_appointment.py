from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.urology.appointment"
    _inherit = 'ksc.base.appointment'

    urol_app_id = fields.Many2one('ksc.urology.appointment',readonly=True)


class InheritlUrologyApp(models.Model):
    _inherit = 'ksc.urology.appointment'

    def consultation_done(self):
        res = super(InheritlUrologyApp, self).consultation_done()
        self.env['ksc.line.urology.appointment'].create({
            'urol_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res
