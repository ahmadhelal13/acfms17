# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class PatientLabTestLine(models.Model):
    _name = "laboratory.request.line"
    _description = "Test Lines"

    test_id = fields.Many2one(
        'ksc.lab.test', string='Test', ondelete='cascade', required=True)
    test_state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', readonly=True, compute="_compute_test_state")
    ksc_tat = fields.Char(related='test_id.ksc_tat',
                          string='Turnaround Time', readonly=True)
    instruction = fields.Char(related='test_id.ksc_instruction',
                              string='Special Instructions', readonly=True)
    test_type = fields.Many2one('lab.test.type', readonly=False)
    request_id = fields.Many2one(
        'ksc.laboratory.request', string='Lines', ondelete='cascade')
    sale_price = fields.Float(string='Sale Price')
    company_id = fields.Many2one('res.company', ondelete='restrict',
                                 string='Company', related='request_id.company_id')
    is_invoiced = fields.Boolean()

    def _compute_test_state(self):
        for rec in self:
            test = self.env['patient.laboratory.test'].search(
                [('test_id', '=', rec.test_id.id)], order="create_date desc", limit=1)
            if test:
                rec.test_state = test.state
            else:
                rec.test_state = 'draft'

    @ api.onchange('test_id')
    def onchange_test(self):
        if self.test_id:
            if self.request_id.pricelist_id:
                product_id = self.test_id.product_id.with_context(
                    pricelist=self.request_id.pricelist_id.id)
                self.sale_price = product_id.price
            else:
                self.sale_price = self.test_id.product_id.lst_price

    def prepare_test_result_data(self):
        result_ids = []
        result_ids_2 = []
        result_ids_3 = []
        if self.test_id.structure_selection == "parameter":
            lines = self.test_id.get_line_by_age_and_gender(
                self.request_id.patient_id)
            if lines:
                for line in lines:
                    result_ids.append((0, 0, {
                        'parameter_id': line.id,
                        'name': line.name,
                        'lab_uom_id': line.lab_uom_id.id,
                        'normal_range': line.normal_range,
                        'remark': line.remark,
                    }))
            else:
                UserError("Patient's age must be defined")

        if self.test_id.structure_selection == "customize":
            for line in self.test_id.parameter_ids:
                result_ids.append((0, 0, {
                    'parameter_id': line.id,
                    'name': line.name,
                    'lab_uom_id_2': line.lab_uom_id_2.id,
                    'normal_range_2': line.normal_range_2,
                    'patient_normal_range': line.patient_normal_range,
                    'control_normal_range': line.control_normal_range,
                    'remark': line.remark
                }))

        if self.test_id.has_two_structure:
            lines = self.test_id.get_line_by_age_and_gender_2(
                self.request_id.patient_id)
            if self.test_id.is_hormones:
                for line_2 in lines:
                    result_ids_2.append((0, 0, {
                        'parameter_id': line_2.id,
                        'name': line_2.name,
                        'rs2_lab_uom_id': line_2.pr2_lab_uom_id.id,
                        'rs2_normal_range': line_2.pr_normal_range,
                        'remark': line_2.remark
                    }))
                    # raise UserError(self.result_ids_2.name)
            else:
                for line_2 in self.test_id.parameter_ids_2:
                    result_ids_2.append((0, 0, {
                        'parameter_id': line_2.id,
                        'name': line_2.name,
                        # 'rs2_lab_uom_id': line_2.pr2_lab_uom_id.id,
                        # 'rs2_normal_range': line_2.pr_normal_range,
                        'patient_normal_range_2': line_2.patient_normal_range_2,
                        'control_normal_range_2': line_2.control_normal_range_2,
                        'normal_range_2': line_2.normal_range_2,
                        'remark': line_2.remark
                    }))
        if self.test_id.has_three_structure:
            for line_3 in self.test_id.parameter_ids_3:
                result_ids_3.append((0, 0, {
                    'parameter_id': line_3.id,
                    'name': line_3.name,
                    'normal_range': line_3.normal_range_3,
                    'remark': line_3.remark
                }))
        res = {
            'patient_id': self.request_id.patient_id.id,
            'physician_id': self.request_id.physician_id and self.request_id.physician_id.id,
            'test_id': self.test_id.id,
            'user_id': self.env.user.id,
            'date_analysis': self.request_id.date,
            'request_id': self.request_id.id,
            'specific_gravity_urine_normal_range': self.test_id.specific_gravity_urine_normal_range,
            'ph_urine_normal_range': self.test_id.ph_urine_normal_range,
            'glucose_urine_normal_range': self.test_id.glucose_urine_normal_range,
            'lecucocytes_urine_normal_range': self.test_id.lecucocytes_urine_normal_range,
            'nitrite_urine_normal_range': self.test_id.nitrite_urine_normal_range,
            'protien_urine_normal_range': self.test_id.protien_urine_normal_range,
            'ketones_urine_normal_range': self.test_id.ketones_urine_normal_range,
            'urobilinogen_urine_normal_range': self.test_id.urobilinogen_urine_normal_range,
            'bilirubin_urine_normal_range': self.test_id.bilirubin_urine_normal_range,
            'blood_urine_normal_range': self.test_id.blood_urine_normal_range,
            'glucose_urine_UOM': self.test_id.glucose_urine_UOM,
            'lecucocytes_urine_UOM': self.test_id.lecucocytes_urine_UOM,
            'protien_urine_UOM': self.test_id.protien_urine_UOM,
            'ketones_urine_UOM': self.test_id.ketones_urine_UOM,
            'urobilinogen_urine_UOM': self.test_id.urobilinogen_urine_UOM,
            'bilirubin_urine_UOM': self.test_id.bilirubin_urine_UOM,
            'blood_urine_UOM': self.test_id.blood_urine_UOM,

            'specific_gravity_urine_without_mico_normal_range': self.test_id.specific_gravity_urine_without_mico_normal_range,
            'ph_urine_without_mico_normal_range': self.test_id.ph_urine_without_mico_normal_range,
            'glucose_urine_without_mico_normal_range': self.test_id.glucose_urine_without_mico_normal_range,
            'lecucocytes_urine_without_mico_normal_range': self.test_id.lecucocytes_urine_without_mico_normal_range,
            'nitrite_urine_without_mico_normal_range': self.test_id.nitrite_urine_without_mico_normal_range,
            'protien_urine_without_mico_normal_range': self.test_id.protien_urine_without_mico_normal_range,
            'ketones_urine_without_mico_normal_range': self.test_id.ketones_urine_without_mico_normal_range,
            'urobilinogen_urine_without_mico_normal_range': self.test_id.urobilinogen_urine_without_mico_normal_range,
            'bilirubin_urine_without_mico_normal_range': self.test_id.bilirubin_urine_without_mico_normal_range,
            'blood_urine_without_mico_normal_range': self.test_id.blood_urine_without_mico_normal_range,
            'glucose_urine_UOM_without_mico': self.test_id.glucose_urine_UOM_without_mico,
            'lecucocytes_urine_UOM_without_mico': self.test_id.lecucocytes_urine_UOM_without_mico,
            'protien_urine_UOM_without_mico': self.test_id.protien_urine_UOM_without_mico,
            'ketones_urine_UOM_without_mico': self.test_id.ketones_urine_UOM_without_mico,
            'urobilinogen_urine_UOM_without_mico': self.test_id.urobilinogen_urine_UOM_without_mico,
            'bilirubin_urine_UOM_without_mico': self.test_id.bilirubin_urine_UOM_without_mico,
            'blood_urine_UOM_without_mico': self.test_id.blood_urine_UOM_without_mico,

            'result_ids': result_ids,
            'result_ids_2': result_ids_2,
            'result_ids_3': result_ids_3,
        }
        return res


