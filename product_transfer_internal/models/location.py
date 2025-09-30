
from datetime import datetime

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class Location(models.Model):
    _inherit = 'stock.location'

    user_ids = fields.Many2many('res.users')

