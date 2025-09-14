# -*- coding: utf-8 -*-lab.test.result

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LabTestResult(models.Model):
    _name = 'lab.test.result'
    _description = 'Lab Test Result'

    patient_lab_id = fields.Many2one(
        'patient.laboratory.test', 'Lab Test', ondelete='cascade')
    parameter_id = fields.Many2one(
        'lab.parameter.line', required=True, ondelete='cascade')
    sequence = fields.Integer("Sequence", default="1")
    name = fields.Char("Name")
    lab_uom_id = fields.Many2one(
        'ksc.lab.test.uom', related="parameter_id.lab_uom_id")
    lab_uom_id_2 = fields.Many2one(
        'ksc.lab.test.uom', related="parameter_id.lab_uom_id_2")
    result = fields.Char('Result')
    culture_growth_result = fields.Selection(
        [('sensitive', 'Sensitive'), ('intermediate_sensitive',
                                      'Intermediate Sensitive'), ('resistant', 'Resistant')],
        string='Culture 1')
    culture_growth_result_2 = fields.Selection(
        [('sensitive', 'Sensitive'), ('intermediate_sensitive',
                                      'Intermediate Sensitive'), ('resistant', 'Resistant')],
        string='Culture 2')
    culture_growth_result_3 = fields.Selection(
        [('sensitive', 'Sensitive'), ('intermediate_sensitive',
                                      'Intermediate Sensitive'), ('resistant', 'Resistant')],
        string='Culture 3')
    widal_result = fields.Selection(
        [('1', '< 1:20'), ('2', '1:20'), ('3', '1:40'), ('4', '1:80'), ('5', '1:160'), ('6', '1:320'), ('7', '1:640'),
         ('8', '1:1280'),
         ('9', '1:2560'), ('10', '1:5120')], string='Result')
    brucella_result = fields.Selection(
        [('1', '< 1:20 NEGATIVE'), ('2', '= 1:20'), ('3', '= 1:40'), ('4', ' = 1:80 POSITIVE'),
         ('5', '= 1:160 POSITIVE'), ('6',
                                     '= 1:320 POSITIVE'), ('7', '= 1:640 POSITIVE'),
         ('8', '= 1:1280 POSITIVE'),
         ('9', '= 1:2560 POSITIVE'), ('10', '= 1:5120 POSITIVE')], string='Result')
    brucella_rose_result = fields.Selection(
        [('1', '< 25'), ('2', '= 25')], string='Result')
    rpr_result = fields.Selection(
        [('1', 'NON-REACTIVE'), ('2', 'REACTIVE(1:20)'), ('3', 'REACTIVE(1:40)'), ('4', 'REACTIVE(1:80)'),
         ('5', 'REACTIVE(1:160)'), ('6', 'REACTIVE(1:320)'), ('7', 'REACTIVE(1:640)'),
         ('8', 'REACTIVE(1:1280)'),
         ('9', 'REACTIVE(1:2560)'), ('10', 'REACTIVE(1:5120)')], string='Result')
    polar_result = fields.Selection(
        [('positive', 'POSITIVE'), ('negative', 'NEGATIVE')], string='Result')
    pregnancy_result = fields.Selection([('1', 'POSITIVE'), ('2', 'NEGATIVE'), ('3', 'DOUBTFUL POSITIVE')],
                                        string='Result')
    blood_group_result = fields.Selection(
        [('1', 'A'), ('2', 'B'), ('3', 'O'), ('4', 'AB')], string="Result")
    min_result = fields.Integer('Minutes')
    sec_result = fields.Integer('Seconds')
    patient_normal_range = fields.Char('Patient Normal Range', readonly=True)
    control_normal_range = fields.Char('Control Normal Range', readonly=True)
    patient = fields.Float('Patient In Second', default=1)
    control = fields.Float('Control In Second', default=1)
    isi = fields.Float('ISI', default=1.0)
    inr = fields.Float('INR', compute='_inr_calculation',
                       readonly=True, digits=(12, 4))
    normal_range = fields.Text("Reference", readonly=True)
    normal_range_2 = fields.Text("Reference", readonly=True)
    result_type = fields.Selection([
        ('normal', "Normal"),
        ('warning', "Warning"),
        ('danger', "Danger"),
    ], default='normal', string="Result Type", required=True)
    remark = fields.Char("Remark")

    def _inr_calculation(self):
        for rec in self:
            inr_result = (rec.patient / rec.control) ** rec.isi
            rec.inr = inr_result
    # ===========new requirments ================================4-2-2024======
    # ASO test

    aso_result = fields.Selection(
        [('1', '< 200'), ('2', '= 200'), ('3', '= 400'), ('4', '= 800'),
         ('5', '= 1600'), ('6', '= 3200'), ('7', '= 6400'), ('8', '= 12800')], string='Result', tracking=True)

    # CRP test
    crp_result = fields.Selection([
        ('1', '< 6'), ('2', '= 6'), ('3', '= 12'), ('4', '= 24'),
        ('5', '= 48'), ('6', '= 96'), ('7', '= 192'), ('8', '= 384'),
        ('9', '= 768'), ('10', '= 1536')], string='Result', tracking=True)

    # RF test
    rf_result = fields.Selection([
        ('1', '< 8'), ('2', '= 8'), ('3', '= 16'), ('4', '= 32'),
        ('5', '= 64'), ('6', '= 128'), ('7', '= 256'), ('8', '= 512'),
        ('9', '= 1024'), ('10', '= 2048'), ('11', '= 4096')], string='Result', tracking=True)
    # GONORRHEA
    gonorrhea_result = fields.Selection([('1', 'POSITIVE'), ('2', 'NEGATIVE')],
                                        string='Result')
    # Celiac
    celiac_result = fields.Selection([('1', 'POSITIVE'), ('2', 'NEGATIVE')],
                                     string='Result')

    # Alcohol
    alcohol_result = fields.Selection([('1', 'POSITIVE'), ('2', 'NEGATIVE')],
                                      string='Result')

    # Drugs
    drugs_result = fields.Selection([('1', 'POSITIVE'), ('2', 'NEGATIVE')],
                                    string='Result')
    def _valid_field_parameter(self, field, name):
        # Allow 'tracking' parameter for fields
        if name == "tracking":
            return True
        return super()._valid_field_parameter(field, name)


class LabTestResult2(models.Model):
    _name = 'lab.test.result.two'
    _description = 'Lab Test Result'

    patient_lab_id = fields.Many2one(
        'patient.laboratory.test', 'Lab Test', ondelete='cascade')
    sequence = fields.Integer("Sequence", default="1")
    parameter_id = fields.Many2one(
        'lab.parameter.line.two', required=True, ondelete='cascade')
    name = fields.Char("Name", readonly=True)
    rs2_lab_uom_id = fields.Many2one(
        'ksc.lab.test.uom', related="parameter_id.pr2_lab_uom_id")
    rs2_lab_uom_id_2 = fields.Many2one(
        'ksc.lab.test.uom', related="parameter_id.pr2_lab_uom_id_2")
    rs2_result = fields.Char('Result')
    rs2_normal_range = fields.Text(
        "Reference", related="parameter_id.pr_normal_range", readonly=True)
    patient_normal_range_2 = fields.Char('Patient Normal Range', readonly=True)
    control_normal_range_2 = fields.Char('Control Normal Range', readonly=True)
    normal_range_2 = fields.Text("Reference", readonly=True)
    result_2 = fields.Char('Result', readonly=True)
    patient_2 = fields.Float('Patient In Second', default=1)
    control_2 = fields.Float('Control In Second', default=1)
    polar_result_2 = fields.Selection(
        [('positive', 'POSITIVE'), ('negative', 'NEGATIVE')], string='Result')
    remark = fields.Char("Remark")

    def _valid_field_parameter(self, field, name):
        # Allow 'tracking' parameter for fields
        if name == "tracking":
            return True
        return super()._valid_field_parameter(field, name)

class LabTestResult3(models.Model):
    _name = 'lab.test.result.three'
    _description = 'Lab Test Result'

    patient_lab_id = fields.Many2one(
        'patient.laboratory.test', 'Lab Test', ondelete='cascade')
    sequence = fields.Integer("Sequence", default="1")
    parameter_id = fields.Many2one(
        'lab.parameter.line.three', required=True, ondelete='cascade')
    name = fields.Char("Name", readonly=True)
    min_result = fields.Integer('Minutes')
    sec_result = fields.Integer('Seconds')
    normal_range = fields.Text("Reference", readonly=True)
    remark = fields.Char("Remark")
    def _valid_field_parameter(self, field, name):
        # Allow 'tracking' parameter for fields
        if name == "tracking":
            return True
        return super()._valid_field_parameter(field, name)


