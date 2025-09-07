from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(selection_add=[('dental', 'Dental')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('dental', 'Dental')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('dental'):
            ids = self.env.company.dental_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class KscPatientDiagnosis(models.Model):
    _name = 'ksc.patient.diagnosis'
    _description = 'Patient Diagnosis Notes'
    _rec_name = 'note'

    note = fields.Text()
    patient_id = fields.Many2one('res.partner')


class KscTreatmentPlanDetails(models.Model):
    _name = 'ksc.treatment.plan.details'
    _description = 'Treatment Plan Details'
    _rec_name = 'note'

    note = fields.Text()
    patient_id = fields.Many2one('res.partner')


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'ksc.mixin']

    hide_child_teeth = fields.Boolean()

    teeth_treatment_ids = fields.One2many(
        'medical.teeth.treatment', 'patient_id', 'Operations', readonly=True, tracking=True)
    planned_operation_ids = fields.One2many(
        'medical.teeth.treatment', 'patient_id', compute='_compute_planned_operation_ids', tracking=True)
    in_progress_operation_ids = fields.One2many(
        'medical.teeth.treatment', 'patient_id', compute='_compute_in_progress_operation_ids', tracking=True)
    completed_operation_ids = fields.One2many(
        'medical.teeth.treatment', 'patient_id', compute='_compute_completed_operation_ids', tracking=True)
    diagnosis_ids = fields.One2many(
        'ksc.patient.diagnosis', 'patient_id', tracking=True)
    treatment_plan_details_ids = fields.One2many(
        'ksc.treatment.plan.details', 'patient_id', tracking=True)

    planned_total = fields.Float(
        compute='_compute_planned_total', string='Total')
    ortho_plan_ids = fields.One2many(
        'ksc.ortho.plan', 'patient_id', 'Orthodontic Plan', tracking=True)

    @api.depends('planned_operation_ids')
    def _compute_planned_total(self):
        for rec in self:
            rec.planned_total = sum(self.planned_operation_ids.mapped('total'))

    discount_planned_total = fields.Float(
        compute='_compute_discount_planned_total', string='Discount Total')

    @api.depends('planned_operation_ids')
    def _compute_discount_planned_total(self):
        for rec in self:
            rec.discount_planned_total = sum(
                self.planned_operation_ids.mapped('dicount_amount'))

    amount_planned_total = fields.Float(
        compute='_compute_amount_planned_total', string='Amount Total')

    @api.depends('planned_operation_ids')
    def _compute_amount_planned_total(self):
        for rec in self:
            rec.amount_planned_total = sum(
                self.planned_operation_ids.mapped('amount'))

    @api.depends('teeth_treatment_ids')
    def _compute_planned_operation_ids(self):
        for rec in self:
            rec.planned_operation_ids = rec.teeth_treatment_ids.search(
                [('patient_id', '=', rec.id), ('state', '=', 'planned')])

    @api.depends('teeth_treatment_ids')
    def _compute_in_progress_operation_ids(self):
        for rec in self:
            rec.in_progress_operation_ids = rec.teeth_treatment_ids.search(
                [('patient_id', '=', rec.id), ('state', '=', 'in_progress')])

    @api.depends('teeth_treatment_ids')
    def _compute_completed_operation_ids(self):
        for rec in self:
            rec.completed_operation_ids = rec.teeth_treatment_ids.search(
                [('patient_id', '=', rec.id), ('state', '=', 'completed')])

    def _get_dental_base_url(self):
        return '/dental/web'

    # Methods to open the dental
    def action_dental_client(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self._get_dental_base_url() + '?patient_id=%d' % self.id,
            'target': 'self',
        }

    # ------------

    def get_teeth_id(self, line):
        if line['teeth_id'] not in ['all', '-']:
            return int(line['teeth_id']) + 32 if line['child'] else int(line['teeth_id'])
        return False

    def get_teeth_treatment_fields(self, lines, appt_id):
        vals = []
        for line in lines:
            surface = line['values'][0]['values']
            vals.append({
                'state': line['status_name'],
                'teeth_id': self.get_teeth_id(line),
                'description': int(line['values'][0]['categ_id']),
                'detail_description': " ".join(surface),
                'discount': line['discount'],
                'appt_id': appt_id and int(appt_id),
                'patient_id': self.id,
                'id': int(line['id']) if line['id'] not in ['undefined', ''] else False,
                'child': line['child'],
            })
        return vals

    def create_teeth_treatment(self, vals):
        for val in vals:
            val['date'] = val['create_date'].replace('T', ' ')[:19]
        self.env['medical.teeth.treatment'].create(vals)

    def delete_teeth_treatment(self, ids):
        self.env['medical.teeth.treatment'].browse(ids).unlink()

    def update_teeth_treatment(self, vals):
        treatment_obj = self.env['medical.teeth.treatment']
        for val in vals:
            treatment_obj.browse(val['id']).write(val)

    def get_invoice_line_account(self, type, product):
        accounts = product.product_tmpl_id.get_product_accounts()
        if type in ('out_invoice', 'out_refund'):
            return accounts['income']
        return accounts['expense']

    def try_create_invoice(self):
        lines = self.env['medical.teeth.treatment'].search(
            [('patient_id', '=', self.id), ('state', '=', 'in_progress'), ('invoice_id', '=', None)])
        products_data = []
        for line in lines:
            products_data.append({
                'product_id': line.description,
                'quantity': 1,
                'discount': line.discount,
                'price_unit': line.amount,
            })
        inv_data = {
            'physician_id': self.env.user.partner_id.id,
            'clinic': 'dental',
        }
        if products_data:
            invoice = self.ksc_create_invoice(
                partner=self, product_data=products_data, inv_data=inv_data)
            lines.write({'invoice_id': invoice.id})

    def new_create_lines(self, vals, hide_child_teeth=True):
        new_lines = list(
            filter(lambda dic: 'DentalNewID' in str(dic['id']), vals))
        old_lines = list(
            filter(lambda dic: 'DentalNewID' not in str(dic['id']), vals))
        old_ids = [x['id'] for x in old_lines]
        del_lines = list(filter(lambda id: id not in old_ids,
                         self.teeth_treatment_ids.ids))
        if new_lines:
            self.create_teeth_treatment(new_lines)
        if old_lines:
            self.update_teeth_treatment(old_lines)
        if del_lines:
            self.delete_teeth_treatment(del_lines)
        self.try_create_invoice()
        self.hide_child_teeth = hide_child_teeth
        return True

    def create_lines(self, treatment_lines, patient_id, appt_id, child=False):
        vals = self.get_teeth_treatment_fields(treatment_lines, appt_id)
        new_lines = list(filter(lambda dic: dic['id'] == False, vals))
        old_lines = list(filter(lambda dic: dic['id'] != False, vals))
        old_ids = [x['id'] for x in old_lines]
        teeth_treatment_ids = self.teeth_treatment_ids.filtered(
            lambda self: self.child == child)
        del_lines = list(
            filter(lambda id: id not in old_ids, teeth_treatment_ids.ids))
        if new_lines:
            self.create_teeth_treatment(new_lines)
        if old_lines:
            self.update_teeth_treatment(old_lines)
        if del_lines:
            self.delete_teeth_treatment(del_lines)
        self.try_create_invoice()
        return True

    readonly_based_on_reception_group = fields.Boolean(
        compute="_compute_readonly_based_on_reception_group")

    def get_receptionist_clinic_group(self):
        return "ksc_dental.ksc_dental_receptionist"

    @api.depends('create_uid')
    def _compute_readonly_based_on_reception_group(self):
        for rec in self:
            if self.env.user.has_group(f'{rec.get_receptionist_clinic_group()}'):
                rec.readonly_based_on_reception_group = True
            else:
                rec.readonly_based_on_reception_group = False


class DentalPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_dental_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.dental.appointment'].search(domain).ids
        if lab_ids:
            return self.env.ref(
                'ksc_dental.dental_patient_file_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
