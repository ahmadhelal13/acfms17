from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    original_token =fields.Char(string='Original Token',compute="_comppute_original_token",store=True)


    def _comppute_original_token(self):
        for rec in self:
            if rec.openapi_token :
                rec.original_token = rec.openapi_token 
            else:
                rec.original_token=''


    @api.onchange('openapi_token')
    def _onchange_openapi_token(self):
        for rec in self:
            if rec.openapi_token:
                rec.openapi_token = rec.original_token
            else:
                pass