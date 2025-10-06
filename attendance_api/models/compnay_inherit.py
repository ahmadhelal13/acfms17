# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ResCompanyInh(models.Model):
    _inherit = "res.company"

    face_recog_url = fields.Char(string="Face Recognation Url")
    face_recog_token = fields.Char(string="Face Recognation Token")

    # domain_url_with_port = fields.Char(string="Domain Url with port")
    # db_name = fields.Char(string="Database Name")
    # db_user_name = fields.Char(string="Database User Name")
    # db_user_password = fields.Char(string="Database Password")
