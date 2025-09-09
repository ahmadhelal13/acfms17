# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    clinic = fields.Selection(
        selection_add=[('obstetrics_and_gynecology', 'Obstetrics and Gynecology')])


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(
        selection_add=[('obstetrics_and_gynecology', 'Obstetrics and Gynecology')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('obstetrics_and_gynecology'):
            ids = self.env.company.obstetrics_and_gynecology_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    avalibel_in_obstetrics_and_gynecology = fields.Boolean()


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Account Journal'

    avalibel_in_obstetrics_and_gynecology = fields.Boolean()


class KSCServiceLine(models.Model):
    _inherit = "ksc.service.line"
    _description = "List of Services"

    obstetrics_and_gynecology_appt_id = fields.Many2one('ksc.obstetrics_and_gynecology.appointment', ondelete="cascade",
                                                        string='Appointment')

    def _compute_patient_id(self):
        super(KSCServiceLine, self)._compute_patient_id()
        for rec in self:
            if rec.obstetrics_and_gynecology_appt_id:
                rec.patient_id = rec.obstetrics_and_gynecology_appt_id.patient_id

    def _compute_clinic_name(self):
        super(KSCServiceLine, self)._compute_clinic_name()
        for rec in self:
            if rec.obstetrics_and_gynecology_appt_id:
                rec.clinic_name = rec.obstetrics_and_gynecology_appt_id.get_clinic_name()

# class KSCDiseases(models.Model):
#     _inherit = 'ksc.diseases'

#     obstetrics_and_gynecology_appt_id = fields.Many2one('ksc.obstetrics_and_gynecology.appointment', ondelete="cascade", string='Appointment')


class KscDiseasesLine(models.Model):
    _inherit = "ksc.diseases.line"

    obstetrics_and_gynecology_appt_id = fields.Many2one(
        'ksc.obstetrics_and_gynecology.appointment', ondelete="cascade", string='Obs&Gyn Appointment')


class KscObstetricsAndGynecologyAppointment(models.Model):
    _name = 'ksc.obstetrics_and_gynecology.appointment'
    _inherit = 'ksc.appointment'
    _description = 'Ksc Obstetrics And Gynecology Appointment'
    _order = "start_date desc"

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [
        ('readonly', True)]}
    service_line_ids = fields.One2many('ksc.service.line', 'obstetrics_and_gynecology_appt_id', string='Service Line', copy=False)
    # diseases_ids = fields.One2many('ksc.diseases', 'obstetrics_and_gynecology_appt_id')
    diseases_ids = fields.One2many(
        'ksc.diseases.line', 'obstetrics_and_gynecology_appt_id')
    clinic_name = fields.Char(default="obstetrics_and_gynecology")

    def name_of_clinic(self):
        return "obstetrics_and_gynecology"

    def get_available(self):
        return "avalibel_in_obstetrics_and_gynecology"

    @api.model
    def create(self, values):
        if values.get('name', 'New Appointment') == 'New Appointment':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'ksc.obstetrics_and_gynecology.appointment') or 'New Appointment'
        return super(KscObstetricsAndGynecologyAppointment, self).create(values)

    @api.model
    def _get_room_domain(self):
        return [('id', 'in', self.env.company.obstetrics_and_gynecology_room_ids.ids)]

    @api.model
    def _get_physician_domain(self):
        return [('id', 'in', self.env.company.obstetrics_and_gynecology_physician_ids.ids)]

    @api.model
    def _get_service_id(self):
        consultation = False
        if self.env.user.company_id.obstetrics_and_gynecology_consultation_product_id:
            consultation = self.env.user.company_id.obstetrics_and_gynecology_consultation_product_id.id
        return consultation

    def get_receptionist_clinic_group(self):
        return "ksc_obstetrics_and_gynecology.ksc_obstetrics_and_gynecology_receptionist"

    def get_nurse_clinic_group(self):
        return "ksc_obstetrics_and_gynecology.ksc_obstetrics_and_gynecology_nurse"

    def get_manager_clinic_group(self):
        return "ksc_obstetrics_and_gynecology.ksc_obstetrics_and_gynecology_manager"

    def get_doctor_clinic_group(self):
        return "ksc_obstetrics_and_gynecology.ksc_obstetrics_and_gynecology_doctor"

    def consultation_done(self):
        if self.diseases_ids:
            for disease in self.diseases_ids:
                self.patient_id.diseases_ids.create({
                    'name': disease.disease_id.name,
                    'patient_id': self.patient_id.id,
                    'obstetrics_and_gynecology_appt_id': self.id,
                })
        if self.service_line_ids:
            for service in self.service_line_ids:
                if not service.is_invoiced:
                    self.state = 'to_invoice'
                else:
                    self.state = 'done'
                    self.set_values_for_price_list()
        else:
            self.state = 'done'

    lmp = fields.Date(string="L.M.P")
    parity = fields.Char(string="PARITY")
    indication = fields.Text(string="INDICATION")

    size = fields.Selection(
        string='Size',
        selection=[('normal', 'Normal'),
                   ('enlarged', 'Enlarged'), ],
    )

    normal_size = fields.Char(string="Size")
    enlarged_size = fields.Selection(
        string='Enlarged Size',
        selection=[('uniform', 'Uniform'),
                   ('fibroid', 'Fibroid'), ],
    )

    enlarged_fibroid_size = fields.Selection(
        string='Enlarged Fibroid Size',
        selection=[('single', 'Single'),
                   ('multiple', 'Multiple'), ],
    )

    echopattern = fields.Selection(
        string='Echopattern',
        selection=[('normal', 'NORMAL'),
                   ('abnormal', 'ABNORMAL'), ],
    )
    endometrium = fields.Selection(
        string='Endometrium',
        selection=[('normal', 'NORMAL'),
                   ('abnormal', 'ABNORMAL'), ],
    )

    right_side = fields.Selection(
        string='Right',
        selection=[('normal', 'Normal'),
                   ('pco', 'Pco'),
                   ('ovarian', 'Ovarian Cyst'), ],
    )

    ovarian_cyst_right = fields.Selection(
        string='Ovarian Cyst',
        selection=[('cystic', 'Cystic '),
                   ('complex', 'Complex'),
                   ('size', 'Size'), ],
    )

    left_side = fields.Selection(
        string='Left',
        selection=[('normal', 'NORMAL'),
                   ('pco', 'Pco'),
                   ('ovarian', 'Ovarian'), ],
    )

    ovarian_cyst_left = fields.Selection(
        string='Ovarian Cyst',
        selection=[('cystic', 'Cystic '),
                   ('complex', 'Complex'),
                   ('size', 'Size'), ],
    )
    pod = fields.Selection(
        string='P.O.D',
        selection=[('normal', 'NORMAL'),
                   ('abnormal', 'Abnormal'), ],
    )

    ldd = fields.Date(string="L.D.D")
    ga = fields.Text(string="GA")

    pregnancy = fields.Selection(
        string='PREGNANCY',
        selection=[('single', 'Single'),
                   ('multiple', 'Multiple'), ],
    )

    cardiac_activity = fields.Selection(
        string='CARDIAC ACTIVITY',
        selection=[('present', 'Present'),
                   ('absent', 'Absent'), ],
    )

    presentation = fields.Selection(
        string='PRESENTATION',
        selection=[('cephalic', 'Cephalic'),
                   ('breech', 'Breech'),
                   ('transverse', 'TRANSVERSE'),
                   ('obliq', 'OBLIQ'),
                   ],
    )

    crl = fields.Char(string="CRL")
    gs = fields.Char(string="GS")
    bpd = fields.Char(string="BPD")
    hc = fields.Char(string="HC")
    ac = fields.Char(string="AC")
    fl = fields.Char(string="FL")
    fetal_weight = fields.Text(string="Fetal Weight")
    fetal_anomalies = fields.Selection(
        string='FETAL ANOMALIES',
        selection=[('absent', 'ABSENT'),
                   ('present', 'PRESENT'),
                   ],
    )

    placenta = fields.Selection(
        string='PLACENTA',
        selection=[('absent', 'ANT'),
                   ('present', 'POST'),
                   ('present', 'LAT'),
                   ('present', 'NORMAL'),
                   ('present', 'PREVIA'),
                   ],
    )
    specify = fields.Text(string="Specify")
    grade = fields.Selection(
        string='Grade',
        selection=[('i', 'I'),
                   ('ii', 'II'),
                   ('iii', 'III'),
                   ],
    )

    retro_placental_space = fields.Selection(
        string='RETRO PLACENTAL SPACE',
        selection=[('normal', 'NORMAL'),
                   ('abnormal', 'ABNORMAL'), ],
    )

    amniotic_fluid = fields.Selection(
        string='AMNIOTIC FLUID',
        selection=[('normal', 'NORMAL'),
                   ('abnormal', 'ABNORMAL'), ],
    )

    afi = fields.Char(string="AFI")
    impression = fields.Text(string="IMPRESSION")

    # ======================
    presenting_symptoms = fields.Text(string="Presenting Symptoms")
    history_of_present_illness = fields.Text(
        string="History of Present Illness")
    menstrual_history = fields.Text(string="Menstrual History")
    obstetric_history = fields.Text(string="Obstetric History")
    gynaecological_history = fields.Text(string="Gynaecological History")
    past_medical_history = fields.Text(string="Past Medical History")

    family_history = fields.Text(string="Family History")
    cervical_smear_history = fields.Text(string="Cervical Smear History")
    contraceptive_history = fields.Text(string="Contraceptive History")
    social_history = fields.Text(string="Social History")

    sexual_history = fields.Text(string="Sexual History")
    personal_history = fields.Text(string="Personal History")

    # =======physical exam====

    weight = fields.Char(string="Weight")
    height = fields.Char(string="Height")

    plus = fields.Char(string="Plus")
    temp = fields.Char(string="Temp")
    bp = fields.Text(string="BP")
    eyes = fields.Text(string="Eyes")
    tongue = fields.Text(string="Tongue")
    skin = fields.Text(string="Skin")
    pallor = fields.Text(string="Pallor")
    icterus = fields.Text(string="Icterus")

    generalized_lymphadenopathy = fields.Text(
        string="Generalized Lymphadenopathy")
    chest = fields.Text(string="Chest")
    breast = fields.Text(string="Breast")
    heart = fields.Text(string="Heart")
    abdomen = fields.Text(string="Abdomen")
    per_speculum_examination = fields.Text(string="Per Speculum Examination")

    pelvic = fields.Text(string="Bimanual Pelvic Examinaion")
    rectal_examination = fields.Text(string="Rectal Examination")

    investigations = fields.Text(string="Investigations")
    treatment = fields.Text(string="Treatment")


class ObstAndGynPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_obst_and_gyn_info_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['ksc.obstetrics_and_gynecology.appointment'].search(
            domain, order="start_date asc").ids
        # raise UserError(lab_ids)
        if lab_ids:
            return self.env.ref(
                'ksc_obstetrics_and_gynecology.obs_and_gyn__patient_file_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
