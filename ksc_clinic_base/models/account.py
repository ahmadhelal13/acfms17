from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    physician_id = fields.Many2one('res.partner', string='Physician', readonly=True,
                                   states={'draft': [('readonly', False)]})
    clinic = fields.Selection([], readonly=True)
    is_service = fields.Boolean()
    check_credit_note = fields.Selection([('nothing', 'Nothing'), ('has_credit_note', 'Has Credit Note'), (
        'credit_note', 'Credit Note')], compute="_compute_check_credit_note")
    check_discount = fields.Selection(
        [('nothing', 'Nothing'), ('has_discount', 'Has Discount')], compute="_compute_check_discount")
    # physician_name = fields.Char(readonly=True)
    room = fields.Char(readonly=True)

    def _compute_check_credit_note(self):
        for rec in self:
            if rec.move_type == 'out_refund':
                rec.check_credit_note = 'credit_note'
            elif rec.has_credit_note == True:
                rec.check_credit_note = 'has_credit_note'
            else:
                rec.check_credit_note = 'nothing'

    def _compute_check_discount(self):
        for rec in self:
            if rec.invoice_line_ids:
                for invoice_line in rec.invoice_line_ids:
                    if invoice_line.discount > 0:
                        rec.check_discount = 'has_discount'
                    else:
                        rec.check_discount = 'nothing'
            else:
                rec.check_discount = 'nothing'

    def action_register_payment(self):
        action = super(AccountMove, self).action_register_payment()
        action['context']['clinic'] = self.clinic
        action['context']['physician_id'] = self.physician_id.id
        return action


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    _description = 'Register Payment'

    domain_journal_ids = fields.Many2many(
        'account.journal', compute='_compute_domain_journal_ids')

    def _create_payment_vals_from_wizard(self):
        payment_vals = super(AccountPaymentRegister,
                             self)._create_payment_vals_from_wizard()
        if self._context.get('clinic'):
            payment_vals['clinic'] = self._context.get('clinic')
        if self._context.get('physician_id'):
            payment_vals['physician_id'] = self._context.get('physician_id')
        return payment_vals

    @api.depends('amount', 'payment_type', 'journal_id')
    def _compute_domain_journal_ids(self):
        for rec in self:
            rec.domain_journal_ids = rec.get_journal_ids()

    def get_journal_domain(self):
        domain = [('type', 'in', ['bank', 'cash'])]
        if self._context.get('clinic'):
            field = self._context.get('clinic') + '_journal_ids'
            journal_ids = getattr(self.env.company, field)
            if journal_ids:
                domain.append(('id', 'in', journal_ids.ids))
        return domain

    def get_journal_ids(self):
        domain = self.get_journal_domain()
        return self.env['account.journal'].search(domain)


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection([])
    domain_journal_ids = fields.Many2many(
        'account.journal', compute='_compute_domain_journal_ids')
    signed_amount = fields.Monetary(compute='_compute_signed_amount')

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(AccountPayment, self).read_group(
            domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        if 'signed_amount' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(line['__domain'])
                    total_invoice_due = 0.0
                    for record in lines:
                        total_invoice_due += record.signed_amount
                    line['signed_amount'] = total_invoice_due
        return res

    def _compute_signed_amount(self):
        for rec in self:
            if rec.payment_type == "outbound":
                rec.signed_amount = -1 * rec.amount
            elif rec.payment_type == "inbound":
                rec.signed_amount = rec.amount

    @api.depends('amount', 'payment_type', 'journal_id')
    def _compute_domain_journal_ids(self):
        for rec in self:
            rec.domain_journal_ids = rec.get_journal_ids()

    def get_journal_domain(self):
        return [('type', 'in', ['bank', 'cash'])]

    def get_journal_ids(self):
        domain = self.get_journal_domain()
        return self.env['account.journal'].search(domain)

    def print_report(self):
        return True