class LaboratoryRequest(models.Model):
    _name = 'ksc.laboratory.request'
    _description = 'Laboratory Request'
    _inherit = ['portal.mixin', 'mail.thread',
                'mail.activity.mixin', 'ksc.mixin']
    _order = 'date desc, id desc'

    @ api.depends('line_ids')
    def _get_total_price(self):
        self.total_price = sum(line.sale_price for line in self.line_ids)

    STATES = {'requested': [('readonly', True)], 'accepted': [('readonly', True)], 'in_progress': [('readonly', True)],
              'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    name = fields.Char(string='Lab Request ID', readonly=True,
                       index=True, copy=False, tracking=True)
    notes = fields.Text(string='Notes', states=STATES)
    date = fields.Datetime('Date', widget="datetime:format('%d/%m/%Y %I:%M %p')", readonly=True, default=lambda self: fields.Datetime.now(), states=STATES,
                           tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('cancel', 'Cancel'),
        ('done', 'Done')],
        string='State', readonly=True, default='draft', tracking=True)
    patient_id = fields.Many2one('res.partner', domain="[('is_patient','=',True)]", string='Patient', required=True,
                                 ondelete='restrict', states=STATES, tracking=True)
    physician_id = fields.Many2one('res.partner', domain="[('is_physician','=',True)]", string='Prescribing Doctor',
                                   help="Doctor who Request the lab test.", ondelete='restrict', states=STATES,
                                   tracking=True)
    invoice_id = fields.Many2one(
        'account.move', string='Invoice', copy=False, states=STATES)
    lab_bill_id = fields.Many2one(
        'account.move', string='Vendor Bill', copy=False, states=STATES)
    line_ids = fields.One2many('laboratory.request.line', 'request_id',
                               string='Lab Test Line', states=STATES)
    no_invoice = fields.Boolean(string='Invoice Exempt', states=STATES)
    total_price = fields.Float(compute=_get_total_price, string='Total')
    info = fields.Text(string='Extra Info', states=STATES)

    company_id = fields.Many2one('res.company', ondelete='restrict',
                                 string='Hospital', default=lambda self: self.env.user.company_id.id, states=STATES)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', check_company=True,
                                   domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                   help="If you change the pricelist, related invoice will be affected.")
    test_type = fields.Many2one('lab.test.type', states=STATES)
    LABSTATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    other_laboratory = fields.Boolean(string='Referral Lab', states=LABSTATES)
    laboratory_id = fields.Many2one(
        'ksc.laboratory', ondelete='restrict', string='Laboratory', states=LABSTATES)
    sample_ids = fields.One2many(
        'ksc.patient.laboratory.sample', 'request_id', string='Test Samples', states=STATES)
    laboratory_group_id = fields.Many2one('laboratory.group', ondelete="set null", string='Laboratory Group',
                                          states=STATES)
    invoice_state = fields.Selection(
        [('paid', 'Paid'), ('not_paid', 'Not Paid')], compute="_compute_invoice_state")
    has_credit_note = fields.Selection([('has_credit', 'Has Credit'), ('has_no_credit', 'Has No Credit Note')],
                                       compute="_compute_has_credit_note")
    is_invoiced = fields.Boolean()

    out_patient = fields.Boolean(default="True")

    @ api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'ksc.laboratory.request') or 'New'
        result = super(LaboratoryRequest, self).create(vals)
        return result

    # def write(self, vals):
    #     for res in self:
    #         if res.physician_id.user_id.id != res.env.user.id:
    #             raise UserError(
    #                 "You are not allowed to edit a lap request created by another doctor!!")
    #     return super(LaboratoryRequest, self).write(vals)

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
            for invoice in invoice_ids:
                if invoice.payment_state == 'paid' or invoice.payment_state == 'in_payment':
                    is_paid += 1
            if is_paid > 0:
                rec.invoice_state = 'paid'
            else:
                rec.invoice_state = 'not_paid'

    @ api.constrains('line_ids')
    def _check_exist_product_in_line(self):
        for rec in self:
            exist_product_list = []
            for line in rec.line_ids:
                if line.test_id.id in exist_product_list:
                    raise ValidationError(_('Test Is Already Exist!!'))
                exist_product_list.append(line.test_id.id)

    def get_clinic_name(self):
        name = self._name.replace('ksc.', '').replace(
            '.request', '').replace('.', '_')
        return name

    @ api.onchange('laboratory_group_id')
    def onchange_laboratory_group(self):
        test_line_ids = []
        if self.laboratory_group_id:
            for line in self.laboratory_group_id.line_ids:
                test_line_ids.append((0, 0, {
                    'test_id': line.test_id.id,
                    'instruction': line.instruction,
                    'test_type': line.test_type,
                    'sale_price': line.sale_price,
                }))
            self.line_ids = test_line_ids

    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise UserError(
                    _("Lab Requests can be delete only in Draft state."))
        return super(LaboratoryRequest, self).unlink()

    def button_requested(self):
        if not self.line_ids:
            raise UserError(
                _('Please add atleast one Laboratory test line before submiting request.'))
        # self.name = self.env['ir.sequence'].next_by_code('ksc.laboratory.request')
        self.date = fields.Datetime.now()
        self.state = 'requested'

    def button_accept(self):
        if not self.invoice_id:
            raise UserError(_('Invoice is not created yet'))
        Sample = self.env['ksc.patient.laboratory.sample']
        if self.sudo().company_id.ksc_auto_create_lab_sample:
            for line in self.line_ids:
                if line.test_id.sample_type_id:
                    Sample.create({
                        'sample_type_id': line.test_id.sample_type_id.id,
                        'request_id': line.request_id.id,
                        'user_id': self.env.user.id,
                        'company_id': line.request_id.sudo().company_id.id,
                    })
        self.state = 'accepted'

    def button_in_progress(self):
        self.state = 'in_progress'
        LabTest = self.env['patient.laboratory.test']
        for line in self.line_ids:
            vals = line.prepare_test_result_data()
            LabTest.create(vals)

    def button_done(self):
        self.state = 'done'

    def button_cancel(self):
        test_ids = self.env['patient.laboratory.test'].search(
            [('request_id', '=', self.id)])
        if test_ids:
            for test in test_ids:
                test.write({'state': 'cancel'})
        self.state = 'cancel'

    def create_invoice(self):
        if not self.line_ids:
            raise UserError(_("Please add lab Tests first."))
        product_data = []
        for line in self.line_ids:
            if not line.is_invoiced:
                product_data.append({
                    'product_id': line.test_id.product_id,
                    'price_unit': line.sale_price,
                })
                line.is_invoiced
        inv_data = {
            'physician_id': self.physician_id and self.physician_id.id or False,
            'clinic': self.get_clinic_name(),
            'appointment_name': self.name,
            'partner_id': self.patient_id.id,
        }
        pricelist_context = {}
        if self.pricelist_id:
            pricelist_context = {'ksc_pricelist_id': self.pricelist_id.id}

        if product_data:
            invoice = self.ksc_create_invoice(
                partner=self.patient_id, product_data=product_data, inv_data=inv_data)
            self.is_invoiced = True
            # invoice.action_post()
            self.invoice_id = invoice.id
            invoice.request_id = self.id
            return self.view_invoice()

    def create_laboratory_bill(self):
        if not self.line_ids:
            raise UserError(_("Please add lab Tests first."))

        product_data = []
        for line in self.line_ids:
            product_data.append({
                'product_id': line.test_id.product_id,
                'price_unit': line.test_id.product_id.standard_price,
            })

        inv_data = {
            'type': 'in_invoice',
            'physician_id': self.physician_id and self.physician_id.id or False,
            'clinic': self.get_clinic_name(),
        }
        bill = self.ksc_create_invoice(partner=self.laboratory_id.partner_id, product_data=product_data,
                                       inv_data=inv_data)
        bill.action_post()
        self.lab_bill_id = bill.id
        bill.request_id = self.id

    def view_invoice(self):
        invoices = self.mapped('invoice_id')
        action = self.ksc_action_view_invoice(invoices)
        return action

    def action_view_test_results(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_laboratory.action_lab_result")
        action['domain'] = [('request_id', '=', self.id)]
        action['context'] = {'default_request_id': self.id,
                             'default_physician_id': self.physician_id.id}
        return action

    def action_view_lab_samples(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ksc_laboratory.action_ksc_patient_laboratory_sample")
        action['domain'] = [('request_id', '=', self.id)]
        action['context'] = {'default_request_id': self.id}
        return action

    def action_sendmail(self):
        '''
        This function opens a window to compose an email, with the template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference(
                'ksc_laboratory', 'ksc_lab_req_email')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'ksc.laboratory.request',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_barcode_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'barcode.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_request_id': self.id,
            }
        }

    def print_report(self):
        # Method to print sale order report
        payment_ids = self.env['account.payment'].search(
            [("clinic", "=", "laboratory"), ("date", "=", fields.Date.today()),
             ('create_uid', '=', self.env.uid)])
        if payment_ids:
            return self.env.ref('ksc_clinic_base.today_payment_action').report_action(payment_ids)
        else:
            raise UserError(_('No payments record!'))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
