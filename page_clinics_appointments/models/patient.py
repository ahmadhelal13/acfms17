from odoo import _, api, fields, models


class ClinicPatient(models.Model):
    _inherit = "res.partner"
    _description = 'Clinic Patient'

    dent_app_ids = fields.One2many('ksc.line.dental.appointment', 'patient_id')
    dermat_app_ids = fields.One2many(
        'ksc.line.dermatology.appointment', 'patient_id')
    pract_app_ids = fields.One2many(
        'ksc.line.practitioner.appointment', 'patient_id')
    medic_app_ids = fields.One2many(
        'ksc.line.medicine.appointment', 'patient_id')
    nose_ear_app_ids = fields.One2many(
        'ksc.line.nose_and_ear.appointment', 'patient_id')
    nut_app_ids = fields.One2many(
        'ksc.line.nutrition.appointment', 'patient_id')
    obs_app_ids = fields.One2many(
        'ksc.line.obstetrics_and_gynecology.appointment', 'patient_id')
    opth_app_ids = fields.One2many(
        'ksc.line.ophthalmology.appointment', 'patient_id')
    orth_app_ids = fields.One2many(
        'ksc.line.orthopedic.appointment', 'patient_id')
    pediat_app_ids = fields.One2many(
        'ksc.line.pediatric.appointment', 'patient_id')
    pyths_app_ids = fields.One2many(
        'ksc.line.physiotherapy.appointment', 'patient_id')
    urol_app_ids = fields.One2many(
        'ksc.line.urology.appointment', 'patient_id')
