# -*- coding: utf-8 -*-
import re
import string
import time
from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    clinical_type = fields.Selection(
        [('inventory', 'Inventory Product'), ('consultation', 'Consultation'), ('follow_up', 'Follow Up'),
         ('special_follow_up', 'Special Follow Up'),
         ('service', 'Service'), ('session_service', 'Session Service')],
        string="Clinical Type", default='inventory')
    day_from = fields.Integer()
    day_to = fields.Integer()


class AccountMove(models.Model):
    _inherit = 'account.move'

    appointment_id = fields.Many2one('ksc.appointment', string='Appointment', readonly=True,
                                     states={'draft': [('readonly', False)]})
    appointment_name = fields.Char(readonly=True)


class KscRoom(models.Model):
    _name = 'ksc.room'
    _description = 'Ksc Room'

    name = fields.Char(required=True, translate=True)


class KscAppointment(models.Model):
    _name = 'ksc.appointment'
    _inherit = ['portal.mixin', 'mail.thread',
                'mail.activity.mixin', 'ksc.mixin']
    _description = 'Ksc Appointment'

    @api.model
    def _get_service_id(self):
        return False

    @api.model
    def _get_room_domain(self):
        res = []
        return res

    @api.model
    def _get_physician_domain(self):
        res = []
        return res

    @api.model
    def _get_product_domain(self):
        res = []
        return res

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}

    name = fields.Char(string='Appointment Id', readonly=True,
                       copy=False, tracking=True, states=READONLY_STATES)
    patient_id = fields.Many2one('res.partner', domain="[('is_patient','=',True)]", ondelete='restrict',
                                 required=True, index=True, help='Patient Name', states=READONLY_STATES, tracking=True)
    physician_id = fields.Many2one('res.partner', domain=lambda self: self._get_physician_domain(), ondelete='restrict',
                                   string='Physician',
                                   index=True, help='Physician\'s Name', states=READONLY_STATES, tracking=True)
    patient_mobile = fields.Char(related='patient_id.mobile')
    civil_num = fields.Char(related='patient_id.civil', string='Civil')
    image_128 = fields.Binary(
        related='patient_id.image_128', string='Image', readonly=True)
    notes = fields.Text(string='Notes', states=READONLY_STATES)
    invoice_id = fields.Many2one(
        'account.move', string='Invoice', copy=False, ondelete="restrict")
    is_invoiced = fields.Boolean()
    services_invoice_id = fields.Many2one(
        'account.move', string='Services Invoice', copy=False, ondelete="restrict")
    state = fields.Selection([
        ('draft', 'Draft - مسودة'),
        ('confirm', 'Confirm - تم حجز الموعد'),
        ('waiting', 'Waiting - الأنتظار'),
        ('in_consultation', 'In consultation - في الكشف'),
        ('pause', 'Pause - متوقف مؤقت'),
        ('to_invoice', 'To Invoice - فاتورة'),
        ('done', 'Done - تم'),
        ('cancel', 'Cancelled - ألغاء'),
    ], string='State', default='draft', required=True, copy=False, tracking=True)
    appointment_purpose = fields.Selection(
        [('consultation', 'Consultation - كشف'),
         ('follow_up', 'Follow Up - متابعة')],
        string='Appointment Purpose', default='consultation', tracking=True)
    start_date = fields.Datetime(string='Start Date', states=READONLY_STATES, copy=False,
                                 default=lambda self: datetime.now() - timedelta(hours=3))
    end_date = fields.Datetime(string='End Date', states=READONLY_STATES, copy=False,
                               default=lambda self: datetime.now() - timedelta(hours=3, minutes=-20))
    room_id = fields.Many2one('ksc.room', domain=lambda self: self._get_room_domain(), ondelete='cascade',
                              string='Room', help="Appointment Room", states=READONLY_STATES, copy=False)
    cancel_reason = fields.Text(
        string="Cancel Reason", states=READONLY_STATES, copy=False)

    product_id = fields.Many2one('product.product', ondelete='restrict', domain=lambda self: self._get_product_domain(),
                                 string='Service', help="Consultation Services",
                                 default=lambda self: self._get_service_id(), states=READONLY_STATES)
    company_id = fields.Many2one('res.company', ondelete='restrict', states=READONLY_STATES,
                                 string='Hospital', default=lambda self: self.env.user.company_id.id)
    # =============== used for showing pricelist==================
    # diseases_ids = fields.One2many(
    #     'ksc.diseases', 'appointments_id', states=READONLY_STATES)
    diseases_ids = fields.One2many(
        'ksc.diseases.line', 'appointments_id', states=READONLY_STATES)

    differencial_diagnosis = fields.Text(string='Differential Diagnosis', states=READONLY_STATES,
                                         help="The process of weighing the probability of one disease versus that of other diseases possibly accounting for a patient's illness.")
    medical_advice = fields.Text(string='Medical Advice', states=READONLY_STATES,
                                 help="The provision of a formal professional opinion regarding what a specific individual should or should not do to restore or preserve health.")

    follow_up = fields.Boolean()
    special_follow_up = fields.Boolean("Follow Up")

    service_line_ids = fields.One2many('ksc.service.line', 'appointment_id', string='Service Line',
                                       states=READONLY_STATES, copy=False)
    invoice_state = fields.Selection([('paid', 'Paid - تم الدفع'), ('not_paid', 'Not Paid - لم يتم الدفع'), ('partial', 'Partially Paid - دفع جزئي')],
                                     compute="_compute_invoice_state")
    has_credit_note = fields.Selection(
        [('has_credit', 'Has Credit - تحتوي على مرتجع'),
         ('has_no_credit', 'Has No Credit Note - لا تحتوي على مرتجع')],
        compute="_compute_has_credit_note")

    hide_based_on_group = fields.Boolean(
        compute="_compute_hide_based_on_group")
    queue_number = fields.Integer()

    price_list_type = fields.Many2many(
        'product.pricelist', string='Price Lists')

    # ===========================medical history=========================
    heart_disease = fields.Selection(
        related='patient_id.heart_disease',   string='Heart disease - أمراض قلبية')
    bleeding = fields.Selection(
        related='patient_id.bleeding',   string='Bleeding - النزف')
    hypertension = fields.Selection(
        related='patient_id.hypertension',   string='Hypertension - أرتفاع')
    diabetes = fields.Selection(
        related='patient_id.diabetes',   string='Diabetes - السكري')
    asthma = fields.Selection(
        related='patient_id.asthma',   string='Asthma - الربو ')
    thyroid_disease = fields.Selection(
        related='patient_id.thyroid_disease',   string='Thyroid disease - أمراض الغده الدرقية')
    rheumatoid_arthritis = fields.Selection(
        related='patient_id.rheumatoid_arthritis',   string='Rheumatoid arthritis - التهاب مفاصل رثيوي')
    others_diseases = fields.Text(
        related='patient_id.others_diseases', string='Others - أمراض اخرى')

    do_you_take_any_medicine_now = fields.Selection(
        related='patient_id.do_you_take_any_medicine_now',   string='Do you take any medicine now ? هل تأخذ أدويه حاليا؟ ')
    are_you_allergic_to_any_medicine = fields.Selection(related='patient_id.are_you_allergic_to_any_medicine',
                                                        string='Are you allergic to any medicine ? هل لديك حساسيه للأدوية')
    others_drugs = fields.Text(
        related='patient_id.others_drugs', string='Others - أدوية اخرى')
    for_ladies = fields.Selection(
        related='patient_id.for_ladies',   string='For ladies - للسيدات')
    remarks = fields.Text(
        related='patient_id.remarks', string='Remarks - ملاحظات ')
    extra_oral_exam = fields.Text(
        related='patient_id.extra_oral_exam', string='Extra Oral Exam')
    intra_oral_exam = fields.Text(
        related='patient_id.intra_oral_exam', string='Intra Oral Exam')
    x_ray_investigation = fields.Text(
        related='patient_id.x_ray_investigation', string='X-Ray Investigation')
    periaplcal = fields.Text(
        related='patient_id.periaplcal', string='Periaplcal')
    occlusal = fields.Text(
        related='patient_id.occlusal', string='Occlusal')
    b_w = fields.Text(related='patient_id.b_w', string='B.W')
    o_p_g = fields.Text(
        related='patient_id.o_p_g', string='O.P.G')
    other_investigations = fields.Text(
        related='patient_id.other_investigations', string='Other Investigations')
    diagnosis = fields.Text(related='patient_id.diagnosis',
                            string='Diagnosis')
    treatment_procedures = fields.Text(
        related='patient_id.treatment_procedures', string="Treatment Procedures")

    # ===========================medical report=========================
    medical_report = fields.Html(string="Descreption")

    # ===========================special report=========================
    special_report_diagnosis = fields.Text(string="Diagnosis")
    special_report_recommendation = fields.Text(string="Recommendation")
    work_place = fields.Char(string="Work Place")

    def set_values_for_price_list(self):
        price_list_ids = []
        invoice_ids = []
        for rec in self:
            invoice_ids = rec.env['account.move'].search(
                [('appointment_name', '=', rec.name), ('clinic', '=', rec.get_clinic_name())])
            if invoice_ids:
                for pr in invoice_ids:
                    if pr.pricelist_id:
                        price_list_ids.append(pr.pricelist_id.id)
                        rec.price_list_type = [(6, 0, price_list_ids)]
                    else:
                        pass

    def get_queue_number(self):
        # start_of_day = datetime.combine(self.start_date, datetime.time(0,0,0))
        start_of_day = self.start_date.strftime('%m/%d/%Y 00:00:00')

        # end_of_day = datetime.combine(self.start_date, datetime.time(23,59,59))
        end_of_day = self.start_date.strftime('%m/%d/%Y 23:59:59')
        prev_app_id = self.env[f'ksc.{self.get_clinic_name()}.appointment'].search([('start_date', '>=', start_of_day), ('start_date', '<', end_of_day),
                                                                                    ('queue_number', '!=', 0)], order="start_date desc", limit=1)

        app_id = self.env[f'ksc.{self.get_clinic_name()}.appointment'].search(
            [('start_date', '>=', start_of_day), ('start_date', '<', end_of_day), ('queue_number', '=', 0)], order="start_date desc", limit=1)
        # raise UserError(app_id)
        # ('queue_number', '=', 0)
        if app_id:
            if prev_app_id:
                app_id[0].queue_number = prev_app_id[0].queue_number + 1
            else:
                app_id[0].queue_number = 1

    def get_receptionist_clinic_group(self):
        return ""

    @api.depends('create_uid')
    def _compute_hide_based_on_group(self):
        for rec in self:
            if self.env.user.has_group(f'{rec.get_receptionist_clinic_group()}'):
                rec.hide_based_on_group = False
            else:
                rec.hide_based_on_group = True

    read_based_on_nurse_group = fields.Boolean(
        compute="_compute_read_based_on_nurse_group")

    def get_nurse_clinic_group(self):
        return ""

    @api.depends('create_uid')
    def _compute_read_based_on_nurse_group(self):
        for rec in self:
            if self.env.user.has_group(f'{rec.get_nurse_clinic_group()}'):
                rec.read_based_on_nurse_group = False
            else:
                rec.read_based_on_nurse_group = True
    # ===============permission for manager===================

    read_based_on_manager_group = fields.Boolean(
        compute="_compute_read_based_on_manager_group")

    def get_manager_clinic_group(self):
        return ""

    @api.depends('create_uid')
    def _compute_read_based_on_manager_group(self):
        for rec in self:
            if self.env.user.has_group(f'{rec.get_manager_clinic_group()}'):
                rec.read_based_on_manager_group = False
            else:
                rec.read_based_on_manager_group = True

    # ===============notes permission for doctor===================
    read_based_on_doctor_group = fields.Boolean(
        compute="_compute_read_based_on_doctor_group")

    def get_doctor_clinic_group(self):
        return ""

    @api.depends('create_uid')
    def _compute_read_based_on_doctor_group(self):
        for rec in self:
            if self.env.user.has_group(f'{rec.get_doctor_clinic_group()}'):
                rec.read_based_on_doctor_group = False
            else:
                rec.read_based_on_doctor_group = True

    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            if rec.patient_id:
                name = "%s [%s]" % (rec.name, rec.patient_id.name)
            res += [(rec.id, name)]
        return res

    def add_diseases(self):
        for disease in self.diseases_ids:
            disease.patient_id = self.patient_id.id

    def _compute_has_credit_note(self):
        for rec in self:
            invoice_ids = rec.env['account.move'].search(
                [('appointment_name', '=', rec.name), ('clinic', '=', rec.get_clinic_name())])
            has_credit = 0
            if invoice_ids:
                for invoice in invoice_ids:
                    if invoice.move_type == 'out_refund':
                        has_credit += 1
            if has_credit > 0:
                rec.has_credit_note = 'has_credit'
            else:
                rec.has_credit_note = 'has_no_credit'

    def _compute_invoice_state(self):
        for rec in self:
            invoice_ids = rec.env['account.move'].search(
                [('appointment_name', '=', rec.name), ('clinic', '=', rec.get_clinic_name())])
            is_paid = 0
            is_partial = 0
            for invoice in invoice_ids:
                if invoice.payment_state == 'paid' or invoice.payment_state == 'in_payment':
                    is_paid += 1
                elif invoice.payment_state == 'partial':
                    is_partial += 1

            if is_paid > 0 and is_partial == 0:
                rec.invoice_state = 'paid'
            elif is_paid == 0 and is_partial > 0:
                rec.invoice_state = 'partial'
            else:
                rec.invoice_state = 'not_paid'

    def action_create_evaluation(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_clinic_base.action_ksc_patient_evaluation_popup")
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.patient_id.id,
                             'default_physician_id': self.physician_id.id}
        return action

    def unlink(self):
        for data in self:
            if data.state != 'draft':
                raise UserError(
                    _('You can not delete record not in draft state'))
        return super(KscAppointment, self).unlink()

    def appointment_confirm(self):
        if not self.invoice_id:
            raise UserError(_('Invoice is not created yet'))
        self.set_values_for_price_list()
        self.state = 'confirm'

    def appointment_waiting(self):
        self.state = 'waiting'

    def appointment_consultation(self):
        self.state = 'in_consultation'

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    # 'appointments_id': self.id if self.id else False,
                })
        if self.service_line_ids:
            for service in self.service_line_ids:
                if not service.is_invoiced:
                    self.state = 'to_invoice'
                else:
                    self.state = 'done'
                    self.set_values_for_price_list()
        else:
            self.state = 'done'

    def action_pause(self):
        self.state = 'pause'

    def action_start_paused(self):
        self.state = 'in_consultation'

    def appointment_done(self):
        for service in self.service_line_ids:
            if not service.is_invoiced:
                raise UserError(_('Service invoice is not created yet'))
            else:
                self.state = 'done'

    def appointment_cancel(self):
        self.state = 'cancel'

    def action_open_change_physician(self):
        self.state = 'draft'

    def appointment_return_to_inconsultation(self):
        self.state = 'in_consultation'

    def get_clinic_name(self):
        name = self._name.replace('ksc.', '').replace(
            '.appointment', '').replace('.', '_')
        return name

    def create_invoice(self):
        product_id = self.product_id
        product_data = []
        if not product_id:
            raise UserError(_("Please Set Consultation Service first."))
        else:
            if not self.is_invoiced:
                product_data.append({'product_id': product_id})
                self.is_invoiced = True
        for service in self.service_line_ids:
            if not service.is_invoiced:
                product_data.append({
                    'product_id': service.product_id,
                    'quantity': service.qty,
                })
                service.is_invoiced = True
        # self.set_values_for_price_list()

        inv_data = {
            'physician_id': self.physician_id and self.physician_id.id or False,
            'partner_id': self.patient_id.id,
            'clinic': self.get_clinic_name(),
            'appointment_name': self.name,
            # 'physician_name': self.name,
            'room': self.room_id.name,
        }

        if product_data or not self.is_invoiced:
            invoice = self.ksc_create_invoice(
                partner=self.patient_id, product_data=product_data, inv_data=inv_data)
            # invoice.action_post()
            self.invoice_id = invoice.id
            return self.view_invoice()

    def view_invoice(self):
        appointment_invoices = self.env['account.move'].search(
            [('id', '=', self.invoice_id.id)])

        action = self.ksc_action_view_invoice(appointment_invoices)
        action['context'].update({
            'default_partner_id': self.patient_id.id,
            'default_clinic': self.get_clinic_name(),
        })
        return action

    def view_list_invoice(self):
        appointment_invoices = self.env['account.move'].search(
            [('partner_id', '=', self.patient_id.id), ('clinic', '=', self.get_clinic_name()), ('payment_state', 'not in', ['in_payment', 'paid'])])
        action = False
        if appointment_invoices:
            for app in appointment_invoices:
                if app.name == self.name:
                    action = self.ksc_action_view_invoice(app)
                else:
                    action = self.ksc_action_view_invoice(appointment_invoices)
        else:
            raise UserError("There's no invoice yet")
        return action

    # def view_list_invoice(self):
    #     appointment_invoices = self.env['account.move'].search(
    #         [('appointment_name', '=', self.name), ('clinic', '=', self.get_clinic_name())])
    #     action = self.ksc_action_view_invoice(appointment_invoices)
    #     # action['context'].update({
    #     #     'default_partner_id': self.patient_id.id,
    #     #     'default_clinic': self.get_clinic_name(),
    #     # })
    #     return action

    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Follow Up'),
            'res_model': 'ksc.wizard.appointment.followup',
            'view_mode': 'form',
            'context': {'model': self._name, 'rec_id': self.id},
            'target': 'new',
        }

    def action_open_prescription(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_prescription_model.ksc_prescription_mode_ksc")
        action['context'] = {
            'default_patient_id': self.patient_id.id,
            'default_physician_id': self.physician_id.id,
            'default_name_of_appointment': self.get_clinic_name(),
            'default_date': self.start_date,
        }
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_open_radio_request(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_radiology.action_ksc_radiology_consultation")
        action['context'] = {
            'default_patient_id': self.patient_id.id,
            'default_physician_id': self.physician_id.id,
            'default_date': self.start_date,
        }
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action
        # return {
        #     'name': 'Radio Request',
        #     'res_model': 'ksc.radiology.appointment',
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'tree',
        #     # 'view_id': self.env.ref("ksc_radiology.view_ksc_radiology_appointment_form").id,
        #     'view_id': self.env.ref("ksc_radiology.view_ksc_radiology_appointment_tree").id,

        #     'context': {
        #         'default_patient_id': self.patient_id.id,
        #         'default_physician_id': self.physician_id.id,
        #         'default_date': self.start_date,
        #         'default_product_id': self.product_id.id,
        #     },
        #     'target': 'current',
        # }

    # edit="false" sample="1"

    def action_open_lab_request(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_laboratory.hms_action_lab_test_request")
        action['context'] = {
            'default_patient_id': self.patient_id.id,
            'default_physician_id': self.physician_id.id,
            'default_date': self.start_date,
            'default_out_patient': False,

        }
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_open_change_physician(self):
        return {
            'res_model': 'change.physician.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("ksc_clinic_base.change_wizard_view_form").id,
            'context': {
                'default_appointment_name': self.name,
                'default_clinic_name': self.get_clinic_name(),
            },
            'target': 'new',
        }

    def get_available(self):
        return ""

    @api.onchange('special_follow_up', 'start_date', 'appointment_purpose')
    def is_follow_up(self):
        available = self.get_available()
        if self.appointment_purpose == 'follow_up':
            self.product_id = None
            if not self.special_follow_up:
                self.product_id = None
                b = {'domain': {'product_id': [
                    (available, '=', 1), ('clinical_type', '=', 'follow_up')]}}
            if self.patient_id and self.physician_id and self.special_follow_up:
                last_consultation = self.search(
                    [('patient_id.id', '=', self.patient_id.id), ('physician_id.id', '=', self.physician_id.id),
                     ('state', 'not in', ['draft', 'cancel'])],
                    order='start_date desc',
                    limit=1)
                if last_consultation:
                    delta = self.start_date - last_consultation.start_date
                    if last_consultation.state != 'done':
                        self.special_follow_up = False
                        raise UserError(
                            _('Last consultation {} not done'.format(last_consultation.name)))
                    if last_consultation.appointment_purpose == 'consultation':
                        b = {'domain': {'product_id': [(available, '=', 1), ('day_from', '<=', delta.days),
                                                       ('day_to', '>', delta.days),
                                                       ('clinical_type', '=', 'special_follow_up')]}}
                    else:
                        last_invoice_id = last_consultation.invoice_id
                        last_invoice_line_ids = last_invoice_id.invoice_line_ids
                        if last_invoice_id.amount_total == 0:
                            for line in last_invoice_line_ids:
                                if line.discount == 0:
                                    self.appointment_purpose = 'consultation'
                                elif line.discount > 0:
                                    b = {'domain': {'product_id': [(available, '=', 1), ('day_from', '<=', delta.days),
                                                                   ('day_to', '>',
                                                                    delta.days),
                                                                   ('clinical_type', '=', 'special_follow_up')]}}
                        elif last_invoice_id.amount_total > 0:
                            b = {'domain': {'product_id': [(available, '=', 1), ('day_from', '<=', delta.days),
                                                           ('day_to', '>',
                                                            delta.days),
                                                           ('clinical_type', '=', 'special_follow_up')]}}
                else:
                    raise UserError(
                        _('This Patient Has No Appointment With Doctor Before'))
            elif not self.patient_id and not self.physician_id and self.special_follow_up:
                raise UserError(_('Please choose patient or physician'))
        else:
            self.product_id = None
            b = {'domain': {
                'product(_id': [(available, '=', 1), ('clinical_type', '=', 'consultation')]}}
        return b

    def name_of_clinic(self):
        return ""

    def print_report(self):
        clinic_name = self.name_of_clinic()
        payment_ids = self.env['account.payment'].search(
            [("clinic", "=", clinic_name), ("date", "=", fields.Date.today()),
             ('create_uid', '=', self.env.uid)])
        if payment_ids:
            return self.env.ref('ksc_clinic_base.today_payment_action').report_action(payment_ids)
        else:
            raise UserError(_('No payments record!'))


class KSCServiceLine(models.Model):
    _name = "ksc.service.line"
    _inherit = ['ksc.mixin']
    _description = "List of Services"

    name = fields.Char(
        string='Name', default=lambda self: self.product_id.name)
    product_id = fields.Many2one(
        'product.product', ondelete="restrict", string='Service')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
                                  help='Amount of medication (eg, 250 mg) per dose')
    qty = fields.Float(string='Quantity', default=1.0)
    price = fields.Float(string='Price', default=1.0,
                         related='product_id.list_price', readonly=True)
    move_id = fields.Many2one('stock.move', string='Stock Move')
    date = fields.Date("Date", default=fields.Date.context_today)
    appointment_id = fields.Many2one(
        'ksc.appointment', ondelete="cascade", string='Appointment')
    is_invoiced = fields.Boolean()

    def unlink(self):
        if self.is_invoiced:
            raise UserError(_('You can not delete invoiced service!'))
        return super(KSCServiceLine, self).unlink()

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.product_uom = self.product_id.uom_id.id


class KSCDiseases(models.Model):
    _name = 'ksc.diseases'
    _description = "Diseases"

    name = fields.Char(string='Name', required=True,
                       help='Disease name', default="New Disease", index=True)
    ref = fields.Char(string='Disease Id',
                      readonly=True, copy=False, tracking=True)
    appointments_id = fields.Many2one('ksc.appointment')

    @api.model
    def create(self, values):
        if values.get('ref', 'New Disease') == 'New Disease':
            values['ref'] = self.env['ir.sequence'].next_by_code(
                'ksc.diseases') or 'New Disease'
        return super(KSCDiseases, self).create(values)