# ======================================================================================
# ================common values ========================================================
# ======================================================================================
urine_result_list = [('1', "None"), ('2', "Mucus threads"), ('3', "Yeast Cells"), ('4', "Budding Yeast Cells"), ('5', "Monilia"),
                     ('6', "Spermatozoa"), ('7', "Oval Fat Bodies"), ('8',
                                                                      "Trichomonas vaginalis trophozoite"),
                     ('9', "Scistosoma haematobium ova"), ('10',
                                                           "Cotton Fiber"), ('11', "Talcum Powder"),
                     ('12', "Starch"), ('13', "Hair"), ('14', "Talcum Powder"),
                     ('16', "Calcium carbonates"), ('17', "Calcium phosphates"), (
    '18', "Styruvites"), ('19', "Cholesterol"), ('20', "Cystine"),
    ('21', "Leucine"), ('22', "Tyrosine"), ('23', "Sulfa"),  (
    '24', "Ammonium biurates"), ('25', "Acyclovir"), ('26', "Amoxicillin"),
    ('27', "Hyaline casts"), ('28', "Waxy casts"), ('29', "Coarse granular casts"),
    ('30', "Fine granular casts"), ('31',
                                    "Leukocyte casts"), ('32', "Erythrocyte casts"),
    ('33', "Epithelial casts"), ('34',
                                 "Cellular casts"), ('35', "Bacterial casts"),
    ('36', "Bilirubin casts"), ('37', "Yeast casts"), ('38', "Fatty casts"),
    ('39', "Hemoglobin casts"), ('40',
                                 "Macrophage casts"), ('41', "Myeloma casts"),
    ('42', "Neutrophil casts"), ('43',
                                 "Oxalate casts"), ('44', "Renal Epithelial casts"),
    ('45', "Renal Tubular casts"), ('46', "Uric Acid casts"),
    ('47', "Fat Bodies"), ('48', "Feces"), ('49',
                                            "Clue cell"), ('50', "Triple phosphates"),
    ('51', "Amorphous urates"), ('52', "Amorphous phosphates"), ('53',
                                                                 "Calcium oxalates"), ('54', "Uric acids"), ('55', "Triple phosphates"),
]

urine_shape_list = [('1', 'present'), ('2', '+'),
                    ('3', '++'), ('4', '+++'), ('5', '++++')]

other_shape_stool_list = [
    ('1', 'present'), ('2', 'ova seen'), ('3',
                                          'fertilized ova seen'), ('4', 'unfertilized ova seen'),
    ('5', 'cysts seen'), ('6', 'trophozoites seen'), ('7',
                                                      'adult seen'), ('8', 'adult female seen'),
    ('9', 'adult male seen'), ('10', 'scolex seen'), ('11',
                                                      'proglottids seen'), ('12', 'oocysts seen'),
    ('13', 'larvae seen'), ('14',
                            'filariform larvae seen'), ('15', 'rhabditiform larvae seen'),
]

semen_head_defects_list1 = [
    ('1', 'Double'), ('2', 'Giant'),
    ('3', 'Amorphous'), ('4', 'Pin'),
    ('5', 'Tapered'), ('6', 'Constricted')]

semen_head_defects_list2 = [
    ('1', '/ Double'), ('2', '/ Giant'),
    ('3', '/ Amorphous'), ('4', '/ Pin'),
    ('5', '/ Tapered'), ('6', '/ Constricted')]

semen_neck_midpiece_defects_list1 = [
        ('1', 'Asymmetric'), ('2', 'Bent'), ('3', 'Thin'), ('4', 'Thick'),
        ('5', 'Irregular'), ('6', 'Cytoplasmic Droplet')]

semen_neck_midpiece_defects_list2 = [
        ('1', '/ Asymmetric'), ('2', '/ Bent'), ('3', '/ Thin'), ('4', '/ Thick'),
        ('5', '/ Irregular'), ('6', '/ Cytoplasmic Droplet')]


semen_tail_defects_list1 =[
        ('1', 'Doubled'), ('2', 'Coiled'), ('3', 'Short'), ('4', 'Broken')]

semen_tail_defects_list2 = [
         ('1', '/ Doubled'), ('2', '/ Coiled'), ('3', '/ Short'), ('4', '/ Broken')]

growth_of_list = [('1', "ß Hemolytic Streptococci"), ('2', "Coagulase Negative Staphylococcus species"),
                  ('3', "Escherichia coli"), ('4',
                                              "Gram Negative Bacilli"), ('5', "Group 'B' Streptococci"),
                  ('6', "Klebsiella species"), ('7',
                                                "Non-Hemolytic Streptococci"), ('8', "Proteus species"),
                  ('9', "Pseudomonas aeruginosa"), ('10',
                                                    "Pseudomonas species"), ('11', "Staphylococcus aureus"),
                  ('12', "Staphylococcus spp."), ('13',
                                                  "Staphylococcus epidermidis."), ('14', "Salmonella spp."),
                  ('15', "Shigella spp."), ('16',
                                            "Group 'A' Streptococci"), ('17', "Group 'C' Streptococci"),
                  ('18', "Group 'D' Streptococci"), ('19',
                                                     "Group 'F' Streptococci"), ('20', "Group 'G' Streptococci"),
                  ('21', "Streptococcus pyogenes"), ('22',
                                                     "Streptococcus agalactiae"), ('23', "Streptococcus pneumoniae"),
                  ('24', "Group 'D' Enterococcus"), ('25', "Group 'D' Non-Enterococcus")]
# ======================================================================================
# ======================================================================================
# ======================================================================================


