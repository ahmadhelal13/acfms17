from odoo import fields, models, api



class InheritKscBaseApp(models.Model):
    _name = "ksc.line.dermatology.appointment"
    _inherit = 'ksc.base.appointment'

    dermat_app_id = fields.Many2one('ksc.dermatology.appointment',readonly=True)
   


class InheritDermatologyApp(models.Model):
    _inherit = 'ksc.dermatology.appointment'

    def consultation_done(self):
        res = super(InheritDermatologyApp, self).consultation_done()
        self.env['ksc.line.dermatology.appointment'].create({
            'dermat_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

