from odoo import fields, models, api


class KscBaseAppointmentTest(models.Model):
    _name = "ksc.base.appointment"

    appointment_id = fields.Many2one('ksc.appointment',string="Appointment")
    date = fields.Datetime(string="Date",readonly=True)
    doctor_id = fields.Many2one('res.partner',string="Doctor",readonly=True)
    room_id = fields.Many2one('ksc.room',string="Room",readonly=True)
    patient_id = fields.Many2one('res.partner',string="Patient",readonly=True)


class InheritKscBaseApp(models.Model):
    _name = "ksc.line.dental.appointment"
    _description = "Dental Appointment"
    _inherit = 'ksc.base.appointment'

    dent_app_id = fields.Many2one('ksc.dental.appointment',readonly=True)


class InheritDentalApp(models.Model):
    _inherit = 'ksc.dental.appointment'
    

    def consultation_done(self):
        res = super(InheritDentalApp, self).consultation_done()
        self.env['ksc.line.dental.appointment'].create({
            'dent_app_id': self.id,
            'date': self.start_date,
            'doctor_id': self.physician_id.id,
            'room_id': self.room_id.id,
            'patient_id': self.patient_id.id,
        })
        return res
