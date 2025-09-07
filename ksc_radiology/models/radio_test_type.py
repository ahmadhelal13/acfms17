# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class radioTestType(models.Model):
    _name = 'radio.test.type'
    _description = 'Radio test type'

    name = fields.Char('Name', store=True, required=True)
