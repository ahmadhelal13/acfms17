from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.medicine.appointment"
    _inherit = 'ksc.base.appointment'

    medic_app_id = fields.Many2one('ksc.medicine.appointment',readonly=True)
   


class InheritlMedicineerApp(models.Model):
    _inherit = 'ksc.medicine.appointment'

    def consultation_done(self):
        res = super(InheritlMedicineerApp, self).consultation_done()
        self.env['ksc.line.medicine.appointment'].create({
            'medic_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

