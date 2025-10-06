# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from lxml import etree, objectify
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(selection_add=[('dermatology', 'Dermatology')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('dermatology', 'Dermatology')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('dermatology'):
            ids = self.env.company.dermatology_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_dermatology = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_dermatology = fields.Boolean()


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    dermatology_appt_id = fields.Many2one(
        'ksc.dermatology.appointment', ondelete="cascade", string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.dermatology_appt_id:
                rec.patient_id = rec.dermatology_appt_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.dermatology_appt_id:
                rec.clinic_name = rec.dermatology_appt_id.get_clinic_name()


class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"
    _description = "Ksc diseases lines"

    dermatology_appt_id = fields.Many2one(
        'ksc.dermatology.appointment', ondelete="cascade", string='Derma Appointment')


# class KSCDiseases(models.Model):
#     _inherit = 'ksc.diseases'

#     dermatology_appt_id = fields.Many2one('ksc.dermatology.appointment', ondelete="cascade", string='Appointment')


class KscdermatologyAppointment(models.Model):
    _name = 'ksc.dermatology.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc dermatology Appointment'
    _order = "start_date desc"
    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}

    service_line_ids = fields.One2many('dermatology.line', 'appointment_id', string='Service Line',copy=False)
    consultation_service_log_id = fields.Many2one('consultation.service.log')
    # diseases_ids = fields.One2many('ksc.diseases', 'dermatology_appt_id')
    diseases_ids = fields.One2many('ksc.diseases.line', 'dermatology_appt_id')
    clinic_name = fields.Char(default="dermatology")
    before_treatment = fields.Binary()
    after_treatment = fields.Binary()
    zone_treatment = fields.Binary()

    ############ dermatology and venerology ############

    # group_ids = fields.Many2many('res.groups', string="Access Groups", readonly=True,)
    cheif_complaint = fields.Text()
    past_history = fields.Text()
    history = fields.Text()
    other_diseases = fields.Text()
    examination = fields.Text()

    skin = fields.Text()
    mucous = fields.Text()
    investigations = fields.Text()
    diagnosis = fields.Text()
    treatment = fields.Text()

    def get_receptionist_clinic_group(self):
        return "ksc_dermatology.ksc_dermatology_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_dermatology.ksc_dermatology_nurse"

    def get_manager_clinic_group(self):
        return "ksc_dermatology.ksc_dermatology_manager"

    def get_doctor_clinic_group(self):
        return "ksc_dermatology.ksc_dermatology_doctor"

    # def fields_view_get(self,view_id=None,view_type="form",toolbar=False,submenu=False):
    #     res = super(KscdermatologyAppointment,self).fields_view_get(view_id=view_id,view_type=view_type,toolbar=toolbar,submenu=submenu)
    #     if view_type=="form":
    #         doc=etree.XML(res['arch'])
    #         page_name=doc.xpath("//notebook/page[@name='dermatology_and_venerology']")
    #         if page_name:
    #             if self.env.user.has_group('ksc_dermatology.ksc_dermatology_receptionist'):
    #                 self.hide_based_on_group=True
    #             else:
    #                 self.hide_based_on_group=False
    #     return res
    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'dermatology_appt_id': self.id,
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
                })
                service.is_invoiced = True
        inv_data = {
            'physician_id': self.physician_id and self.physician_id.id or False,
            'partner_id': self.patient_id.id,
            'clinic': self.get_clinic_name(),
            'appointment_name': self.name,
        }
        if product_data or not self.is_invoiced:
            invoice = self.ksc_create_invoice(
                partner=self.patient_id, product_data=product_data, inv_data=inv_data)
            invoice.action_post()
            self.invoice_id = invoice.id
            return self.view_invoice()

    def name_of_clinic(self):
        return "dermatology"

    @api.onchange('service_line_ids')
    def end_date_calculate(self):
        minutes = 0
        for service in self.service_line_ids:
            minutes += service.sessions_will_take * service.duration
            self.end_date = self.start_date + relativedelta(minutes=minutes)

    def get_available(self):
        return "avalibel_in_dermatology"

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get('name', 'New Appointment') == 'New Appointment':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'ksc.dermatology.appointment') or 'New Appointment'

        return super(KscdermatologyAppointment, self).create(vals_list)

    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.dermatology_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.dermatology_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.dermatology_consultation_product_id:
            consultation = self.env.user.company_id.dermatology_consultation_product_id.id
        return consultation


class resPartner(models.Model):
    _inherit = 'res.partner'

    consultation_service_log_ids = fields.One2many(
        'consultation.service.log', 'derma_patient_id')


