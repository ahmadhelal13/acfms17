from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, time


class MinistryReportPhysician(models.Model):
    _name = "ministry.report.physician"
    _description = "a model for Ministry Report storage"

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    ministry_report_ids = fields.One2many("ministry.report.line", "ministry_report_physician_id")


class MinistryReportLine(models.Model):
    _name = "ministry.report.line"
    _description = "a model for Ministry Report storage"

    clinic = fields.Char(string="Department/Physician")
    new_kw_m = fields.Integer(string="New Kuwaiti Male")
    new_kw_f = fields.Integer(string="New Kuwaiti Female")
    review_kw_m = fields.Integer(string="Review Kuwaiti Male")
    review_kw_f = fields.Integer(string="Review Kuwaiti Female")
    new_expt_m = fields.Integer(string="New Expat Male")
    new_expt_f = fields.Integer(string="New Expat Female")
    review_expt_m = fields.Integer(string="Review Expat Male")
    review_expt_f = fields.Integer(string="Review Expat Female")
    total = fields.Integer(string="Total")
    ministry_report_physician_id = fields.Many2one("ministry.report.physician")
