from odoo import fields, models, api


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.nutrition.appointment"
    _inherit = 'ksc.base.appointment'

    nut_app_id = fields.Many2one('ksc.nutrition.appointment',readonly=True)
   


class InheritlNutritionApp(models.Model):
    _inherit = 'ksc.nutrition.appointment'

    def consultation_done(self):
        res = super(InheritlNutritionApp, self).consultation_done()
        self.env['ksc.line.nutrition.appointment'].create({
            'nut_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res