class dermatologyLines(models.Model):
    _name = "dermatology.line"
    _inherit = ['ksc.mixin']
    _description = 'Dermatology Line'

    name = fields.Char(
        string='Name', default=lambda self: self.product_id.name)
    product_id = fields.Many2one('product.product')
    number_of_session = fields.Integer(related='product_id.number_of_session')
    duration = fields.Integer('Duration In Minutes',
                              related='product_id.duration1')
    remaining = fields.Integer(
        compute='_compute_sessions_remaining', store=True)
    sessions_will_take = fields.Integer('Session that will take', default=1)
    sessions_taken = fields.Integer(
        'Session taken', compute="_compute_sessions_remaining", default=0)
    product_price = fields.Float('Price', related="product_id.list_price")
    done = fields.Boolean(default=False)
    done_two = fields.Boolean(default=False)
    invoice_id = fields.Many2one('account.move', readonly=True)
    is_invoiced = fields.Boolean(default=False)
    clinic_name = fields.Char(compute='_compute_clinic_name')
    appointment_id = fields.Many2one(
        'ksc.dermatology.appointment', string='Appointment', ondelete="cascade")
    derma_patient_id = fields.Many2one(
        'res.partner', string='Patient', related='appointment_id.patient_id')

    @api.onchange('product_id', 'number_of_session', 'duration', 'remaining')
    def session_taken(self):
        log = self.env['consultation.service.log']
        for rec in self:
            log_product = log.search(
                [('derma_patient_id', '=', rec.derma_patient_id.id), ('product_id', '=', rec.product_id.id),
                 ('state', '=', 'in_progress')])
            if log_product:
                rec.sessions_taken = log_product.sessions_done
                rec.is_invoiced = log_product.is_invoiced

    @api.constrains("sessions_will_take", "remaining")
    def check_remaining(self):
        for rec in self:
            if rec.sessions_will_take > rec.remaining and rec.done:
                raise ValidationError(
                    _('Session will take must be less than or equal remaining'))

    @api.constrains("sessions_will_take", "number_of_session", "is_invoiced")
    def check_will_take(self):
        for rec in self:
            if rec.sessions_will_take > rec.number_of_session and rec.is_invoiced == False:
                raise ValidationError(
                    _('Session will take must be less than or equal number of session'))

    def _compute_clinic_name(self):
        for rec in self:
            if rec.appointment_id:
                rec.clinic_name = rec.appointment_id.get_clinic_name()

    @api.depends('number_of_session', 'sessions_taken')
    def _compute_sessions_remaining(self):
        for rec in self:
            log = self.env['consultation.service.log']
            log_product_id = log.search(
                [('derma_patient_id', '=', rec.derma_patient_id.id), ('product_id', '=', rec.product_id.id),
                 ('state', '=', 'in_progress')], limit=1)
            log_product = log_product_id.filtered(
                lambda a: a.state == 'in_progress')
            if log_product:
                total_val = 0
                for pro in log_product:
                    total_val += pro.sessions_done
                    rec.is_invoiced = pro.is_invoiced
                rec.sessions_taken = total_val
            remaining = rec.number_of_session - rec.sessions_taken
            if remaining != rec.number_of_session:
                rec.remaining = remaining
                rec.make_record_done()
            else:
                rec.remaining = 1

    def make_record_done(self):
        self.done = True

    def add_sessions_to_log(self):
        self.done_two = True
        log = self.env['consultation.service.log']
        for line in self.appointment_id.service_line_ids:
            log_product = log.search(
                [('derma_patient_id', '=', self.derma_patient_id.id), ('product_id', '=', line.product_id.id),
                 ('state', '=', 'in_progress')])
            if log_product:
                sessions_done = log_product.sessions_done + line.sessions_will_take
                if log_product.number_of_session < sessions_done:
                    new_sessions_done = sessions_done - log_product.number_of_session
                    sessions_done = log_product.number_of_session
                    new_log_product = log.sudo().create({
                        'product_id': line.product_id.id,
                        'sessions_done': new_sessions_done,
                        'derma_patient_id': self.appointment_id.patient_id.id,
                    })
                log_product.sudo().write({
                    'sessions_done': sessions_done,
                })
                self.appointment_id.consultation_service_log_id = log_product.id
            else:
                log_product = log.sudo().create({
                    'product_id': line.product_id.id,
                    'sessions_done': line.sessions_will_take,
                    'derma_patient_id': self.appointment_id.patient_id.id,
                    'is_invoiced': self.is_invoiced,
                })
                self.appointment_id.consultation_service_log_id = log_product.id

    def create_invoice(self):
        inv_data = {
            'clinic': self.clinic_name
        }
        products_data = [{
            'name': self.name,
            'product_id': self.product_id,
            'quantity': 1,
        }]
        invoice = self.ksc_create_invoice(
            partner=self.derma_patient_id, product_data=products_data, inv_data=inv_data)
        self.invoice_id = invoice.id
        invoice.action_post()
        self.is_invoiced = True


class ConsultationServiceLog(models.Model):
    _name = 'consultation.service.log'
    _description = 'Consultation Service Log'

    # product_id = fields.Many2one('product.product', domain=[('is_treatment', '=', True)], required=True)
    product_id = fields.Many2one('product.product', 'Consultation Service')
    number_of_session = fields.Integer(
        'Number of Sessions', related="product_id.number_of_session")
    sessions_done = fields.Integer('Session Done', default=0)
    sessions_remaining = fields.Integer(
        'Sessions Remaining', compute='_compute_sessions_remaining')
    state = fields.Selection([
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='State', store=True, compute='_compute_state', )
    is_invoiced = fields.Boolean(default=False)
    derma_patient_id = fields.Many2one('res.partner')
    appointment_ids = fields.One2many(
        'ksc.dermatology.appointment', 'consultation_service_log_id')

    @api.depends('number_of_session', 'sessions_done', 'sessions_remaining')
    def _compute_state(self):
        for rec in self:
            if rec.sessions_remaining <= 0:
                rec.state = 'done'
            else:
                rec.state = 'in_progress'

    @api.depends('number_of_session', 'sessions_done')
    def _compute_sessions_remaining(self):
        for rec in self:
            rec.sessions_remaining = rec.number_of_session - rec.sessions_done


class DermatologyPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"
    _description = "Patient Wizard"

    def print_dermatology_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.dermatology.appointment'].search(
            domain, order="start_date asc").ids
        # raise UserError(lab_ids)
        if lab_ids:
            return self.env.ref(
                'ksc_dermatology.derma_patient_file_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
