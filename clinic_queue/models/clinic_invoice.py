from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import time,datetime

class ClinicInvoice(models.Model):
    _inherit = 'account.move'

    def print_clinic_reciept(self):
         pass
    
    def print_dental_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.dental.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 
        if invoice_to_print:
                return self.env.ref('clinic_queue.dental_receipet_report_action').report_action(invoice_to_print)  
        else:
            raise UserError("The invoice didn't created yet")


    def print_derma_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.dermatology.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.dermal_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise UserError("The invoice didn't created yet")
        

    def print_general_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.practitioner.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.practitioner_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise UserError("The invoice didn't created yet")
        
    def print_internal_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.medicine.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.medicine_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise UserError("The invoice didn't created yet")


    def print_nose_ear_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.nose_and_ear.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.nose_and_ear_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise UserError("The invoice didn't created yet")
        
    def print_nutrition_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.nutrition.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.nutrition_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise UserError("The invoice didn't created yet")
        
    def print_obs_gyn_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.obstetrics_and_gynecology.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.obstetrics_and_gynecology_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise UserError("The invoice didn't created yet")


    def print_ophthalmology_receipt(self):  
        invoice_ids = []
        invoice_ids = self.env['ksc.ophthalmology.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.ophthalmology_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise UserError("The invoice didn't created yet")   
    
    def print_orthopedic_receipt(self):  
        invoice_ids = []
        invoice_ids = self.env['ksc.orthopedic.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.orthopedic_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise

    def print_pediatric_receipt(self):  
        invoice_ids = []
        invoice_ids = self.env['ksc.pediatric.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.pediatric_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise

    def print_physiotherapy_receipt(self):  
        invoice_ids = []
        invoice_ids = self.env['ksc.physiotherapy.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.physiotherapy_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise
    
    def print_radiology_receipt(self):  
        invoice_ids = []
        invoice_ids = self.env['ksc.radiology.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.radiology_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise

    def print_urolog_receipt(self):  
        invoice_ids = []
        invoice_ids = self.env['ksc.urology.appointment'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 

        if invoice_to_print:
                return self.env.ref('clinic_queue.urology_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise
    
    def print_laboratory_receipt(self):
        invoice_ids = []
        invoice_ids = self.env['ksc.laboratory.request'].search([])
        invoice_to_print=()
        for rec in invoice_ids:
            if rec.invoice_id.id == self.id:
                invoice_to_print = rec 
        if invoice_to_print:
                return self.env.ref('clinic_queue.lab_request_receipet_report_action').report_action(invoice_to_print) 
        else:
            raise
