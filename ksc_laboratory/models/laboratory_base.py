# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class kscLabTestUom(models.Model):
    _name = "ksc.lab.test.uom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Lab Test UOM"
    _order = 'sequence asc'
    _rec_name = 'code'

    name = fields.Char(string='UOM Name', required=True)
    code = fields.Char(string='Code', required=True, index=True,
                       help="Short name - code for the test UOM")
    sequence = fields.Integer("Sequence", default="100")

    _sql_constraints = [('code_uniq', 'unique (name)',
                         'The Lab Test code must be unique')]


class kscLaboratory(models.Model):
    _name = 'ksc.laboratory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Laboratory'
    _inherit = ['portal.mixin', 'mail.thread',
                'mail.activity.mixin', 'ksc.mixin']
    _inherits = {
        'res.partner': 'partner_id',
    }

    description = fields.Text()
    partner_id = fields.Many2one(
        'res.partner', 'Partner', ondelete='restrict', required=True)


class LabTest(models.Model):
    _name = "ksc.lab.test"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Lab Test Type"

    name = fields.Char(
        string='Name', help="Test type, eg X-Ray, hemogram,biopsy...", index=True)
    active = fields.Boolean(string="Archive", default="1")
    code = fields.Char(string='Code', help="Short name - code for the test")
    description = fields.Text(string='Description')
    product_id = fields.Many2one(
        'product.product', string='Service', required=True)
    company_id = fields.Many2one('res.company', ondelete='restrict', string='Company',
                                 default=lambda self: self.env.user.company_id.id)
    ksc_tat = fields.Char(string='Turnaround Time')
    ksc_instruction = fields.Char(string='Special Instructions')
    test_type = fields.Many2one('lab.test.type')
    sample_type_id = fields.Many2one(
        'ksc.laboratory.sample.type', string='Sample Type')
    # condition one
    parameter_ids = fields.One2many(
        'lab.parameter.line', 'test_id', required=True)
    structure_selection = fields.Selection([('parameter', 'Parameter'),
                                            ('customize', 'Customize')], string="Structure Selection",
                                           default='parameter')
    custom_unit = fields.Boolean(string="Has Unit", default=False)
    custom_reference = fields.Boolean(string="Has Normal Range")
    has_patient_and_control = fields.Boolean(
        'Has Patient And Control Normal Range')
    has_special = fields.Boolean('Has Special Result')
    special_result = fields.Selection(
        [('polar', 'Polar'), ('min_sec', 'Min And Sec'), ('culture_and_growth', 'culture & sensitivity'),
         ('widal', 'Is Widal Test'),
         ('brucella', 'Is Brucella Test'),
         ('brucella_rose', 'Is Brucella Rose Test'), ('rpr',
                                                      'Is RPR Test'), ('inr', 'INR Result'),
         ('malaria', 'Malaria Result'),
         ('gram', 'Gram Stain Result'), ('pregnancy', 'Pregnancy Result'), ('blood_group', 'Blood Group')],
        string='Special Result')
    has_fixed_table = fields.Boolean("Has Fixed Table In Result")
    # condition two
    has_two_structure = fields.Boolean('Has Two Condition')
    parameter_ids_2 = fields.One2many(
        'lab.parameter.line.two', 'test_id', required=True)
    custom_reference_2 = fields.Boolean(string="Has Normal Range")
    has_patient_and_control_2 = fields.Boolean(
        'Has Patient And Control Normal Range')
    has_special_2 = fields.Boolean('Has Special Result')
    special_result_2 = fields.Selection(
        [('polar', 'Polar')], string='Special Result')
    # condition three
    has_three_structure = fields.Boolean('Has Tree Condition')
    parameter_ids_3 = fields.One2many(
        'lab.parameter.line.three', 'test_id', required=True)
    custom_reference_3 = fields.Boolean(string="Has Normal Range")
    has_special_3 = fields.Boolean('Has Special Result')
    special_result_3 = fields.Selection(
        [('min_sec', 'Min And Sec')], string='Special Result')
    # special test
    has_special_test = fields.Boolean('Has Special Test')
    special_test = fields.Selection([('stool_routine', 'STOOL ROUTINE'), ('urine_routine', 'Urine ROUTINE'), ('wet_film', 'Wet Film'),
                                     ('semen_analysis', 'Semen Analysis'), ('urine_routine_without_microscopy', 'Urine ROUTINE Without Micorscopy'), ('mycoplasma', 'Mycoplasma')],
                                    string='Special Test')
    # urine routine normal range
    is_urine_routine_normal_range = fields.Boolean(default=False, store=True)
    specific_gravity_urine_normal_range = fields.Char(
        "Specific Gravity Normal Range")
    ph_urine_normal_range = fields.Char("PH Normal Range")
    glucose_urine_normal_range = fields.Char("Glucose Normal Range")
    lecucocytes_urine_normal_range = fields.Char("Lecucocytes Normal Range")
    nitrite_urine_normal_range = fields.Char("Nitrite Normal Range")
    protien_urine_normal_range = fields.Char("Protien Normal Range")
    ketones_urine_normal_range = fields.Char("Ketones Normal Range")
    urobilinogen_urine_normal_range = fields.Char("Urobilinogen Normal Range")
    bilirubin_urine_normal_range = fields.Char("Bilirubin Normal Range")
    blood_urine_normal_range = fields.Char("Blood Normal Range")
    # UOM of urine routine normal range
    glucose_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM')
    lecucocytes_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM')
    protien_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM')
    ketones_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM')
    urobilinogen_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM')
    bilirubin_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM')
    blood_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM')

    is_celiac_quick_test_2 = fields.Boolean(
        string='Is Celiac Quick Test', default=False, tracking=True)
    is_calprotectin = fields.Boolean(default=False, tracking=True)

    # urine routine without micor normal range
    is_urine_routine_without_micor_normal_range = fields.Boolean(
        default=False, store=True)
    specific_gravity_urine_without_mico_normal_range = fields.Char(
        "Specific Gravity Normal Range")
    ph_urine_without_mico_normal_range = fields.Char("PH Normal Range")
    glucose_urine_without_mico_normal_range = fields.Char(
        "Glucose Normal Range")
    lecucocytes_urine_without_mico_normal_range = fields.Char(
        "Lecucocytes Normal Range")
    nitrite_urine_without_mico_normal_range = fields.Char(
        "Nitrite Normal Range")
    protien_urine_without_mico_normal_range = fields.Char(
        "Protien Normal Range")
    ketones_urine_without_mico_normal_range = fields.Char(
        "Ketones Normal Range")
    urobilinogen_urine_without_mico_normal_range = fields.Char(
        "Urobilinogen Normal Range")
    bilirubin_urine_without_mico_normal_range = fields.Char(
        "Bilirubin Normal Range")
    blood_urine_without_mico_normal_range = fields.Char("Blood Normal Range")
    # UOM of urine routine without micor normal range
    glucose_urine_UOM_without_mico = fields.Many2one(
        'ksc.lab.test.uom', string='UOM')
    lecucocytes_urine_UOM_without_mico = fields.Many2one(
        'ksc.lab.test.uom', string='UOM')
    protien_urine_UOM_without_mico = fields.Many2one(
        'ksc.lab.test.uom', string='UOM')
    ketones_urine_UOM_without_mico = fields.Many2one(
        'ksc.lab.test.uom', string='UOM')
    urobilinogen_urine_UOM_without_mico = fields.Many2one(
        'ksc.lab.test.uom', string='UOM')
    bilirubin_urine_UOM_without_mico = fields.Many2one(
        'ksc.lab.test.uom', string='UOM')
    blood_urine_UOM_without_mico = fields.Many2one(
        'ksc.lab.test.uom', string='UOM')

    # =================new structure for condition 2===================
    is_hormones = fields.Boolean(string='Result For Device 2')

    _sql_constraints = [
        ('code_company_uniq', 'unique (code,company_id)',
         'The code of the account must be unique per company !')
    ]

    @api.onchange("special_test")
    def func_is_urine_routine_normal_range(self):
        for rec in self:
            if rec.special_test == "urine_routine":
                rec.is_urine_routine_normal_range = True
            else:
                rec.is_urine_routine_normal_range = False

    @api.onchange("special_test")
    def func_is_urine_routine_without_micor_normal_range(self):
        for rec in self:
            if rec.special_test == "urine_routine_without_microscopy":
                rec.is_urine_routine_without_micor_normal_range = True
            else:
                rec.is_urine_routine_without_micor_normal_range = False

    def get_line_by_age_and_gender(self, patient_id):
        age = patient_id.days
        gender = patient_id.gender

        line = self.parameter_ids.filtered(
            lambda rec: rec.is_btween(age) and rec.gender == gender and rec.test_id.id == self.id)
        return line if line else False

    def get_line_by_age_and_gender_2(self, patient_id):
        age = patient_id.days
        gender = patient_id.gender
        #
        line = self.parameter_ids_2.filtered(
            lambda rec: rec.is_btween_2(age) and rec.pr2_gender == gender and rec.test_id.id == self.id)
        return line if line else False

    @api.constrains('parameter_ids')
    def _constrains_age(self):
        for rec in self:
            names = []
            for line in rec.parameter_ids:
                if line.name not in names:
                    names.append(line.name)
                    lines = rec.parameter_ids.filtered(
                        lambda x: line.name == x.name)
                    for age in range(1, 1000):
                        record = lines.filtered(
                            lambda x: x.is_btween(age) and x.gender == 'male')
                        if len(record) > 1:
                            raise ValidationError(_('check duplicated!'))
                        record = lines.filtered(
                            lambda x: x.is_btween(age) and x.gender == 'female')
                        if len(record) > 1:
                            raise ValidationError(_('check duplicated!'))

    @api.constrains('parameter_ids_2')
    def _constrains_age_2(self):
        for rec in self:
            names = []
            for line in rec.parameter_ids_2:
                if line.name not in names:
                    names.append(line.name)
                    lines = rec.parameter_ids_2.filtered(
                        lambda x: line.name == x.name)
                    for age in range(1, 1000):
                        record = lines.filtered(lambda x: x.is_btween_2(
                            age) and x.pr2_gender == 'male')
                        if len(record) > 1:
                            raise ValidationError(_('check duplicated!'))
                        record = lines.filtered(lambda x: x.is_btween_2(
                            age) and x.pr2_gender == 'female')
                        if len(record) > 1:
                            raise ValidationError(_('check duplicated!'))

    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            if rec.code:
                name = "%s [%s]" % (rec.name, rec.code)
            res += [(rec.id, name)]
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class PatientLabSample(models.Model):
    _name = "ksc.patient.laboratory.sample"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Patient Laboratory Sample"
    _order = 'date desc, id desc'

    STATES = {'cancel': [('readonly', True)], 'examine': [
        ('readonly', True)], 'collect': [('readonly', True)]}

    name = fields.Char(string='Name', help="Sample Name",
                       readonly=True, copy=False, index=True)
    patient_id = fields.Many2one('res.partner', related="request_id.patient_id", string='Patient', store=True,
                                 readonly=True)
    user_id = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user)
    date = fields.Date(string='Request Date',
                       default=fields.Date.context_today)
    collection_date = fields.Datetime(string='Collection Date')
    examin_date = fields.Datetime(string='Examination Date')
    request_id = fields.Many2one('ksc.laboratory.request', string='Lab Request', ondelete='restrict', required=True)
    company_id = fields.Many2one('res.company', ondelete='restrict',
                                 string='Company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('collect', 'Collected'),
        ('examine', 'Examined'),
        ('cancel', 'Cancel'),
    ], string='State', readonly=True, default='draft', tracking=True)
    sample_type_id = fields.Many2one(
        'ksc.laboratory.sample.type', string='Sample Type', required=True)
    container_name = fields.Char(string='Sample Container Code',
                                 help="If using preprinted sample tube/slide/box no can be updated here.", copy=False,
                                 index=True)

    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('name_company_uniq', 'unique (name,company_id)',
         'Sample Name must be unique per company !')
    ]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'ksc.patient.laboratory.sample')
        return super(PatientLabSample, self).create(vals)

    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise UserError(_("Record can be delete only in Draft state."))
        return super(PatientLabSample, self).unlink()

    @api.onchange('request_id')
    def onchange_request_id(self):
        if self.request_id:
            self.patient_id = self.request_id.patient_id.id

    def action_collect(self):
        self.state = 'collect'
        self.collection_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def action_examine(self):
        self.state = 'examine'
        self.examin_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def action_cancel(self):
        self.state = 'cancel'


