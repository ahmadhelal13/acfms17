from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.physiotherapy.appointment"
    _inherit = 'ksc.base.appointment'

    pyths_app_id = fields.Many2one('ksc.physiotherapy.appointment',readonly=True)
   


class InheritlPhysiotherapyApp(models.Model):
    _inherit = 'ksc.physiotherapy.appointment'

    def consultation_done(self):
        res = super(InheritlPhysiotherapyApp, self).consultation_done()
        self.env['ksc.line.physiotherapy.appointment'].create({
            'pyths_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

