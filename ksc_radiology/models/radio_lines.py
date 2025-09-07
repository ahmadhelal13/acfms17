# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class radioLines(models.Model):
    _name = 'radio.lines'
    _description = 'radio type lines'

    name = fields.Char('Name')
    radio_type_id = fields.Many2one(
        'radio.test.type', string='Radio Type', required=True)
    product_id = fields.Many2one('product.product', string='Service', domain='[("avalibel_in_radiology", "=", True)]',
                                 required=True)
