from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class LabParameter(models.Model):
    _name = "lab.parameter"
    _description = "Lab Parameter"

    name = fields.Char(required=True)
    test_type = fields.Many2one(
        "lab.test.type", string="Test Type", required=True)
    structure_selection = fields.Selection([('parameter', 'Parameter'),
                                            ('customize', 'Customize')], default="parameter")
    is_parameter = fields.Boolean(
        string="Is Parameter", compute="_compute_test_type")
    is_customize = fields.Boolean(
        string="Is Customize", compute="_compute_test_type")
    custom_unit = fields.Boolean(string="Has Unit", store="True")
    custom_reference = fields.Boolean(string="Has Normal Range")
    custom_polar = fields.Boolean(string="Has Polar", store="True")
    custom_time = fields.Boolean(
        string="Has Min And Sec In Result", store="True")
    lab_uom_id = fields.Many2one('ksc.lab.test.uom', string='UOM')

    @api.onchange('structure_selection')
    def _compute_test_type(self):
        if self.structure_selection == "parameter":
            self.is_parameter = True
            self.is_customize = False
        elif self.structure_selection == "customize":
            self.is_customize = True
            self.is_parameter = False

    def get_line_by_age_and_gender(self, patient_id):
        age = patient_id.days
        gender = patient_id.gender
        line = self.line_ids.filtered(
            lambda line: line.is_btween(age) and line.gender == gender)
        # raise UserWarning(line)
        return line[0] if line else False

    @api.constrains('line_ids')
    def _constrains_age(self):
        for rec in self:
            for age in range(1, 1000):
                line = self.line_ids.filtered(
                    lambda line: line.is_btween(age) and line.gender == 'male')
                if len(line) > 1:
                    raise ValidationError(_('check duplicated!'))
                line = self.line_ids.filtered(
                    lambda line: line.is_btween(age) and line.gender == 'female')
                if len(line) > 1:
                    raise ValidationError(_('check duplicated!'))


class LabParameterLine(models.Model):
    _name = "lab.parameter.line"
    _description = "Lab Parameter Line"
    _rec_name = 'gender'

    name = fields.Char('Name')
    sequence = fields.Integer("Sequence", default="1")
    gender = fields.Selection(
        [('male', "male"), ('female', "female")], default='male', required=True)
    lab_uom_id = fields.Many2one('ksc.lab.test.uom', string='UOM')
    lab_uom_id_2 = fields.Many2one('ksc.lab.test.uom', string='UOM')
    normal_range = fields.Text(string="Reference")
    normal_range_2 = fields.Text(string="Reference")
    from_age = fields.Integer(string="From")
    from_by_day = fields.Float(compute='_compute_from_by_day')
    to_by_day = fields.Float(compute='_compute_to_by_day')
    to_age = fields.Integer(string="To")
    age_type = fields.Selection([
        ('year', 'year'),
        ('month', 'month'),
        ('day', 'day'),
    ], string="Age Type")
    patient_normal_range = fields.Char('Patient Normal Range')
    control_normal_range = fields.Char('Control Normal Range')
    test_id = fields.Many2one('ksc.lab.test', ondelete='cascade')
    # test_type_id = fields.Char(comput="_get_lab_type",strore=False)
    test_type = fields.Char()
    remark = fields.Char('Remark')

    # def _get_lab_type(self):

    #     for rec in self:
    #         if rec.test_id:
    #             rec.test_type_id=rec.test_id.test_type
    #             rec.test_type= rec.test_type_id.name
    #         else:
    #             rec.test_type=""

    @api.depends('from_age', 'to_age', 'age_type')
    def _compute_to_by_day(self):
        for rec in self:
            to_by_day = 0
            if rec.test_id:
                rec.test_type = rec.test_id.test_type.name
            if rec.to_age and rec.age_type:
                if rec.age_type == 'day':
                    to_by_day = rec.to_age
                elif rec.age_type == 'month':
                    to_by_day = rec.to_age * 30.33333
                elif rec.age_type == 'year':
                    to_by_day = (rec.to_age * 365) + 364
            rec.to_by_day = to_by_day

    @api.depends('from_age', 'to_age', 'age_type')
    def _compute_from_by_day(self):
        for rec in self:
            from_by_day = 0
            if rec.from_age and rec.age_type:
                if rec.age_type == 'day':
                    from_by_day = rec.from_age
                elif rec.age_type == 'month':
                    from_by_day = rec.from_age * 30.33333
                elif rec.age_type == 'year':
                    from_by_day = rec.from_age * 365
            rec.from_by_day = from_by_day

    @api.constrains('from_age', 'to_age', 'age_type')
    def _constrains_age(self):
        for rec in self:
            if rec.age_type == 'year' and (rec.from_age == 0 or rec.to_age == 0):
                raise ValidationError(_('year must be not equal zero!'))
            if rec.age_type == 'month' and (rec.from_age <= 0 or rec.to_age > 12):
                raise ValidationError(
                    _('month must be less than 12 and bigest than 0!'))
            if rec.age_type == 'day' and (rec.from_age <= 0 or rec.to_age > 30):
                raise ValidationError(
                    _('day must be less than 30 and bigest than 0!'))
            if rec.from_age > rec.to_age:
                raise ValidationError(_('the to must be less than from!'))

    def is_btween(self, age):
        return age >= self.from_by_day and age <= self.to_by_day


