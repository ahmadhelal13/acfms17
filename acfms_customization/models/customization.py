# -*- coding: utf-8 -*-
from email.policy import default

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError, ValidationError


class ResCompany(models.Model):
    _inherit = "res.groups"


class civilGender(models.Model):
    _name = "civil.gender"
    _description = "civil gender"

    name = fields.Char()


class ResPartner(models.Model):
    _inherit = "res.partner"

    general_file_no = fields.Char()
    derma_file_no = fields.Char()
    dental_file_no = fields.Char()


class AccountMoveCustom(models.Model):
    _inherit = "account.move"

    has_credit_note = fields.Boolean(default=False)
    total_discount = fields.Float(compute="_compute_total_discount")
    total_amount = fields.Float(compute="_compute_total_discount")
    all_notes = fields.Text(compute="_compute_all_notes")

    def _compute_all_notes(self):
        for rec in self:
            if rec.invoice_line_ids:
                all_notes = """"""
                for line in rec.invoice_line_ids:
                    if line.notes:
                        all_notes += f"({line.notes}) \n"
                if all_notes:
                    rec.all_notes = all_notes
                else:
                    rec.all_notes = ""

    def _compute_total_discount(self):
        for rec in self:
            total_price = 0
            sub_total = 0
            if rec.invoice_line_ids:
                for line in rec.invoice_line_ids:
                    if line.discount:
                        total_price += line.quantity * line.price_unit
                        sub_total += line.price_subtotal
            discount = total_price - sub_total
            rec.total_discount = discount
            rec.total_amount = total_price

    def action_register_payment(self):
        action = super(AccountMoveCustom, self).action_register_payment()
        action["context"]["total_discount"] = self.total_discount
        action["context"]["total_amount"] = self.total_amount
        action["context"]["all_notes"] = self.all_notes
        action["context"]["appointment_name"] = self.appointment_name
        return action

    # def action_reverse(self):
    #     res = super(AccountMoveCustom, self).action_reverse()
    #     self.has_credit_note = True
    #     res['context']['appointment_name'] = self.appointment_name
    #     return res


class AccountPayment(models.Model):
    _inherit = "account.payment"

    total_discount = fields.Float(readonly=True)
    total_amount = fields.Float(readonly=True)
    partial_discount = fields.Float(compute="_compute_partial_discount")
    all_notes = fields.Text(readonly=True)
    appointment_name = fields.Char(readonly=True)
    physician_id = fields.Many2one("res.partner", string="Physician", domain="[('is_physician','=',True)]")

    def _compute_partial_discount(self):
        for rec in self:
            if rec.total_discount > 0 and rec.total_amount > 0:
                par_disc = (rec.amount / (rec.total_amount - rec.total_discount)) * rec.total_discount
                if rec.payment_type == "outbound":
                    rec.partial_discount = -1 * par_disc
                elif rec.payment_type == "inbound":
                    rec.partial_discount = par_disc
            else:
                rec.partial_discount = 0

    # def print_all_report(self):
    #     payment_ids = self.env['account.payment'].search(
    #         [("date", "=", fields.Date.today()), ('create_uid', '=', self.env.uid)],
    #           order="clinic desc, journal_id desc")
    #     if payment_ids:
    #         return self.env.ref('acfms_customization.today_payment_all_clinic_action').report_action(payment_ids)
    #     else:
    #         raise UserError(_('No payments record!'))

    # this fun written by ahmed 2-3-2023
    def print_payment_without_affia(self):
        payment_ids = self.env["account.payment"].search(
            [("date", "=", fields.Date.today()), ("create_uid", "=", self.env.uid), ("journal_id.no_show_in_payment", "=", False)], order="journal_id asc"
        )
        # raise UserError(payment_ids.name)
        if payment_ids:
            return self.env.ref("acfms_customization.today_payment_all_clinic_without_affia_action").report_action(payment_ids)
        else:
            raise UserError(_("No payments record!"))


class AccountPaymentRegisterCustomize(models.TransientModel):
    _inherit = "account.payment.register"

    def _create_payment_vals_from_wizard(self):
        payment_vals = super(AccountPaymentRegisterCustomize, self)._create_payment_vals_from_wizard()
        if self._context.get("total_discount"):
            payment_vals["total_discount"] = self._context.get("total_discount")
        if self._context.get("total_amount"):
            payment_vals["total_amount"] = self._context.get("total_amount")
        if self._context.get("clinic"):
            payment_vals["clinic"] = self._context.get("clinic")
        if self._context.get("all_notes"):
            payment_vals["all_notes"] = self._context.get("all_notes")
        if self._context.get("appointment_name"):
            payment_vals["appointment_name"] = self._context.get("appointment_name")
        if self._context.get("physician_id"):
            payment_vals["physician_id"] = self._context.get("physician_id")
        return payment_vals


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    notes = fields.Char()


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    # @api.model
    def reverse_moves(self):
        if self.move_ids:
            for move in self.move_ids:
                move.has_credit_note = True
        res = super(AccountMoveReversal, self).reverse_moves()
        return res


class MyJournal(models.Model):
    _inherit = "account.journal"

    is_knet = fields.Boolean(string="Is Knet")
    no_show_in_payment = fields.Boolean(string="Do Not Show In Payment")
