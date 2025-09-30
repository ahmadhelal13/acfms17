
from odoo import fields,models,api

class ProductConf(models.Model):
    _name = 'product.conf'

    location_id = fields.Many2one('stock.location')
    max = fields.Float('Max Qty')
    min = fields.Float('Min Qty')
    transfer_id = fields.Many2one('product.template')


class PRoducts(models.Model):
    _inherit = 'product.template'

    product_lines = fields.One2many('product.conf', 'transfer_id')