class LabParameterLine2(models.Model):
    _name = "lab.parameter.line.two"
    _description = "Lab Parameter Line Two"

    name = fields.Char('Name')
    patient_normal_range_2 = fields.Char('Patient Normal Range')
    control_normal_range_2 = fields.Char('Control Normal Range')
    normal_range_2 = fields.Char("Reference")
    test_id = fields.Many2one('ksc.lab.test', ondelete='cascade')
    remark = fields.Char('Remark')
    test_type = fields.Char()

    pr_normal_range = fields.Text(string="Reference")
    sequence = fields.Integer("Sequence", default="1")
    pr2_gender = fields.Selection(
        [('male', "male"), ('female', "female")], default='male', string="Gender", required=True)
    pr2_lab_uom_id = fields.Many2one('ksc.lab.test.uom', string='UOM')
    pr2_lab_uom_id_2 = fields.Many2one('ksc.lab.test.uom', string='UOM')
    pr2_from_age = fields.Integer(string="From")
    pr2_from_by_day = fields.Float(
        compute='_compute_from_by_day_2', string='From By Day')
    pr2_to_by_day = fields.Float(
        compute='_compute_to_by_day_2', string='To By Day')
    pr2_to_age = fields.Integer(string="To")
    pr2_age_type = fields.Selection([
        ('year', 'year'),
        ('month', 'month'),
        ('day', 'day'),
    ], string="Age Type")

    @api.depends('pr2_from_age', 'pr2_to_age', 'pr2_age_type')
    def _compute_to_by_day_2(self):
        for rec in self:
            pr2_to_by_day = 0
            if rec.pr2_to_age and rec.pr2_age_type:
                if rec.pr2_age_type == 'day':
                    pr2_to_by_day = rec.pr2_to_age
                elif rec.pr2_age_type == 'month':
                    pr2_to_by_day = rec.pr2_to_age * 30.33333
                elif rec.pr2_age_type == 'year':
                    pr2_to_by_day = (rec.pr2_to_age * 365) + 364
            rec.pr2_to_by_day = pr2_to_by_day

    @api.depends('pr2_from_age', 'pr2_to_age', 'pr2_age_type')
    def _compute_from_by_day_2(self):
        for rec in self:
            pr2_from_by_day = 0
            if rec.pr2_from_age and rec.pr2_age_type:
                rec.test_type = rec.test_id.test_type.name
                if rec.pr2_age_type == 'day':
                    pr2_from_by_day = rec.pr2_from_age
                elif rec.pr2_age_type == 'month':
                    pr2_from_by_day = rec.pr2_from_age * 30.33333
                elif rec.pr2_age_type == 'year':
                    pr2_from_by_day = rec.pr2_from_age * 365
            rec.pr2_from_by_day = pr2_from_by_day

    @api.constrains('pr2_from_age', 'pr2_to_age', 'pr2_to_age')
    def _constrains_age_2(self):
        for rec in self:
            if rec.pr2_age_type == 'year' and (rec.pr2_from_age == 0 or rec.pr2_to_age == 0):
                raise ValidationError(_('year must be not equal zero!'))
            if rec.pr2_age_type == 'month' and (rec.pr2_from_age <= 0 or rec.pr2_to_age > 12):
                raise ValidationError(
                    _('month must be less than 12 and bigest than 0!'))
            if rec.pr2_age_type == 'day' and (rec.pr2_from_age <= 0 or rec.pr2_to_age > 30):
                raise ValidationError(
                    _('day must be less than 30 and bigest than 0!'))
            if rec.pr2_from_age > rec.pr2_to_age:
                raise ValidationError(_('the to must be less than from!'))

    def is_btween_2(self, age):
        return age >= self.pr2_from_by_day and age <= self.pr2_to_by_day


