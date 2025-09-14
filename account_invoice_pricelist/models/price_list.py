# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class priceListInhertancr(models.Model):
    _inherit = "product.pricelist"
    _description = "put percentage field"

    percentage = fields.Integer("Percentage")
    color = fields.Integer()

    @api.constrains("percentage")
    def _precentage_constrain(self):
        for rec in self:
            if rec.percentage > 100:
                raise ValidationError(_('Percentage must be equal or less than 100!'))
