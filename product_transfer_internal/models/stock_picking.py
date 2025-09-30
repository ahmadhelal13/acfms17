# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    po_transfer_req = fields.Many2one('product.transfer.internal')
    po_transfer_req_ids = fields.Many2many('product.transfer.internal', string="PO Transfer Requests")
    transfer_req_ids = fields.Many2many(
        'product.transfer.internal', 'picking_transer_request_rel', 'picking_id', 'transfer_req_id', string='Transfer Request')

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        active_model = self.env.context.get('active_model')
        if active_model and active_model == 'product.transfer.internal':
            return False
        return super(Picking, self).onchange_picking_type()

    # def action_done(self):
    #     res = super(Picking, self).action_done()
    #     self.exists().mapped('move_lines.po_transfer_req_line_ids').action_po_received()
    #     self.exists().mapped('move_lines.transfer_req_line_ids').action_done()
    #     return res


class StockMove(models.Model):
    _inherit = "stock.move"

    po_transfer_req_line_ids = fields.Many2many("product.transfer.internal.line", "stock_move_product_transfer_internal_line_rel_a", "stock_move_id", "product_transfer_internal_line_id", string="PO Transfer Request Lines")
    transfer_req_line_ids = fields.Many2many("product.transfer.internal.line", "stock_move_product_transfer_internal_line_rel_b", "stock_move_id", "product_transfer_internal_line_id", string="Transfer Request Lines")

    def _action_confirm(self, merge=True, merge_into=False):
        res = super(StockMove, self)._action_confirm(merge=merge, merge_into=merge_into)
        self.exists().mapped("transfer_req_line_ids").filtered(lambda r: r.state == 'draft').action_inprogress()
        return res