class LabParameterLine3(models.Model):
    _name = "lab.parameter.line.three"
    _description = "Lab Parameter Line Three"

    name = fields.Char('Name')
    patient_lab_id = fields.Many2one('patient.laboratory.test', 'Lab Test')
    normal_range_3 = fields.Char(string="Reference")
    test_id = fields.Many2one('ksc.lab.test', ondelete='cascade')
    remark = fields.Char('Remark')


class malariaResults(models.Model):
    _name = "malaria.results"
    _description = "Malaria Results"

    malaria_type = fields.Selection(
        [('1', 'Not Seen'), ('2', 'Plasmodium falciparum'), ('3', 'Plasmodium vivax'), ('4', 'Plasmodium ovale'),
         ('5', 'Plasmodium malariae'), ('6', 'Plasmodium knowlesi')], string='Malaria Type', tracking=True)
    malaria_shape = fields.Selection(
        [('1', 'Ring - Present'), ('2', 'Trophozoite - Present'), ('3', 'Schizont - present'), ('4', 'Gametocyte - present')], string='Malaria Shape',
        tracking=True)
    patient_lab_id = fields.Many2one('patient.laboratory.test', 'Lab Test')

    def _valid_field_parameter(self, field, name):
        # Allow 'tracking' parameter for fields
        if name == "tracking":
            return True
        return super()._valid_field_parameter(field, name)


class gramStainResults(models.Model):
    _name = "gram.stain.results"
    _description = "Malaria Results"

    x = fields.Selection(
        [('1', 'Scanty number of'), ('2', 'Moderate number of'), ('3', 'Heavy number of'), ('4', 'Occasional'),
         ('5', 'Few'), ('6', 'Heavy')], string="Gram Stain Show's")
    y = fields.Selection([('1', 'Gram Positive (G+)'), ('2', 'Gram Negative (G-)'), ('3', 'Epithelial cells seen'),
                          ('4', 'Pus cells seen')], string="Of")
    z = fields.Selection([('1', 'cocci'), ('2', 'bacilli'),
                         ('3', 'coccobacilli')], string="Type")
    l = fields.Selection([('1', 'in clusters'), ('2', 'in chains'), ('3', 'in pairs'), ('4', 'in singles')],
                         string="Shape")
    patient_lab_id = fields.Many2one('patient.laboratory.test', 'Lab Test')
    def _valid_field_parameter(self, field, name):
        # Allow 'tracking' parameter for fields
        if name == "tracking":
            return True
        return super()._valid_field_parameter(field, name)