class LaboratoryGroupLine(models.Model):
    _name = "laboratory.group.line"
    _description = "Laboratory Group Line"

    group_id = fields.Many2one(
        'laboratory.group', ondelete='restrict', string='Laboratory Group')
    test_id = fields.Many2one(
        'ksc.lab.test', string='Test', ondelete='cascade', required=True)
    test_state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', readonly=True, compute="_compute_test_group_state")
    ksc_tat = fields.Char(related='test_id.ksc_tat',
                          string='Turnaround Time', readonly=True)
    instruction = fields.Char(related='test_id.ksc_instruction',
                              string='Special Instructions', readonly=True)
    sale_price = fields.Float(string='Sale Price')
    test_type = fields.Many2one('lab.test.type')

    @api.onchange('test_id')
    def onchange_test(self):
        if self.test_id:
            self.sale_price = self.test_id.product_id.lst_price

    
    def _compute_test_group_state(self):
        for rec in self:
            test = self.env['patient.laboratory.test'].search(
                [('test_id', '=', rec.test_id.id)], order="create_date desc", limit=1)
            if test:
                rec.test_state = test.state
            else:
                rec.test_state = 'draft'


class LaboratoryGroup(models.Model):
    _name = "laboratory.group"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Laboratory Group"

    name = fields.Char(string='Group Name', required=True)
    line_ids = fields.One2many(
        'laboratory.group.line', 'group_id', string='Medicament line')
    test_type = fields.Many2one('lab.test.type')


class LabSampleType(models.Model):
    _name = "ksc.laboratory.sample.type"
    _description = "Laboratory Sample Type"
    _order = 'sequence asc'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer("Sequence", default="100")
    description = fields.Text("Description")


class LabTestType(models.Model):
    _name = 'lab.test.type'
    _description = 'Lab Test Type'

    name = fields.Char(required=True)
    has_multi_device = fields.Boolean('Has Multiple Device')
    device_1 = fields.Char('Device 1')
    device_2 = fields.Char('Device 2')
