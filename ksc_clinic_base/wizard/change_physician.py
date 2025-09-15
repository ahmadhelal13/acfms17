
from re import T
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChangePhysician(models.TransientModel):
    _name = 'change.physician.wizard'
    _description = 'Change Physician Wizard'

    physician_id = fields.Many2one('res.partner', ondelete='restrict', string='Physician')
    appointment_name = fields.Char()
    clinic_name = fields.Char()


    @api.onchange('clinic_name')
    def _get_physician_domain(self):
        if self.clinic_name == 'dental':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.dental_physician_ids.ids)]}
            }
        elif self.clinic_name == 'dermatology':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.dermatology_physician_ids.ids)]}
            }
        elif self.clinic_name == 'practitioner':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.practitioner_physician_ids.ids)]}
            }
        elif self.clinic_name == 'medicine':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.medicine_physician_ids.ids)]}
            }
        elif self.clinic_name == 'nose_and_ear':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.nose_and_ear_physician_ids.ids)]}
            }
        elif self.clinic_name == 'nutrition':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.nutrition_physician_ids.ids)]}
            }
        elif self.clinic_name == 'obstetrics_and_gynecology':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.obstetrics_and_gynecology_physician_ids.ids)]}
            }
        elif self.clinic_name == 'ophthalmology':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.ophthalmology_physician_ids.ids)]}
            }
        elif self.clinic_name == 'orthopedic':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.orthopedic_physician_ids.ids)]}
            }
        elif self.clinic_name == 'pediatric':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.pediatric_physician_ids.ids)]}
            }
        elif self.clinic_name == 'physiotherapy':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.physiotherapy_physician_ids.ids)]}
            }
        elif self.clinic_name == 'radiology':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.radiology_physician_ids.ids)]}
            }
        elif self.clinic_name == 'urology':
            return {
                'domain': {'physician_id': [('id', 'in', self.env.company.urology_physician_ids.ids)]}
            }

        

    def change_physician(self):
        invoice_ids = self.env['account.move'].search([('appointment_name', '=', self.appointment_name), ('clinic', '=', self.clinic_name)])
        appointment_ids = self.env[f'ksc.{self.clinic_name}.appointment'].search([('name', '=', self.appointment_name)])
        if invoice_ids:
            for invoice in invoice_ids:
                invoice.write({"physician_id" : self.physician_id.id})
        if appointment_ids:
            appointment_ids[0].write({"physician_id" : self.physician_id.id})

class ChangePhysician(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment'

    message = fields.Char(default=_("Are You Want To Cancel Appointment ?"), readonly=True)
    appointment_name = fields.Char()
    clinic_name = fields.Char()

    def confirm_cancel_appointment(self):
        appointment_ids = self.env[f'ksc.{self.clinic_name}.appointment'].search([('name', '=', self.appointment_name)])
        if appointment_ids:
            appointment_ids[0].state = 'cancel'