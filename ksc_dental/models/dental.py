# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

# from mock import DEFAULT
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import hashlib
import time


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = "product.product"

    action_perform = fields.Selection([("action", "Action"), ("missing", "Missing"), ("composite", "Composite")], "Action perform", default="action")
    is_medicament = fields.Boolean("Medicament", help="Check if the product is a medicament")
    is_insurance_plan = fields.Boolean("Insurance Plan", help="Check if the product is an insurance plan")
    is_treatment = fields.Boolean("Treatment", help="Check if the product is a Treatment")
    is_planned_visit = fields.Boolean("Planned Visit")
    duration = fields.Selection([("three_months", "Three Months"), ("six_months", "Six Months"), ("one_year", "One Year")], "Duration")

    insurance_company_id = fields.Many2many("res.partner", "treatment_insurance_company_relation", "insurance_company_id", "treatment_id", "Insurance Company")

    def get_treatment_charge(self):
        print("remon")
        return self.lst_price


class TeethCode(models.Model):
    _description = "teeth code"
    _name = "teeth.code"

    name = fields.Char(required=True)
    upper = fields.Boolean()
    lower = fields.Boolean()
    child = fields.Boolean()
    man = fields.Boolean()

    # _sql_constraints = [('uniq_name', 'unique(name)',
    #                      "The name of teeth must be unique !")]


class ProductCategory(models.Model):
    _inherit = "product.category"
    _description = "Product Category"

    treatment = fields.Boolean("Treatment")

    def get_treatment_categs(self):
        all_records = self.search([])
        treatment_list = []
        for each_rec in all_records:
            if each_rec.treatment == True:
                treatment_list.append({"treatment_categ_id": each_rec.id, "name": each_rec.name, "treatments": []})

        product_rec = self.env["product.product"].search([("is_treatment", "=", True)])
        for each_product in product_rec:
            each_template = each_product.product_tmpl_id
            for each_treatment in treatment_list:
                if each_template.categ_id.id == each_treatment["treatment_categ_id"]:
                    each_treatment["treatments"].append({"treatment_id": each_product.id, "treatment_name": each_template.name, "action": each_product.action_perform})
                    break

        return treatment_list


class MedicalTeethTreatment(models.Model):
    _name = "medical.teeth.treatment"
    _description = "Medical Teeth Treatment"
    _order = "date, create_date"

    patient_id = fields.Many2one("res.partner", "Patient Details")
    teeth_id = fields.Many2one("teeth.code", "Tooth")
    description = fields.Many2one("product.product", "Description", domain=[("is_treatment", "=", True)])
    detail_description = fields.Text("Surface")
    state = fields.Selection(
        [("planned", "Planned"), ("condition", "Condition"), ("completed", "Completed"), ("in_progress", "In Progress"), ("invoiced", "Invoiced")], "Status", default="planned"
    )
    total = fields.Float(compute="_compute_total")
    dentist = fields.Many2one("res.partner", "Dentist")
    amount = fields.Float("Amount", related="description.lst_price")
    discount = fields.Float("Discount %")
    note = fields.Text()
    appt_id = fields.Many2one("ksc.dental.appointment", "Appointment ID")
    teeth_code_rel = fields.Many2many("teeth.code", "teeth_code_medical_teeth_treatment_rel", "operation", "teeth")
    invoice_id = fields.Many2one("account.move")
    completed = fields.Boolean()
    child = fields.Boolean()
    dicount_amount = fields.Float(compute="_compute_dicount_amount")

    date = fields.Datetime("date")
    compute_date_create = fields.Datetime(compute="_compute_date_create", string="Create Date")

    @api.depends("date", "create_date")
    def _compute_date_create(self):
        for rec in self:
            rec.compute_date_create = rec.date or rec.create_date

    @api.depends("amount", "discount")
    def _compute_dicount_amount(self):
        for rec in self:
            rec.dicount_amount = rec.amount * (rec.discount / 100)

    def unlink(self):
        for rec in self:
            if rec.state in ("completed", "in_progress") and not self.env.user.has_group("ksc_dental.group_allow_delete_teeth_treatment"):
                raise UserError(_("You cannot remove/deactivate an (In Progress , Completed) record"))
        return super(MedicalTeethTreatment, self).unlink()

    @api.depends("amount", "discount")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.amount - (rec.amount * (rec.discount / 100))


class OrthodonticPlan(models.Model):
    _name = "ksc.ortho.plan"
    _description = "Orthodontic Plan"

    _inherit = "ksc.mixin"

    name = fields.Char("Name", default=lambda self: self.product_id.name)
    patient_id = fields.Many2one("res.partner", domain=[("is_patient", "=", True)])
    physician_id = fields.Many2one("res.partner", domain=[("is_physician", "=", True)], required=True)
    product_id = fields.Many2one("product.product", domain=[("is_treatment", "=", True)], required=True)
    amount = fields.Float("Amount", default=0.0, required=True)
    invoice_id = fields.Many2one("account.move")
    invoiced = fields.Boolean(compute="_compute_invoiced")
    state = fields.Selection(
        related="invoice_id.state",
        readonly=True,
        string="Status",
        store=False,
    )

    @api.depends("invoice_id")
    def _compute_invoiced(self):
        for rec in self:
            rec.invoiced = rec.invoice_id

    def _compute_physician_id(self):
        for rec in self:
            rec.physician_id = self.env.user.partner_id

    def unlink(self):
        for rec in self:
            if rec.invoice_id:
                raise UserError(_("You cannot remove/deactivate an invoiced record"))
        return super(OrthodonticPlan, self).unlink()

    def create_invoice(self):
        products_data = [
            {
                "name": self.name,
                "product_id": self.product_id,
                "quantity": 1,
                "price_unit": self.amount,
            }
        ]
        inv_data = {
            "physician_id": self.physician_id and self.physician_id.id,
            "partner_id": self.patient_id and self.patient_id.id,
        }
        invoice = self.ksc_create_invoice(partner=self.patient_id, product_data=products_data, inv_data=inv_data)
        self.invoice_id = invoice.id

        check_duplicate = self.env["account.move"].search(
            [("partner_id", "=", self.patient_id.id), ("invoice_line_ids.product_id", "=", self.product_id.id), ("state", "=", "draft")]
        )

        for check in check_duplicate:
            if check == self.invoice_id:
                final_duplicte = check_duplicate - check
                for final in final_duplicte:
                    final.unlink()