class PatientLabTest(models.Model):
    _name = "patient.laboratory.test"
    _inherit = ['portal.mixin', 'mail.thread',
                'mail.activity.mixin', 'ksc.mixin']
    _description = "Patient Laboratory Test"
    _order = 'date_analysis desc, id desc'

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    name = fields.Char(string='Test ID', help="Lab result ID",
                       readonly="1", copy=False, index=True, tracking=True)
    test_id = fields.Many2one('ksc.lab.test', string='Test', required=True, ondelete='restrict',
                              tracking=True)
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, ondelete='restrict',
                                 tracking=True)
    user_id = fields.Many2one('res.users', string='Lab User',
                              default=lambda self: self.env.user, tracking=True)
    physician_id = fields.Many2one('res.partner', string='Prescribing Doctor', help="Doctor who requested the test",
                                   ondelete='restrict', tracking=True)
    processed_by = fields.Many2one(
        'res.users', "Processed By", readonly=True, tracking=True)
    diagnosis = fields.Text(string='Diagnosis', tracking=True)
    has_multi_dev = fields.Boolean(
        readonly=True, compute="compute_has_multi_device")
    device_id = fields.Selection(
        [('1', 'Vitros (XT 7600 System Integrated)'), ('2', 'Snibe (Maglumi X3)')], 'Device')

    def compute_has_multi_device(self):
        for rec in self:
            if rec.test_id:
                if rec.test_id.test_type.has_multi_device:
                    rec.has_multi_dev = True
                else:
                    rec.has_multi_dev = False

    # result one
    result_ids = fields.One2many(
        'lab.test.result', 'patient_lab_id', tracking=True)
    culture = fields.Selection(
        [('1', 'Scanty growth of'), ('2', 'Moderate growth of'), ('3', 'Heavy growth of'), ('4', '< 10⁴ growth of'),
         ('5', '10⁴ - 10⁵ growth of'), ('6', '> 10⁵ growth of'),
         ('7', 'No growth after 48 hrs of incubation'), ('8',
                                                         'No significant bacterial growth'),
         ('9', 'Growth of normal bacterial flora'), ('10',
                                                     'No pathogenic organism isolated'),
         ('11', 'No Salmonella spp. nor Shigella spp. isolated after 48 hours of incubation.'),
         ], string='Culture 1', tracking=True)
    growth_of = fields.Selection(
        growth_of_list, string='Growth Of', tracking=True)
    culture_2 = fields.Selection(
        [('1', 'Scanty growth of'), ('2', 'Moderate growth of'), ('3', 'Heavy growth of'), ('4', '< 10⁴ growth of'),
         ('5', '10⁴ - 10⁵ growth of'), ('6', '> 10⁵ growth of'),
         ('7', 'No growth after 48 hrs of incubation'), ('8',
                                                         'No significant bacterial growth'),
         ('9', 'Growth of normal bacterial flora'), ('10',
                                                     'No pathogenic organism isolated'),
         ('11', 'No Salmonella spp. nor Shigella spp. isolated after 48 hours of incubation.'),
         ], string='Culture 2', default='11', tracking=True)
    growth_of_2 = fields.Selection(
        growth_of_list, string='Growth Of', tracking=True)
    culture_3 = fields.Selection(
        [('1', 'Scanty growth of'), ('2', 'Moderate growth of'), ('3', 'Heavy growth of'), ('4', '< 10⁴ growth of'),
         ('5', '10⁴ - 10⁵ growth of'), ('6', '> 10⁵ growth of'),
         ('7', 'No growth after 48 hrs of incubation'), ('8',
                                                         'No significant bacterial growth'),
         ('9', 'Growth of normal bacterial flora'), ('10',
                                                     'No pathogenic organism isolated'),
         ('11', 'No Salmonella spp. nor Shigella spp. isolated after 48 hours of incubation.'),

         ], string='Culture 3', tracking=True)
    growth_of_3 = fields.Selection(growth_of_list,
                                   string='Growth Of', default='1', tracking=True)
    has_2_bactria = fields.Boolean(
        "Has Two Culture", default=False, tracking=True)
    has_3_bactria = fields.Boolean("Has Three Culture", tracking=True)
    fungal = fields.Selection(
        [('1', 'No fungal growth obtained'), ('2', 'Scanty growth of'), ('3', 'Moderate growth of'),
         ('4', 'Heavy growth of')], string="Fungal Culture", tracking=True)
    candida = fields.Selection(
        [('1', 'Candida albicans'), ('2', 'Candida species.')], string="Candida", tracking=True)
    gram_stain_negative = fields.Selection(
        [('1', 'No Gram Negative (G-) intracellular diplococci seen'),
         ('2', 'Few Gram Negative (G-) intracellular diplococci seen.'),
         ('3', 'Moderate Gram Negative (G-) intracellular diplococci seen.'),
         ('4', 'Numerous Gram Negative (G-) intracellular diplococci seen.'),

         ],
        string='Gram Negative', default='1', tracking=True)
    is_polar = fields.Boolean(compute='func_is_polar')
    is_customize_and_culture_growth = fields.Boolean(
        compute='func_is_customize_and_culture_growth', default=False)
    is_parameter = fields.Boolean(compute='func_is_parameter', default=False)
    is_widal = fields.Boolean(compute='func_is_widal', default=False)
    is_brucella = fields.Boolean(compute='func_is_brucella', default=False)
    is_rpr = fields.Boolean(compute='func_is_rpr', default=False)
    is_min_sec = fields.Boolean(compute='func_is_min_sec', default=False)
    is_patient_and_control = fields.Boolean(
        compute='func_is_patient_and_control', default=False)
    is_inr = fields.Boolean(compute='func_is_inr', default=False)
    is_normal_range_2 = fields.Boolean(
        compute='func_is_normal_range_2', default=False)
    is_UOM = fields.Boolean(compute='func_is_UOM', default=False)
    is_malaria = fields.Boolean(compute='func_is_malaria', default=False)
    is_gram = fields.Boolean(compute='func_is_gram', default=False)
    is_pregnancy = fields.Boolean(compute='func_is_pregnancy', default=False)
    is_brucella_rose = fields.Boolean(
        compute='func_is_brucella_rose', default=False)
    is_blood_group = fields.Boolean(
        compute='func_is_blood_group', default=False)
    is_fixed_table = fields.Boolean(compute='func_fixed_table', default=False)
    is_special_test_and_sprcial_result_and_patient_control = fields.Boolean(
        compute='func_is_special_test_and_sprcial_result_and_patient_control', default=False)
    # end result one

    # result two
    result_ids_2 = fields.One2many(
        'lab.test.result.two', 'patient_lab_id', tracking=True)
    has_two_result = fields.Boolean(
        compute='func_has_two_result', default=False)
    is_patient_and_control_2 = fields.Boolean(
        compute='func_is_patient_and_control_2', default=False)
    is_polar_2 = fields.Boolean(compute='func_is_polar_2', default=False)
    is_custom_reference_2 = fields.Boolean(
        compute='func_is_custom_reference_2', default=False)
    # end result two

    # result three
    result_ids_3 = fields.One2many(
        'lab.test.result.three', 'patient_lab_id', tracking=True)
    has_three_result = fields.Boolean(
        compute='func_has_three_result', default=False)
    is_min_sec_3 = fields.Boolean(compute='func_is_min_sec_3', default=False)
    is_normal_range_3 = fields.Boolean(
        compute='func_is_normal_range_3', default=False)
    # end result three

    # special result
    malaria_result_ids = fields.One2many(
        'malaria.results', 'patient_lab_id', tracking=True)
    grain_stain_result_ids = fields.One2many(
        'gram.stain.results', 'patient_lab_id', tracking=True)
    # end special result

    # special test
    # urine routine
    is_urine_routine_test = fields.Boolean(
        compute='func_is_urine_routine_test', default=False)
    color_urine = fields.Selection(
        [('1', 'Straw'), ('2', 'Light Yellow'), ('3', 'Yellow'), ('4', 'Dark Yellow'), ('5', 'Amber'), ('6', 'Red'),
         ('7', 'Brown'), ('8', 'Black')], string="Color", tracking=True)
    appearance_urine = fields.Selection([('1', 'Clear'), ('2', 'Slightly Turbid'), ('3', 'Turbid')],
                                        string="Appearance", tracking=True)

    specific_gravity_urine = fields.Selection(
        [('1', '1.000'), ('2', '1.005'), ('3', '1.010'), ('4', '1.015'), ('5', '1.020'), ('6', '1.025'),
         ('7', '1.030')], string="Specific Gravity (SG)", tracking=True)
    ph_urine = fields.Selection(
        [('1', '5.0'), ('2', '5.5'), ('3', '6.0'), ('4', '6.5'), ('5', '7.0'), ('6', '8.0'), ('7', '9.0')], string="pH", tracking=True)
    glucose_urine = fields.Selection([('1', 'Normal'), ('2', '2.8'), ('3', '5.5'), ('4', '17'), ('5', '55')],
                                     string="Glucose (GLU)", tracking=True)
    lecucocytes_urine = fields.Selection([('1', 'Negative'), ('2', '10'), ('3', '25'), ('4', '75'), ('5', '500')],
                                         string="Leucocytes (LEU)", tracking=True)
    nitrite_urine = fields.Selection(
        [('1', 'Negative'), ('2', 'Positive')], string="Nitrite (NIT)", tracking=True)
    protien_urine = fields.Selection([('1', 'Negative'), ('2', '0.3'), ('3', '1'), ('4', '5')],
                                     string="Protein (PRO)nce", tracking=True)
    ketones_urine = fields.Selection([('1', 'Negative'), ('2', '1.5'), (
        '3', '5'), ('4', '15')], string="Ketones (KET)", tracking=True)
    urobilinogen_urine = fields.Selection([('1', 'Normal'), ('2', '17'), ('3', '51'), ('4', '102'), ('5', '203')],
                                          string="Urobilinogen (URO)", tracking=True)
    bilirubin_urine = fields.Selection(
        [('1', 'Negative'), ('2', '17'), ('3', '51'),
         ('4', '103'), ('5', '+'), ('6', '++'), ('7', '+++')],
        string="Bilirubin (BIL)", tracking=True)
    blood_urine = fields.Selection([('1', 'Negative'), ('2', '5'), ('3', '10'), ('4', '50'), ('5', '250')],
                                   string="Blood (BLD)", tracking=True)
    # normal range
    specific_gravity_urine_normal_range = fields.Char(
        "Specific Gravity Normal Range", readonly=True)
    ph_urine_normal_range = fields.Char("PH Normal Range", readonly=True)
    glucose_urine_normal_range = fields.Char(
        "Glucose Normal Range", readonly=True)
    lecucocytes_urine_normal_range = fields.Char(
        "Lecucocytes Normal Range", readonly=True)
    nitrite_urine_normal_range = fields.Char(
        "Nitrite Normal Range", readonly=True)
    protien_urine_normal_range = fields.Char(
        "Protien Normal Range", readonly=True)
    ketones_urine_normal_range = fields.Char(
        "Ketones Normal Range", readonly=True)
    urobilinogen_urine_normal_range = fields.Char(
        "Urobilinogen Normal Range", readonly=True)
    bilirubin_urine_normal_range = fields.Char(
        "Bilirubin Normal Range", readonly=True)
    blood_urine_normal_range = fields.Char("Blood Normal Range", readonly=True)
    # UOM of normal range
    glucose_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                        related="test_id.glucose_urine_UOM")
    lecucocytes_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                            related="test_id.lecucocytes_urine_UOM")
    protien_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                        related="test_id.protien_urine_UOM")
    ketones_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                        related="test_id.ketones_urine_UOM")
    urobilinogen_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                             related="test_id.urobilinogen_urine_UOM")
    bilirubin_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                          related="test_id.bilirubin_urine_UOM")
    blood_urine_UOM = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                      related="test_id.blood_urine_UOM")

    white_blood_cells_urine = fields.Char(
        "White Blood Cells (WBC)", tracking=True)
    red_blood_cells_urine = fields.Char("Red Blood Cells (RBC)", tracking=True)
    epithelial_cells_urine = fields.Selection([('1', 'Nil'), ('2', '+'), ('3', '++'), ('4', '+++'), ('5', '++++')],
                                              string="Epithelial Cells", tracking=True)
    bacteria_urine = fields.Selection([('1', 'Nil'), ('2', '+'), ('3', '++'), ('4', '+++'), ('5', '++++')],
                                      string="Bacteria", tracking=True)
    crystals_urine = fields.Selection(
        [('1', "Nil"), ('2', "Amorphous urates"),
         ('3', "Amorphous phosphates"), ('4',
                                         "Calcium oxalates"), ('5', "Uric acids"),
         ('6', "Triple phosphates"),
         ('7', "Calcium carbonates"), ('8', "Calcium phosphates"),
         ('9', "Styruvites"), ('10', "Cholesterol"), ('11', "Cystine"),
         ('12', "Leucine"), ('13', "Tyrosine"), ('14', "Sulfa"),
         ('15', "Ammonium biurates"), ('16', "Acyclovir"), ('17', "Amoxicillin"),

         ],
        string='Crystals', tracking=True)
    crystals_shape_urine = fields.Selection(urine_shape_list,
                                            string="Crystal Quantity", tracking=True)
    casts_urine = fields.Selection([('1', "Nil"),
                                    ('2', "Hyaline casts"), ('3',
                                                             "Waxy casts"), ('4', "Coarse granular casts"),
                                    ('5', "Fine granular casts"), ('6',
                                                                   "Leukocyte casts"), ('7', "Erythrocyte casts"),
                                    ('8', "Epithelial casts"), ('9',
                                                                "Cellular casts"), ('10', "Bacterial casts"),
                                    ('11', "Bilirubin casts"), ('12',
                                                                "Yeast casts"), ('13', "Fatty casts"),
                                    ('14', "Hemoglobin casts"), ('15',
                                                                 "Macrophage casts"), ('16', "Myeloma casts"),
                                    ('13', "Neutrophil casts"), ('18',
                                                                 "Oxalate casts"), ('19', "Renal Epithelial casts"),
                                    ('20', "Renal Tubular casts"), ('21',
                                                                    "Uric Acid casts")
                                    ],
                                   string='Casts', tracking=True)
    casts_shape_urine = fields.Selection(urine_shape_list,
                                         string="Casts Quantity", tracking=True)
    other_1_urine = fields.Selection(
        urine_result_list, string="Other Findings", tracking=True)
    shape_1_urine = fields.Selection(urine_shape_list,
                                     string="Quantity", tracking=True)
    other_2_urine = fields.Selection(
        urine_result_list, string="Other Findings", tracking=True)
    shape_2_urine = fields.Selection(urine_shape_list,
                                     string="Quantity", tracking=True)
    other_3_urine = fields.Selection(
        urine_result_list, string="Other Findings", tracking=True)
    shape_3_urine = fields.Selection(urine_shape_list,
                                     string="Quantity", tracking=True)
    other_4_urine = fields.Selection(
        urine_result_list, string="Other Findings", tracking=True)
    shape_4_urine = fields.Selection(urine_shape_list,
                                     string="Quantity", tracking=True)
    # end urine routine

    # urine routine without micro

    color_urine_without_micor = fields.Selection(
        [('1', 'Straw'), ('2', 'Light Yellow'), ('3', 'Yellow'), ('4', 'Dark Yellow'), ('5', 'Amber'), ('6', 'Red'),
         ('7', 'Brown'), ('8', 'Black')], string="Color", tracking=True)
    appearance_urine_without_micor = fields.Selection([('1', 'Clear'), ('2', 'Slightly Turbid'), ('3', 'Turbid')],
                                                      string="Appearance", tracking=True)

    specific_gravity_urine_without_micor = fields.Selection(
        [('1', '1.000'), ('2', '1.005'), ('3', '1.010'), ('4', '1.015'), ('5', '1.020'), ('6', '1.025'),
         ('7', '1.030')], string="Specific Gravity (SG)", tracking=True)
    ph_urine_without_micor = fields.Selection(
        [('1', '5.0'), ('2', '5.5'), ('3', '6.0'), ('4', '6.5'), ('5', '7.0'), ('6', '8.0'), ('7', '9.0')], string="pH", tracking=True)
    glucose_urine_without_micor = fields.Selection([('1', 'Normal'), ('2', '2.8'), ('3', '5.5'), ('4', '17'), ('5', '55')],
                                                   string="Glucose (GLU)", tracking=True)
    lecucocytes_urine_without_micor = fields.Selection([('1', 'Negative'), ('2', '10'), ('3', '25'), ('4', '75'), ('5', '500')],
                                                       string="Leucocytes (LEU)", tracking=True)
    nitrite_urine_without_micor = fields.Selection(
        [('1', 'Negative'), ('2', 'Positive')], string="Nitrite (NIT)", tracking=True)
    protien_urine_without_micor = fields.Selection([('1', 'Negative'), ('2', '0.3'), ('3', '1'), ('4', '5')],
                                                   string="Protein (PRO)", tracking=True)
    ketones_urine_without_micor = fields.Selection(
        [('1', 'Negative'), ('2', '1.5'), ('3', '5'), ('4', '15')], string="Ketones (KET)", tracking=True)
    urobilinogen_urine_without_micor = fields.Selection([('1', 'Normal'), ('2', '17'), ('3', '51'), ('4', '102'), ('5', '203')],
                                                        string="Urobilinogen (URO)", tracking=True)
    bilirubin_urine_without_micor = fields.Selection(
        [('1', 'Negative'), ('2', '17'), ('3', '51'),
         ('4', '103'), ('5', '+'), ('6', '++'), ('7', '+++')],
        string="Bilirubin (BIL)", tracking=True)
    blood_urine_without_micor = fields.Selection([('1', 'Negative'), ('2', '5'), ('3', '10'), ('4', '50'), ('5', '250')],
                                                 string="Blood (BLD)", tracking=True)
    # normal range
    specific_gravity_urine_without_mico_normal_range = fields.Char(
        "Specific Gravity Normal Range", readonly=True)
    ph_urine_without_mico_normal_range = fields.Char(
        "PH Normal Range", readonly=True)
    glucose_urine_without_mico_normal_range = fields.Char(
        "Glucose Normal Range", readonly=True)
    lecucocytes_urine_without_mico_normal_range = fields.Char(
        "Lecucocytes Normal Range", readonly=True)
    nitrite_urine_without_mico_normal_range = fields.Char(
        "Nitrite Normal Range", readonly=True)
    protien_urine_without_mico_normal_range = fields.Char(
        "Protien Normal Range", readonly=True)
    ketones_urine_without_mico_normal_range = fields.Char(
        "Ketones Normal Range", readonly=True)
    urobilinogen_urine_without_mico_normal_range = fields.Char(
        "Urobilinogen Normal Range", readonly=True)
    bilirubin_urine_without_mico_normal_range = fields.Char(
        "Bilirubin Normal Range", readonly=True)
    blood_urine_without_mico_normal_range = fields.Char(
        "Blood Normal Range", readonly=True)
    # UOM of urine routine without micor normal range

    glucose_urine_UOM_without_mico = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                                     related="test_id.glucose_urine_UOM_without_mico")
    lecucocytes_urine_UOM_without_mico = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                                         related="test_id.lecucocytes_urine_UOM_without_mico")
    protien_urine_UOM_without_mico = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                                     related="test_id.protien_urine_UOM_without_mico")
    ketones_urine_UOM_without_mico = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                                     related="test_id.ketones_urine_UOM_without_mico")
    urobilinogen_urine_UOM_without_mico = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                                          related="test_id.urobilinogen_urine_UOM_without_mico")
    bilirubin_urine_UOM_without_mico = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                                       related="test_id.bilirubin_urine_UOM_without_mico")
    blood_urine_UOM_without_mico = fields.Many2one('ksc.lab.test.uom', string='UOM', readonly=True,
                                                   related="test_id.blood_urine_UOM_without_mico")

    white_blood_cells_urine = fields.Char(
        "White Blood Cells (WBC)", tracking=True)
    red_blood_cells_urine = fields.Char("Red Blood Cells (RBC)", tracking=True)
    # end of urine without micor
    # stool routine
    is_stool_routine_test = fields.Boolean(
        compute='func_is_stool_routine_test', default=False)
    # color_stool = fields.Selection(
    #     [('1', 'Straw'), ('2', 'Light Yellow'), ('3', 'Yellow'), ('4', 'Dark Yellow'), ('5', 'Amber'), ('6', 'Red'),
    #      ('7', 'Brown'), ('8', 'Black')], string="Color", tracking=True)
    color_stool = fields.Selection(
        [('1', 'Yellow'), ('2', 'Yellowish Green'), ('3', 'Green'), ('4', 'Yellowish Brown'), ('5', 'Brown'), ('6', 'Dark Brown'),
         ('7', 'Black'), ('8', 'White')], string="Color", tracking=True)
    consistency_stool = fields.Selection(
        [('1', 'Soft-formed'), ('2', 'Hard-formed'), ('3', 'Semi-formed'), ('4', 'Mucoid'), ('5', 'Watery'),
         ('6', 'Liquid')], string="Consistency", tracking=True)
    blood_stool = fields.Selection(
        [('1', 'Nil'), ('2', 'Present')], string="Blood", tracking=True)
    mucus_stool = fields.Selection(
        [('1', 'Nil'), ('2', 'Present')], string="Mucus", tracking=True)

    white_blood_cells_stool = fields.Char(
        "White Blood Cells (WBC)", tracking=True)
    red_blood_cells_stool = fields.Char("Red Blood Cells (RBC)", tracking=True)
    yeast_cell_stool = fields.Selection([('1', 'Nil'), ('2', '+'), ('3', '++'), ('4', '+++'), ('5', '++++')],
                                        string="Yeast Cells", tracking=True)
    # parasites_stool = fields.Selection(
    #     [('1', 'Ova / Cyst not seen'), ('2', 'Entamoeba histolytica'), ('3', 'Giardia lamblia'),
    #      ('4', 'Blastocystis hominis'), ('5', 'Ascaris lumbricoides'), ('6', 'Trichuris trichiura'),
    #      ('7', 'Endolimax nana'), ('8', 'Chilomastix mesnili'), ('9', 'Enterobius vermicularis'), ('10', 'Hookworm'),
    #      ('11', 'Hymenolepis nana'), ('12', 'Balantidium coli')], string="Parasites", tracking=True)

    parasites_stool = fields.Selection(
        [('1', 'Ova / Cyst not seen'), ('2', 'Entamoeba histolytica'), ('3', 'Giardia lamblia'),
         ('4', 'Blastocystis hominis'), ('5',
                                         'Ascaris lumbricoides'), ('6', 'Trichuris trichiura'),
         ('7', 'Endolimax nana'), ('8', 'Chilomastix mesnili'), ('9',
                                                                 'Enterobius vermicularis'), ('10', 'Hookworm'),
         ('11', 'Hymenolepis nana'), ('12',
                                      'Balantidium coli'), ('13', 'Opisthorchis viverrini'),

         ('14', 'Clonorchis sinensis'), ('15',
                                         'Capillaria philippinensis'), ('16', 'Taenia spp.'),
         ('17', 'Diphyllobothrium latum'), ('18',
                                            'Hymenolepis diminuta'), ('19', 'Trichostongylus spp.'),
         ('20', 'Nanophyetus salmincola'), ('21',
                                            'Paragonimus westermani'), ('22', 'Dipylidium caninum'),
         ('23', 'Echinostoma spp.'), ('24', 'Fasciolopsis buski'),

         ('25', 'Fasciola hepatica'), ('26',
                                       'Schistosoma japonicum'), ('27', 'Schistosoma mekongi'),
         ('28', 'Schistosoma haematobium'), ('29',
                                             'Schistosoma intercalatum'), ('30', 'Schistosoma mansoni'),
         ('31', 'Iodamoeba butschlii'), ('32',
                                         'Entamoeba polecki'), ('33', 'Entamieba hartmanni'),
         ('34', 'Entamoeba coli'), ('35',
                                    'Cryptosporidium spp.'), ('36', 'Blastocystis hominis'),

         ('37', 'Mushroom spore'), ('38', 'Intestinal cell')
         ],
        string="Parasites", tracking=True)
    parasites_shape_stool = fields.Selection(other_shape_stool_list,
                                             string="Shape", tracking=True)
    other_1_stool = fields.Selection(
        [('1', 'Ova / Cyst not seen'), ('2', 'Entamoeba histolytica'), ('3', 'Giardia lamblia'),
         ('4', 'Blastocystis hominis'), ('5',
                                         'Ascaris lumbricoides'), ('6', 'Trichuris trichiura'),
         ('7', 'Endolimax nana'), ('8', 'Chilomastix mesnili'), ('9',
                                                                 'Enterobius vermicularis'), ('10', 'Hookworm'),
         ('11', 'Hymenolepis nana'), ('12',
                                      'Balantidium coli'), ('13', 'Opisthorchis viverrini'),

         ('14', 'Clonorchis sinensis'), ('15',
                                         'Capillaria philippinensis'), ('16', 'Taenia spp.'),
         ('17', 'Diphyllobothrium latum'), ('18',
                                            'Hymenolepis diminuta'), ('19', 'Trichostongylus spp.'),
         ('20', 'Nanophyetus salmincola'), ('21',
                                            'Paragonimus westermani'), ('22', 'Dipylidium caninum'),
         ('23', 'Echinostoma spp.'), ('24', 'Fasciolopsis buski'),

         ('25', 'Fasciola hepatica'), ('26',
                                       'Schistosoma japonicum'), ('27', 'Schistosoma mekongi'),
         ('28', 'Schistosoma haematobium'), ('29',
                                             'Schistosoma intercalatum'), ('30', 'Schistosoma mansoni'),
         ('31', 'Iodamoeba butschlii'), ('32',
                                         'Entamoeba polecki'), ('33', 'Entamieba hartmanni'),
         ('34', 'Entamoeba coli'), ('35',
                                    'Cryptosporidium spp.'), ('36', 'Blastocystis hominis'),

         ('37', 'Mushroom spore'), ('38', 'Intestinal cell')
         ],
        string="Other Findings", tracking=True)

    other_1_shape_stool = fields.Selection(other_shape_stool_list,
                                           string="Shape", tracking=True)
    other_2_stool = fields.Selection(
        [('1', 'Ova / Cyst not seen'), ('2', 'Entamoeba histolytica'), ('3', 'Giardia lamblia'),
         ('4', 'Blastocystis hominis'), ('5',
                                         'Ascaris lumbricoides'), ('6', 'Trichuris trichiura'),
            ('7', 'Endolimax nana'), ('8', 'Chilomastix mesnili'), ('9',
                                                                    'Enterobius vermicularis'), ('10', 'Hookworm'),
         ('11', 'Hymenolepis nana'), ('12',
                                      'Balantidium coli'), ('13', 'Opisthorchis viverrini'),

         ('14', 'Clonorchis sinensis'), ('15',
                                         'Capillaria philippinensis'), ('16', 'Taenia spp.'),
         ('17', 'Diphyllobothrium latum'), ('18',
                                            'Hymenolepis diminuta'), ('19', 'Trichostongylus spp.'),
         ('20', 'Nanophyetus salmincola'), ('21',
                                            'Paragonimus westermani'), ('22', 'Dipylidium caninum'),
         ('23', 'Echinostoma spp.'), ('24', 'Fasciolopsis buski'),

         ('25', 'Fasciola hepatica'), ('26',
                                       'Schistosoma japonicum'), ('27', 'Schistosoma mekongi'),
         ('28', 'Schistosoma haematobium'), ('29',
                                             'Schistosoma intercalatum'), ('30', 'Schistosoma mansoni'),
         ('31', 'Iodamoeba butschlii'), ('32',
                                         'Entamoeba polecki'), ('33', 'Entamieba hartmanni'),
         ('34', 'Entamoeba coli'), ('35',
                                    'Cryptosporidium spp.'), ('36', 'Blastocystis hominis'),

         ('37', 'Mushroom spore'), ('38', 'Intestinal cell')
         ],

        string="Other Findings", tracking=True)
    other_2_shape_stool = fields.Selection(other_shape_stool_list,
                                           string="Shape", tracking=True)

    other_3_stool = fields.Selection(
        [('1', 'Ova / Cyst not seen'), ('2', 'Entamoeba histolytica'), ('3', 'Giardia lamblia'),
         ('4', 'Blastocystis hominis'), ('5',
                                         'Ascaris lumbricoides'), ('6', 'Trichuris trichiura'),
            ('7', 'Endolimax nana'), ('8', 'Chilomastix mesnili'), ('9',
                                                                    'Enterobius vermicularis'), ('10', 'Hookworm'),
         ('11', 'Hymenolepis nana'), ('12',
                                      'Balantidium coli'), ('13', 'Opisthorchis viverrini'),

         ('14', 'Clonorchis sinensis'), ('15',
                                         'Capillaria philippinensis'), ('16', 'Taenia spp.'),
         ('17', 'Diphyllobothrium latum'), ('18',
                                            'Hymenolepis diminuta'), ('19', 'Trichostongylus spp.'),
         ('20', 'Nanophyetus salmincola'), ('21',
                                            'Paragonimus westermani'), ('22', 'Dipylidium caninum'),
         ('23', 'Echinostoma spp.'), ('24', 'Fasciolopsis buski'),

         ('25', 'Fasciola hepatica'), ('26',
                                       'Schistosoma japonicum'), ('27', 'Schistosoma mekongi'),
         ('28', 'Schistosoma haematobium'), ('29',
                                             'Schistosoma intercalatum'), ('30', 'Schistosoma mansoni'),
         ('31', 'Iodamoeba butschlii'), ('32',
                                         'Entamoeba polecki'), ('33', 'Entamieba hartmanni'),
         ('34', 'Entamoeba coli'), ('35',
                                    'Cryptosporidium spp.'), ('36', 'Blastocystis hominis'),

         ('37', 'Mushroom spore'), ('38', 'Intestinal cell')
         ],

        string="Other Findings", tracking=True)
    other_3_shape_stool = fields.Selection(other_shape_stool_list,
                                           string="Shape", tracking=True)

    other_4_stool = fields.Selection(
        [('1', 'Ova / Cyst not seen'), ('2', 'Entamoeba histolytica'), ('3', 'Giardia lamblia'),
         ('4', 'Blastocystis hominis'), ('5',
                                         'Ascaris lumbricoides'), ('6', 'Trichuris trichiura'),
            ('7', 'Endolimax nana'), ('8', 'Chilomastix mesnili'), ('9',
                                                                    'Enterobius vermicularis'), ('10', 'Hookworm'),
         ('11', 'Hymenolepis nana'), ('12',
                                      'Balantidium coli'), ('13', 'Opisthorchis viverrini'),

         ('14', 'Clonorchis sinensis'), ('15',
                                         'Capillaria philippinensis'), ('16', 'Taenia spp.'),
         ('17', 'Diphyllobothrium latum'), ('18',
                                            'Hymenolepis diminuta'), ('19', 'Trichostongylus spp.'),
         ('20', 'Nanophyetus salmincola'), ('21',
                                            'Paragonimus westermani'), ('22', 'Dipylidium caninum'),
         ('23', 'Echinostoma spp.'), ('24', 'Fasciolopsis buski'),

         ('25', 'Fasciola hepatica'), ('26',
                                       'Schistosoma japonicum'), ('27', 'Schistosoma mekongi'),
         ('28', 'Schistosoma haematobium'), ('29',
                                             'Schistosoma intercalatum'), ('30', 'Schistosoma mansoni'),
         ('31', 'Iodamoeba butschlii'), ('32',
                                         'Entamoeba polecki'), ('33', 'Entamieba hartmanni'),
         ('34', 'Entamoeba coli'), ('35',
                                    'Cryptosporidium spp.'), ('36', 'Blastocystis hominis'),

         ('37', 'Mushroom spore'), ('38', 'Intestinal cell')
         ],

        string="Other Findings", tracking=True)
    other_4_shape_stool = fields.Selection(other_shape_stool_list,
                                           string="Shape", tracking=True)
    # end stool routine

    # semins test
    is_semen_test = fields.Boolean(
        compute='func_is_semen_test', default=False, tracking=True)
    # --------------semen analysis-------------
    semen_time_collected = fields.Char('Time Collected', tracking=True)
    semen_abstination = fields.Selection([
        ('1', '2 Days'), ('2', '3 Days'), ('3', '4 Days'), ('4',
                                                            '5 Days'), ('5', '6 Days'), ('6', '7 Days'), ('7', '>7 Days')
    ], "Abstination", tracking=True)
    # ------------physical exam part------------
    semen_volume = fields.Float("Volume", tracking=True)
    semen_color = fields.Selection([('pearly_white', 'Pearly White'),
                                    ('pale_yellow', 'Pale Yellow'), ('white', 'White'),
                                    ('cream', 'Cream'), ('light_gray', 'Light Gray'),
                                    ('yellow', 'Yellow'),
                                    ], "Color", tracking=True)
    semen_liquifaction_time = fields.Integer(
        "Liquifaction Time", tracking=True)
    semen_odor = fields.Selection([
        ('normal', 'Normal'), ('Ammonia', 'Ammonia'), ('bleach', 'Bleach'),
        ('slightly_sweet', 'Slightly sweet'), ('very_sweet',
                                               'Very sweet'), ('fishy', 'Fishy'),
        ('rotten', 'Rotten'), ('foul_smell', 'Foul-smell'),
    ], "Odor", tracking=True)
    semen_viscosity = fields.Selection([('normal', 'Normal'), ('thin', 'Thin'), (
        'thick', 'Thick'), ('viscous', 'Viscous')], 'Viscosity', tracking=True)
    semen_ph = fields.Selection(
        [('1', '7.0'), ('2', '7.5'), ('3', '8.0'), ('4', '8.5'), ('5', '9.0')], 'pH', tracking=True)
    # ------------micro exam part------------
    semen_sperm_count = fields.Float('Sperm Count', tracking=True)
    semen_total_count = fields.Float('Total Count', tracking=True)
    semen_sperm_agglutination = fields.Selection(
        [('1', 'Nil'), ('2', '+'), ('3', '++'), ('4', '+++'), ('5', '++++'),], 'Sperm Agglutination', tracking=True)
    semen_abnormal_forms = fields.Selection([
        ('1', '<10%'), ('2', '15%'), ('3', '20%'), ('4', '25%'), ('5', '30%'), ('6',
                                                                                '35%'), ('7', '40%'), ('8', '45%'), ('9', '50%'), ('10', '55%'),
        ('11', '60%'), ('12', '65%'), ('13', '70%'), ('14', '75%'), ('15',
                                                                     '80%'), ('16', '85%'), ('17', '90%'), ('18', '95%'), ('19', '100%')
    ], 'Abnormal Forms', tracking=True)

    semen_motility_after_30_min = fields.Char(
        'Motile After 30 minutes', tracking=True)
    semen_non_motility_after_30_min = fields.Char(
        'Non-Motile After 30 minutes', tracking=True)
    semen_motility_after_1_hour = fields.Char(
        'Motile After 1 hour', tracking=True)
    semen_non_motility_after_1_hour = fields.Char(
        'Non-Motile After 1 hour', tracking=True)
    semen_motility_after_2_hour = fields.Char(
        'Motile After 2 hour', tracking=True)
    semen_non_motility_after_2_hour = fields.Char(
        'Non-Motile After 2 hour', tracking=True)

    semen_progressive_activity_after_30_min = fields.Char(
        'Activity Progressive After 30 minutes', tracking=True)
    semen_sluggish_activity_after_30_min = fields.Char(
        'Activity Sluggish After 30 minutes', tracking=True)
    semen_progressive_activity_after_1_hour = fields.Char(
        'Activity Progressive After 1 hour', tracking=True)
    semen_sluggish_activity_after_1_hour = fields.Char(
        'Activity Sluggish After 1 hour', tracking=True)
    semen_progressive_activity_after_2_hour = fields.Char(
        'Activity Progressive After 2 hour', tracking=True)
    semen_sluggish_activity_after_2_hour = fields.Char(
        'Activity Sluggish After 2 hour', tracking=True)

    # -----chemecal section-------------
    semen_white_blood_cells = fields.Char(
        "White Blood Cells (WBC)", tracking=True)
    semen_red_blood_cells = fields.Char("Red Blood Cells (RBC)", tracking=True)
    semen_epithelial_cells = fields.Char("Epithelial Cells", tracking=True)
    semen_germ_cells = fields.Char("Germ Cells", tracking=True)

    # ------- comment section----------
    semen_comments = fields.Selection([
        ('1', 'AZOOSPERMIA. (No spermatozoa seen even after centrifugation.)'), ('2',
                                                                                 'Occasional motile and non-motile spermatozoa seen.'),
        ('3', 'Occasional motile spermatozoa seen.'),
        ('4', 'Occasional non-motile spermatozoa seen.'),
    ], "Comments", tracking=True)

    semen_head_defects = fields.Selection(semen_head_defects_list1,
                                          "Head defects 1", tracking=True)
    semen_head_defects_2 = fields.Selection(semen_head_defects_list2,
                                            "Head defects 2", tracking=True)
    semen_head_defects_3 = fields.Selection(semen_head_defects_list2,
                                            "Head defects 3", tracking=True)
    semen_head_defects_4 = fields.Selection(semen_head_defects_list2,
                                            "Head defects 4", tracking=True)

    semen_neck_midpiece_defects = fields.Selection(semen_neck_midpiece_defects_list1, "Neck/Midpiece defects 1", tracking=True)
    semen_neck_midpiece_defects_2 = fields.Selection(semen_neck_midpiece_defects_list2, "Neck/Midpiece defects 2", tracking=True)
    semen_neck_midpiece_defects_3 = fields.Selection(semen_neck_midpiece_defects_list2, "Neck/Midpiece defects 3", tracking=True)
    semen_neck_midpiece_defects_4 = fields.Selection(semen_neck_midpiece_defects_list2, tracking=True)

    semen_tail_defects = fields.Selection(semen_tail_defects_list1, "Tail defects 1", tracking=True)
    semen_tail_defects_2 = fields.Selection(semen_tail_defects_list2, "Tail defects 2", tracking=True)
    semen_tail_defects_3 = fields.Selection(semen_tail_defects_list2, "Tail defects 3", tracking=True)
    semen_tail_defects_4 = fields.Selection(semen_tail_defects_list2, "Tail defects 4", tracking=True)
    # end of semen test

    # Mycoplasma test
    is_mycoplasma_test = fields.Boolean(
        compute='func_is_mycoplasma_test', default=False, tracking=True)

    # culture test
    is_culture_test = fields.Boolean(
        compute='func_is_culture_test', default=False, tracking=True)

    mycoplasma_hominis = fields.Selection(
        [('1', 'No growth after 48 hours of incubation'), ('2', '≧10⁴ growth'), ], 'Mycoplasma hominis', tracking=True)
    mycoplasma_ureaplasma_urealyticum = fields.Selection(
        [('1', 'No growth after 48 hours of incubation'), ('2', '≧10⁴ growth')], 'Ureaplasma urealyticum', tracking=True)

    # --------Susceptibility (mg/L) _hominis-----
    mycoplasma_primycin = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Primycin (PRI)', tracking=True)
    mycoplasma_minocycline = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Minocycline (MIN)', tracking=True)
    mycoplasma_doxycycline = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Doxycycline (JOS)', tracking=True)
    mycoplasma_erythromycin = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Erythromycin (ERY)', tracking=True)

    mycoplasma_roxithromycin = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Roxithromycin (ROX)', tracking=True)
    mycoplasma_clindamycin = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Clindamycin (CLI)', tracking=True)
    mycoplasma_ofloxacin = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Ofloxacin (OFL)', tracking=True)
    mycoplasma_ciprofloxacin = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Ciprofloxacin (CIP)', tracking=True)

    mycoplasma_clarithromycin = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Clarithromycin (CLA)', tracking=True)
    mycoplasma_tetracycline = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Tetracycline (TET)', tracking=True)
    mycoplasma_levofloxacin = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Levofloxacin (LEV)', tracking=True)

  # --------Susceptibility (mg/L) _hominis-----

    mycoplasma_primycin_hominis = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Primycin (PRI)', tracking=True)
    mycoplasma_minocycline_hominis = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Minocycline (MIN)', tracking=True)
    mycoplasma_doxycycline_hominis = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Doxycycline (JOS)', tracking=True)
    mycoplasma_erythromycin_hominis = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Erythromycin (ERY)', tracking=True)

    mycoplasma_roxithromycin_hominis = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Roxithromycin (ROX)', tracking=True)
    mycoplasma_clindamycin_hominis = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Clindamycin (CLI)', tracking=True)
    mycoplasma_ofloxacin_hominis = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Ofloxacin (OFL)', tracking=True)
    mycoplasma_ciprofloxacin_hominis = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Ciprofloxacin (CIP)', tracking=True)

    mycoplasma_clarithromycin_hominis = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Clarithromycin (CLA)', tracking=True)
    mycoplasma_tetracycline_hominis = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Tetracycline (TET)', tracking=True)
    mycoplasma_levofloxacin_hominis = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Levofloxacin (LEV)', tracking=True)

    # --------Susceptibility (mg/L) _ureaplasma-----
    mycoplasma_primycin_ureaplasma = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Primycin (PRI)', tracking=True)
    mycoplasma_minocycline_ureaplasma = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Minocycline (MIN)', tracking=True)
    mycoplasma_doxycycline_ureaplasma = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Doxycycline (JOS)', tracking=True)
    mycoplasma_erythromycin_ureaplasma = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Erythromycin (ERY)', tracking=True)

    mycoplasma_roxithromycin_ureaplasma = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Roxithromycin (ROX)', tracking=True)
    mycoplasma_clindamycin_ureaplasma = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Clindamycin (CLI)', tracking=True)
    mycoplasma_ofloxacin_ureaplasma = fields.Selection(
        [('1', 'Susceptible'), ('2', 'Intermediate'), ('3', 'Resistant')], 'Ofloxacin (OFL)', tracking=True)
    mycoplasma_ciprofloxacin_ureaplasma = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Ciprofloxacin (CIP)', tracking=True)

    mycoplasma_clarithromycin_ureaplasma = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Clarithromycin (CLA)', tracking=True)
    mycoplasma_tetracycline_ureaplasma = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Tetracycline (TET)', tracking=True)
    mycoplasma_levofloxacin_ureaplasma = fields.Selection([('1', 'Susceptible'), (
        '2', 'Intermediate'), ('3', 'Resistant')], 'Levofloxacin (LEV)', tracking=True)

    # end of Mycoplasma
    is_urine_routine_without_micorscopy = fields.Boolean(
        default=False, compute='func_is_urine_routine_without_microscopy_test')

    def func_is_urine_routine_without_microscopy_test(self):
        for rec in self:
            if rec.test_id.has_special_test and rec.test_id.special_test == 'urine_routine_without_microscopy':
                rec.is_urine_routine_without_micorscopy = True
            else:
                rec.is_urine_routine_without_micorscopy = False

    # wet film test
    is_wet_film_test = fields.Boolean(
        compute='func_is_wet_film_test', default=False, tracking=True)
    white_blood_cells_wet_film = fields.Char(
        "White Blood Cells (WBC)", tracking=True)
    red_blood_cells_wet_film = fields.Char(
        "Red Blood Cells (RBC)", tracking=True)
    epithelial_cells_wet_film = fields.Selection(
        [('1', 'Nil'), ('2', 'Not seen'), ('3', 'Present'), ('4', 'Occasional'), ('5', 'Few'), ('6', '+'),
         ('7', '++'), ('8', '+++'), ('9', '++++')], string="Epithelial Cells", tracking=True)
    other_1_wet_film = fields.Selection([('1', "Bacteria"), ('2', "Yeast Cells"),
                                         ('3', "Budding Yeast Cells"), ('4',
                                                                        "Germ Cells"), ('5', "Monilia"),
                                         ('6', "Spermatozoa"), ('7', "Trichomonas vaginalis")], string="Other Findings", tracking=True)
    shape_1_wet_film = fields.Selection(
        [('1', 'Nil'), ('2', 'Not seen'), ('3', 'Present'), ('4', 'Occasional'), ('5', 'Few'), ('6', '+'),
         ('7', '++'), ('8', '+++'), ('9', '++++')],
        string="Quantity", tracking=True)
    other_2_wet_film = fields.Selection([('1', "Bacteria"), ('2', "Yeast Cells"),
                                         ('3', "Budding Yeast Cells"), ('4',
                                                                        "Germ Cells"), ('5', "Monilia"),
                                         ('6', "Spermatozoa"), ('7', "Trichomonas vaginalis")], string="Other Findings", tracking=True)
    shape_2_wet_film = fields.Selection(
        [('1', 'Nil'), ('2', 'Not seen'), ('3', 'Present'), ('4', 'Occasional'), ('5', 'Few'), ('6', '+'),
         ('7', '++'), ('8', '+++'), ('9', '++++')],
        string="Quantity", tracking=True)
    other_3_wet_film = fields.Selection([('1', "Bacteria"), ('2', "Yeast Cells"),
                                         ('3', "Budding Yeast Cells"), ('4',
                                                                        "Germ Cells"), ('5', "Monilia"),
                                         ('6', "Spermatozoa"), ('7', "Trichomonas vaginalis")], string="Other Findings", tracking=True)
    shape_3_wet_film = fields.Selection(
        [('1', 'Nil'), ('2', 'Not seen'), ('3', 'Present'), ('4', 'Occasional'), ('5', 'Few'), ('6', '+'),
         ('7', '++'), ('8', '+++'), ('9', '++++')],
        string="Quantity", tracking=True)
    other_4_wet_film = fields.Selection([('1', "Bacteria"), ('2', "Yeast Cells"),
                                         ('3', "Budding Yeast Cells"), ('4',
                                                                        "Germ Cells"), ('5', "Monilia"),
                                         ('6', "Spermatozoa"), ('7', "Trichomonas vaginalis")], string="Other Findings", tracking=True)
    shape_4_wet_film = fields.Selection(
        [('1', 'Nil'), ('2', 'Not seen'), ('3', 'Present'), ('4', 'Occasional'), ('5', 'Few'), ('6', '+'),
         ('7', '++'), ('8', '+++'), ('9', '++++')],
        string="Quantity", tracking=True)
    finding = fields.Boolean("No Trichomonas vaginalis seen", tracking=True)
    finding_wet_1 = fields.Boolean(
        "No Trichomonas vaginalis seen", tracking=True)
    finding_wet_2 = fields.Boolean("No Monilia seen", tracking=True)
    # end wet film test

    # start CELIAC test
    is_celiac_quick_test = fields.Boolean(default=False, tracking=True)
    celiac_quick_test = fields.Selection(
        [('negative', 'NEGATIVE'), ('positive', 'POSITIVE')], string="CELIAC QUICK TEST", tracking=True)
    # end CELIAC test
    # start  GONORRHEA (RAPID TEST)
    # is_gonorrhea_test =  fields.Boolean(compute='func_is_gonorrhea_test', default=False, tracking=True)
    # end  GONORRHEA (RAPID TEST)
    # end special test

    date_requested = fields.Datetime(string='Request Date')
    date_analysis = fields.Date(
        string='Test Date', default=fields.Date.context_today)
    released_date = fields.Datetime(string='Released Date', readonly=True)
    request_id = fields.Many2one(
        'ksc.laboratory.request', string='Lab Request', ondelete='restrict')
    laboratory_id = fields.Many2one('ksc.laboratory', related="request_id.laboratory_id", string='Laboratory',
                                    readonly=True, store=True)
    report = fields.Text(string='Test Report', tracking=True)
    note = fields.Text(string='Extra Info', tracking=True)
    sample_ids = fields.Many2many('ksc.patient.laboratory.sample', 'test_lab_sample_rel', 'test_id', 'sample_id',
                                  string='Test Samples')
    company_id = fields.Many2one('res.company', ondelete='restrict',
                                 string='Company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', readonly=True, default='draft', tracking=True)
    report_url = fields.Char(compute="get_report_url", store=True)

    _sql_constraints = [('name_company_uniq', 'unique(name,company_id)',
                         'Test Name must be unique per company !')]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'patient.laboratory.test')
        res = super(PatientLabTest, self).create(vals)
        return res

    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise UserError(
                    _("Lab Test can be delete only in Draft state."))
        return super(PatientLabTest, self).unlink()

    @api.onchange('request_id')
    def onchange_request_id(self):
        if self.request_id and self.request_id.date:
            self.date_requested = self.request_id.date

    def action_done(self):
        self.state = 'done'
        self.released_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.processed_by = self.env.user

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    def _compute_access_url(self):
        super(PatientLabTest, self)._compute_access_url()
        for rec in self:
            rec.access_url = '/my/lab_results/%s' % (rec.id)

    # --------------------result one-------------------------------

    def func_is_parameter(self):
        for rec in self:
            if rec.test_id.structure_selection == "parameter":
                rec.is_parameter = True
            else:
                rec.is_parameter = False

    def func_is_customize(self):
        for rec in self:
            if rec.test_id.structure_selection == "customize":
                return True
            else:
                return False

    def func_is_customize_and_culture_growth(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == "culture_and_growth":
                rec.is_customize_and_culture_growth = True
            else:
                rec.is_customize_and_culture_growth = False

    @api.onchange("has_2_bactria")
    def check_no_of_bacteria(self):
        for rec in self:
            if rec.has_2_bactria:
                rec.has_2_bactria = True
            else:
                rec.has_2_bactria = False
                rec.culture_2 = '11'
                rec.growth_of_2 = False
                self.result_ids.culture_growth_result_2 = False

    # @api.onchange("has_3_bactria")
    # def check_no_of_bacteria(self):
    #     for rec in self:
    #         if rec.has_3_bactria:
    #             rec.has_2_bactria = True
    #         else:
    #             rec.has_2_bactria = False

    def func_is_widal(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'widal':
                rec.is_widal = True
            else:
                rec.is_widal = False

    def func_is_normal_range_2(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.custom_reference == True:
                rec.is_normal_range_2 = True
            else:
                rec.is_normal_range_2 = False

    def func_is_brucella(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'brucella':
                rec.is_brucella = True
            else:
                rec.is_brucella = False

    def func_is_rpr(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'rpr':
                rec.is_rpr = True
            else:
                rec.is_rpr = False

    def func_is_polar(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'polar':
                rec.is_polar = True
            else:
                rec.is_polar = False

    def func_is_min_sec(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'min_sec':
                rec.is_min_sec = True
            else:
                rec.is_min_sec = False

    def func_is_inr(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'inr':
                rec.is_inr = True
            else:
                rec.is_inr = False

    def func_is_gram(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'gram':
                rec.is_gram = True
            else:
                rec.is_gram = False

    def func_is_malaria(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'malaria':
                rec.is_malaria = True
            else:
                rec.is_malaria = False

    def func_is_patient_and_control(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.has_patient_and_control == True:
                rec.is_patient_and_control = True
            else:
                rec.is_patient_and_control = False

    def func_is_pregnancy(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'pregnancy':
                rec.is_pregnancy = True
            else:
                rec.is_pregnancy = False

    def func_is_brucella_rose(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'brucella_rose':
                rec.is_brucella_rose = True
            else:
                rec.is_brucella_rose = False

    def func_is_UOM(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.custom_unit:
                rec.is_UOM = True
            else:
                rec.is_UOM = False

    def func_is_blood_group(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.special_result == 'blood_group':
                rec.is_blood_group = True
            else:
                rec.is_blood_group = False

    def func_is_special_test_and_sprcial_result_and_patient_control(self):
        for rec in self:
            if rec.test_id.has_patient_and_control or rec.test_id.has_special or rec.test_id.has_special_test:
                rec.is_special_test_and_sprcial_result_and_patient_control = True
            else:
                rec.is_special_test_and_sprcial_result_and_patient_control = False

    def func_fixed_table(self):
        for rec in self:
            if rec.test_id.has_fixed_table:
                rec.is_fixed_table = True
            else:
                rec.is_fixed_table = False

    # --------------------result two-------------------------------

    def func_has_two_result(self):
        for rec in self:
            if rec.test_id.has_two_structure:
                rec.has_two_result = True
            else:
                rec.has_two_result = False

    def func_is_patient_and_control_2(self):
        for rec in self:
            if rec.has_two_result and rec.test_id.has_patient_and_control_2:
                rec.is_patient_and_control_2 = True
            else:
                rec.is_patient_and_control_2 = False

    def func_is_polar_2(self):
        for rec in self:
            if rec.has_two_result and rec.test_id.special_result_2 == 'polar':
                rec.is_polar_2 = True
            else:
                rec.is_polar_2 = False

    def func_is_custom_reference_2(self):
        for rec in self:
            if rec.has_two_result and rec.test_id.custom_reference_2:
                rec.is_custom_reference_2 = True
            else:
                rec.is_custom_reference_2 = False

    # --------------------result three-------------------------------

    def func_has_three_result(self):
        for rec in self:
            if rec.test_id.has_three_structure:
                rec.has_three_result = True
            else:
                rec.has_three_result = False

    def func_is_min_sec_3(self):
        for rec in self:
            if rec.has_three_result and rec.test_id.special_result_3 == 'min_sec':
                rec.is_min_sec_3 = True
            else:
                rec.is_min_sec_3 = False

    def func_is_normal_range_3(self):
        for rec in self:
            if rec.has_three_result and rec.test_id.special_result_3 == 'min_sec':
                rec.is_normal_range_3 = True
            else:
                rec.is_normal_range_3 = False

    # ------------------------------- special test ----------------------

    def func_is_urine_routine_test(self):
        for rec in self:
            if rec.test_id.has_special_test and rec.test_id.special_test == 'urine_routine':
                rec.is_urine_routine_test = True
            else:
                rec.is_urine_routine_test = False

    def func_is_stool_routine_test(self):
        for rec in self:
            if rec.test_id.has_special_test and rec.test_id.special_test == 'stool_routine':
                rec.is_stool_routine_test = True
            else:
                rec.is_stool_routine_test = False

    def func_is_wet_film_test(self):
        for rec in self:
            if rec.test_id.has_special_test and rec.test_id.special_test == 'wet_film':
                rec.is_wet_film_test = True
            else:
                rec.is_wet_film_test = False

    def func_is_semen_test(self):
        for rec in self:
            if rec.test_id.has_special_test and rec.test_id.special_test == 'semen_analysis':
                rec.is_semen_test = True
            else:
                rec.is_semen_test = False

    def func_is_mycoplasma_test(self):
        for rec in self:
            if rec.test_id.has_special_test and rec.test_id.special_test == 'mycoplasma':
                rec.is_mycoplasma_test = True
            else:
                rec.is_mycoplasma_test = False

    def func_is_culture_test(self):
        for rec in self:
            if rec.test_id.special_result == 'culture_and_growth':
                rec.is_culture_test = True
            else:
                rec.is_culture_test = False

    # def func_is_celiac_quick_test(self):
    #     for rec in self:
    #         if rec.func_is_customize() and rec.test_id.custom_reference == True:
    #             rec.is_celiac_quick_test = True
    #         else:
    #             rec.is_celiac_quick_test = False

    # def func_is_gonorrhea_test(self):
    #     for rec in self:
    #         if rec.func_is_customize() and rec.test_id.custom_reference == True:
    #             rec.is_gonorrhea_test = True
    #         else:
    #             rec.is_gonorrhea_test = False

    def get_report_url(self):
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        for rec in self:
            url = base_url + \
                "/report/pdf/ksc_laboratory.lab_result_template/%s" % (rec.id)
            rec.report_url = url
            print('-------------------------------')
            print(url)
            print('-------------------------------')

    # =============new requirment 4-2-2024===========================
    # aso
    is_aso_test = fields.Boolean(
        compute='func_is_aso_test', default=False, tracking=False)

    def func_is_aso_test(self):
        for rec in self:
            if rec.test_id.product_id.name == "ASOT":
                rec.is_aso_test = True
            else:
                rec.is_aso_test = False
    # crp
    is_crp_test = fields.Boolean(
        compute='func_is_crp_test', default=False, tracking=False)

    def func_is_crp_test(self):
        for rec in self:
            if rec.test_id.product_id.name == "C-REACTIVE PROTEIN":
                rec.is_crp_test = True
            else:
                rec.is_crp_test = False

    # rf
    is_rf_test = fields.Boolean(
        compute='func_is_rf_test', default=False, tracking=False)

    def func_is_rf_test(self):
        for rec in self:
            if rec.test_id.product_id.name == "rheumatoid factor":
                rec.is_rf_test = True
            else:
                rec.is_rf_test = False

    # Gonorrhea
    is_gonorrhea_test = fields.Boolean(
        compute='func_is_gonorrhea_test', default=False, tracking=False)

    def func_is_gonorrhea_test(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.product_id.name == "GONORRHEA":
                rec.is_gonorrhea_test = True
            else:
                rec.is_gonorrhea_test = False

     # celiac
    is_celiac_test = fields.Boolean(
        compute='func_is_celiac_test', default=False, tracking=False)

    def func_is_celiac_test(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.product_id.name == "CELIAC QUICK TEST":
                rec.is_celiac_test = True
            else:
                rec.is_celiac_test = False

    # Alcohol
    is_alcohol_test = fields.Boolean(
        compute='func_is_alcohol_test', default=False, tracking=False)

    def func_is_alcohol_test(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.product_id.name == "ALCOHOL (Rapid Test)":
                rec.is_alcohol_test = True
            else:
                rec.is_alcohol_test = False

     # drugs
    is_drugs_test = fields.Boolean(
        compute='func_is_drugs_test', default=False, tracking=False)

    def func_is_drugs_test(self):
        for rec in self:
            if rec.func_is_customize() and rec.test_id.product_id.name == "Drugs":
                rec.is_drugs_test = True
            else:
                rec.is_drugs_test = False
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
