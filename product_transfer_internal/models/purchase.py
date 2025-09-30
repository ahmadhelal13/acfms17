# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Purchase(models.Model):
    _inherit = "purchase.order"

    transfer_req_ids = fields.Many2many(
        "product.transfer.internal", "prod_transfer_purchase_order_rel", "purchase_id", "transfer_id",
        string="Transfer Requests")

    @api.model
    def _prepare_picking(self):
        res = super(Purchase, self.with_context(default_transfer_req_ids=False))._prepare_picking()
        if self.transfer_req_ids:
            origin = res.get('origin', '')
            res.update({
                'origin': ", ".join([origin] + self.transfer_req_ids.mapped('name')),
                'po_transfer_req_ids': [(6, 0, self.transfer_req_ids.ids)],
                'transfer_req_ids': False,
            })
        return res


class PurchaseLine(models.Model):
    _inherit = "purchase.order.line"

    transfer_req_line_ids = fields.Many2many(
        "product.transfer.internal.line", "prod_transfer_line_purchase_order_line_rel", "purchase_line_id", "transfer_line_id",
        string="Transfer Request Lines")

    @api.model
    def create(self, vals):
        record = super(PurchaseLine, self).create(vals)
        if vals.get('transfer_req_line_ids'):
            record.transfer_req_line_ids.action_inprogress()
        return record

    def _prepare_stock_moves(self, picking):
        self.ensure_one()
        res = super(PurchaseLine, self.with_context(default_transfer_req_line_ids=False))._prepare_stock_moves(picking)
        if len(res) > 0:
            res[0].update({
                'po_transfer_req_line_ids': [(6, 0, self.transfer_req_line_ids.ids)],
                'transfer_req_line_ids': False,
            })
        return res
