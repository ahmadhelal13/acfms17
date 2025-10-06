# -*- coding: utf-8 -*-
import json
import time
from ast import literal_eval
from collections import defaultdict
from datetime import date
from itertools import groupby
from operator import itemgetter

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_datetime
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.misc import format_date
from odoo.exceptions import ValidationError, UserError


class ProductTransferInternal(models.Model):
    _name = "product.transfer.internal"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Product Internal Transfer"
    _order = "date_order desc"

    source_location = fields.Many2one("stock.location", string="Requester Location", required=True)
    destination_location = fields.Many2one("stock.location", string="Source Location", required=True)

    name = fields.Char(
        string="Transfer Reference",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
        index=True,
        default=lambda self: _("New"),
        track_visibility="onchange",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submit", "Submit"),
            ("stock", "Stock"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
        index=True,
        track_visibility="onchange",
    )

    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.user.company_id)
    description = fields.Text("Description")

    # @api.constrains('source_location')
    # def get_users_source_location(self):
    #     for rec in self:
    #         source_usr = []
    #         for usr in rec.source_location.user_ids:
    #             source_usr.append(usr.name)
    #         if rec.user_id.name not in source_usr:
    #             raise ValidationError(_(" You Not Allowed On This Location "))\

    @api.model
    def _default_user(self):
        return self.env.context.get("user_id", self.env.user.id)

    @api.depends("user_id")
    def default_employee(self):
        employees = self.env["hr.employee"].search([])
        for rec in self:
            for emp in employees:
                if emp.user_id.name == rec.user_id.name:
                    rec.manager_id = emp.parent_id.id

    manager_id = fields.Many2one("hr.employee", string="Manager", store=True, compute="default_employee")

    user_id = fields.Many2one("res.users", default=_default_user, readonly=True)
    date_order = fields.Datetime(string="Order Date", default=fields.Datetime.now, required=True)
    line_ids = fields.One2many("product.transfer.internal.line", "transfer_req_id", string="Product Lines")
    stock_picking_count = fields.Integer(string="Stock Picking Count", compute="_compute_stock_picking_count")
    po_count = fields.Integer(string="Purchase Order Count", compute="_compute_po_count")

    purchase_order_ids = fields.Many2many("purchase.order", "prod_transfer_purchase_order_rel", "transfer_id", "purchase_id", string="Purchase Orders")
    picking_ids = fields.Many2many("stock.picking", "picking_transer_request_rel", "transfer_req_id", "picking_id", string="Pickings")

    def avoid_action(self):
        if self.mapped("line_ids").filtered(lambda line: line.state != "draft"):
            raise ValidationError(_("Action is Not Valid, because some transfer lines are either in progress or completed"))

    def unlink(self):
        self.avoid_action()
        return super(ProductTransferInternal, self).unlink()

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code("product.transfer.internal") or _("New")
        return super(ProductTransferInternal, self).create(vals)

    def action_draft(self):
        self.mapped("line_ids").action_reset()
        return self.write({"state": "draft"})

    def action_submit(self):
        if not self.line_ids:
            raise ValidationError(_("At least one product Required."))
        return self.write({"state": "submit"})

    def action_stock(self):
        if not self.line_ids:
            raise ValidationError(_("At least one product Required."))
        else:
            self.write({"state": "stock"})

    def action_cancel(self):
        # self.mapped("line_ids").action_cancel()
        return self.write({"state": "cancel"})

    def _compute_stock_picking_count(self):
        for rec in self:
            rec.stock_picking_count = len(rec.picking_ids.ids)

    def _compute_po_count(self):
        for rec in self:
            rec.po_count = len(rec.purchase_order_ids.ids)

    def action_see_stock_picking(self):
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        requests = self.mapped("picking_ids")
        if len(requests) > 1:
            action["domain"] = [("id", "in", requests.ids)]
        elif requests:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = requests.id
        return action

    def action_see_purchase_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("RFQ/Purchase Orders"),
            "res_model": "purchase.order",
            "target": "self",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.purchase_order_ids.ids)],
        }

    def _get_action_state(self):
        return "submit"

    transfer_id = fields.Char(store=True)  # Many2one('stock.picking')
    transfer = fields.Many2one("stock.picking", compute="get_transfer")

    @api.depends("transfer_id")
    def get_transfer(self):
        for rec in self:
            if rec.transfer_id:
                picking_type = self.env["stock.picking"].search([("name", "=", rec.transfer_id)], limit=1)
                if picking_type:
                    for p in picking_type:
                        rec.transfer = p.id
                else:
                    rec.transfer = False
            else:
                rec.transfer = False

    # def transfer_button_validate(self):
    #     self.transfer.sudo().button_validate()
    #     raise ValidationError(self.transfer.name)
    # stock_pick_id = self.env['stock.picking'].search([('transfer_req_ids.id','=',self.id)])
    # if stock_pick_id:
    #     stock_pick_id.sudo().action_assign()
    #     stock_pick_id.sudo().button_validate()
    #     raise ValidationError(stock_pick_id.name)
    # return {
    #     'type': 'ir.actions.act_window',
    #     'name': 'Validate',
    #     'res_model': 'stock.picking',
    #     'target': 'self',
    #     'view_mode': 'tree,form',
    #     'domain': [('transfer_req_ids.id','=',self.id)],
    # }

    def action_internal_transfer(self):
        trans_vals = {}
        t_obj = self.env["stock.picking"]
        line_ids = []

        picking_type = self.env["stock.picking.type"].search(
            [("code", "=", "internal"), ("default_location_src_id", "=", self.destination_location.id)], limit=1
        )  # ('barcode', '=', 'HAWLY-INTERNAL')

        if picking_type:
            for rec in self:
                for p in rec.line_ids:
                    # if p.dest_qty > 0:
                    line_ids.append(
                        (
                            0,
                            0,
                            {
                                "product_id": p.product_id.id,
                                "product_uom_qty": p.req_qty,
                                "name": p.product_id.with_context(lang=self.env.user.lang).partner_ref,
                                # 'date_expected': fields.Datetime.now(),
                                "product_uom": p.product_id.uom_id.id,
                                "location_id": self.source_location.id,
                                "location_dest_id": self.destination_location.id,
                                "additional": True,
                                "state": "draft",
                                "transfer_req_line_ids": [p.id],
                            },
                        )
                    )
                    # else:
                    #     raise UserError(_(f"Source: On Hand Of Product '{p.product_id.name}' Quantity Not Available"))
                vals = {
                    "picking_type_id": picking_type.id if picking_type else False,
                    "picking_type_code": "internal",
                    "partner_id": False,
                    "location_id": rec.destination_location.id,
                    "location_dest_id": rec.source_location.id,
                    "move_ids_without_package": line_ids,
                    "note": "Internal Transfer From Request Transfer %s to %s" % (self.destination_location.name, self.source_location.name),
                    "transfer_req_ids": rec.ids,
                    "is_locked": True,
                }
                trans_id = t_obj.create(vals)
                if trans_id:
                    for scp in trans_id:
                        scp.action_assign()
                        scp.button_validate()
                rec.transfer_id = list(vals.values())[9]
                rec.state = "done"
        else:
            raise UserError("The Destination Stock Must Be of Type Internal")

    def action_buy(self):
        transfer_reqs = self.filtered(lambda obj: obj.state == self._get_action_state())
        prd_lines = transfer_reqs.mapped("line_ids").filtered(lambda l: l.order_type == "buy" and l.state == "draft")
        if not prd_lines:
            raise ValidationError(_("There are no lines having 'Buy' type in submitted request(s)"))
        lines = {}
        for rec in prd_lines:
            prod_id = rec.product_id.id
            if lines.get(prod_id):
                lines[prod_id]["product_qty"] += rec.req_qty
                lines[prod_id]["transfer_req_line_ids"] += [rec.id]
            else:
                lines.update(
                    {
                        rec.product_id.id: {
                            "name": rec.product_id.with_context(lang=self.env.user.lang).display_name,
                            "product_id": rec.product_id.id,
                            # 'is_initial_demand_editable': True,
                            "date_planned": datetime.today(),
                            "product_uom": rec.product_id.uom_id.id,
                            "product_qty": rec.req_qty,
                            "transfer_req_line_ids": [rec.id],
                        }
                    }
                )
        all_po_prd = [(5, 0, 0)] + [(0, 0, v) for k, v in lines.items()]
        ctx = dict(self.env.context, default_order_line=all_po_prd, default_transfer_req_ids=transfer_reqs.ids, make_req_inprogress=True)
        return {
            "name": _("New"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "purchase.order",
            "target": "new",
            "context": ctx,
        }


class ProductTransferInternalLine(models.Model):
    _name = "product.transfer.internal.line"
    _description = "Product list for Product Internal Transfer"
    _rec_name = "product_id"

    transfer_req_id = fields.Many2one("product.transfer.internal", string="Transfer", ondelete="cascade", required=True)
    product_id = fields.Many2one("product.product", string="Product", ondelete="restrict", change_default=True, required=True, domain=[("type", "!=", "service")])
    # 'uom.uom'
    product_uom_id = fields.Many2one(related="product_id.uom_id", string="UoM")
    default_code = fields.Char(related="product_id.default_code", readonly=True, string="Ref")
    prod_type = fields.Selection(related="product_id.type", readonly=True)
    qty_available = fields.Float(string="Request: On hand", related="stock_source_quant_id.quantity", readonly=True)  # default=1.0, compute="get_location_quantity")
    dest_qty_available = fields.Float(string="Destination: On hand", default=1.0, readonly=True)
    # product_min_qty = fields.Float(string='Min Qty', readonly=True)
    req_qty = fields.Float(string="Req. Qty", required=True)
    order_type = fields.Selection(
        [
            ("buy", "Buy"),
            ("internal_transfer", "Internal Transfer"),
        ],
        string="Order Type",
        default="internal_transfer",
    )

    state = fields.Selection(
        [("draft", "Draft"), ("inprogress", "In Progress"), ("po_received", "PO Received"), ("done", "Processed"), ("cancel", "Cancelled")], string="State", default="draft"
    )

    def action_inprogress(self):
        return self.write({"state": "inprogress"})

    def action_po_received(self):
        return self.write({"state": "po_received"})

    def action_cancel(self):
        return self.write({"state": "cancel"})

    def action_reset(self):
        return self.write({"state": "draft"})

    location_id = fields.Many2one("stock.location", string="Location", compute="get_location")
    dest_location_id = fields.Many2one("stock.location", default=1.0, string="Dest Location", compute="get_dest_location")
    dest_qty = fields.Float(string="Source: On hand", readonly=True, related="stock_dest_quant_id.quantity")  # , compute='get_dest_location_quantity')

    stock_dest_quant_id = fields.Many2one("stock.quant", compute="get_destination_qty", readonly=False)
    stock_source_quant_id = fields.Many2one("stock.quant", compute="get_source_qty", readonly=False)

    @api.depends("product_id")
    def get_destination_qty(self):
        for rec in self:
            quant_groups = self.env["stock.quant"].search([("location_id", "=", rec.dest_location_id.id), ("product_id", "=", rec.product_id.id)])
            rec.stock_dest_quant_id = quant_groups

    @api.depends("product_id")
    def get_source_qty(self):
        for rec in self:
            quant_groups = self.env["stock.quant"].search([("location_id", "=", rec.location_id.id), ("product_id", "=", rec.product_id.id)])
            rec.stock_source_quant_id = quant_groups

    @api.depends("transfer_req_id.source_location")
    def get_location(self):
        for rec in self:
            rec.location_id = rec.transfer_req_id.source_location.id

    @api.depends("transfer_req_id.destination_location")
    def get_dest_location(self):
        for rec in self:
            rec.dest_location_id = rec.transfer_req_id.destination_location.id

    @api.depends("location_id", "product_id")
    def get_location_quantity(self):
        for rec in self:
            quant_groups = self.env["stock.quant"].search([("location_id", "=", rec.location_id.id)])
            for q in quant_groups:
                if rec.product_id.id == q.product_id.id:
                    rec.qty_available = q.quantity
                else:
                    rec.qty_available = 0

    @api.depends("dest_location_id")
    def get_dest_location_quantity(self):
        for rec in self:
            quant_groups = self.env["stock.quant"].search([("location_id", "=", rec.dest_location_id.id)])
            for q in quant_groups:
                if rec.product_id.id == q.product_id.id:
                    rec.dest_qty = q.quantity
                else:
                    rec.dest_qty = 0

    max = fields.Float("Max Qty", compute="get_limit_quantity")
    min = fields.Float("Min Qty", compute="get_limit_quantity")

    @api.depends("product_id", "location_id")
    def get_limit_quantity(self):
        for rec in self:
            if rec.product_id.product_lines:
                for loc in rec.product_id.product_lines:
                    if loc.max:
                        rec.max = loc.max
                    else:
                        rec.max = 0
                    if loc.min:
                        rec.min = loc.min
                    else:
                        rec.min = 0
            else:
                rec.max = 0
                rec.min = 0

    # @api.constrains('req_qty')
    # def limit_product(self):
    #     for rec in self:
    #         if rec.req_qty > rec.max :
    #             raise ValidationError('Please Request Less Than Max Qty')

    #         if rec.req_qty < rec.min:
    #             raise ValidationError('Please Request More Than Min Qty')


# class picking(models.Model):
#     _inherit = 'stock.picking'

#     def button_validate(self):
#         # Clean-up the context key at validation to avoid forcing the creation of immediate
#         # transfers.
#         # ctx = dict(self.env.context)
#         # ctx.pop('default_immediate_transfer', None)
#         # self = self.with_context(ctx)

#         # Sanity checks.
#         pickings_without_moves = self.browse()
#         pickings_without_quantities = self.browse()
#         pickings_without_lots = self.browse()
#         products_without_lots = self.env['product.product']
#         for picking in self:
#             if not picking.move_lines and not picking.move_line_ids:
#                 pickings_without_moves |= picking

#             picking.message_subscribe([self.env.user.partner_id.id])
#             picking_type = picking.picking_type_id
#             precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#             no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
#             no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in picking.move_line_ids)
#             if no_reserved_quantities and no_quantities_done:
#                 pickings_without_quantities |= picking

#             if picking_type.use_create_lots or picking_type.use_existing_lots:
#                 lines_to_check = picking.move_line_ids
#                 if not no_quantities_done:
#                     lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
#                 for line in lines_to_check:
#                     product = line.product_id
#                     if product and product.tracking != 'none':
#                         if not line.lot_name and not line.lot_id:
#                             pickings_without_lots |= picking
#                             products_without_lots |= product

#         if not self._should_show_transfers():
#             if pickings_without_moves:
#                 raise UserError(_('Please add some items to move.'))
#             if pickings_without_quantities:
#                 raise UserError(self._get_without_quantities_error_message())
#             if pickings_without_lots:
#                 raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(products_without_lots.mapped('display_name')))
#         else:
#             message = ""
#             if pickings_without_moves:
#                 message += _('Transfers %s: Please add some items to move.') % ', '.join(pickings_without_moves.mapped('name'))
#             if pickings_without_quantities:
#                 message += _('\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(pickings_without_quantities.mapped('name'))
#             if pickings_without_lots:
#                 message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (', '.join(pickings_without_lots.mapped('name')), ', '.join(products_without_lots.mapped('display_name')))
#             if message:
#                 raise UserError(message.lstrip())

#         # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
#         # moves and/or the context and never call `_action_done`.
#         if not self.env.context.get('button_validate_picking_ids'):
#             self = self.with_context(button_validate_picking_ids=self.ids)
#         res = self._pre_action_done_hook()
#         if res is not True:
#             return res

#         # Call `_action_done`.
#         if self.env.context.get('picking_ids_not_to_backorder'):
#             pickings_not_to_backorder = self.browse(self.env.context['picking_ids_not_to_backorder'])
#             pickings_to_backorder = self - pickings_not_to_backorder
#         else:
#             pickings_not_to_backorder = self.env['stock.picking']
#             pickings_to_backorder = self
#         pickings_not_to_backorder.with_context(cancel_backorder=True)._action_done()
#         pickings_to_backorder.with_context(cancel_backorder=False)._action_done()
#         return True
