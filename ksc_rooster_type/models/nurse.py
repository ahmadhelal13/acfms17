# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, exceptions
from datetime import datetime


class NurseGroupLine(models.Model):
    _name = 'nurse.group.line'
    _description="nurse group line"

    group_id = fields.Many2one('res.groups', 'Group Name')
    user_id = fields.Many2one('res.users')
    nurse_id = fields.Many2one('nurse.group')

    def delete_user(self):
        if self.group_id:
            self.group_id.users = [(3, self.user_id.id)]
            self.unlink()


class Change(models.Model):
    _name = 'nurse.change'
    _description = 'change the clinic for Rec and nurse'

    user_nurse_id = fields.Many2one('res.users', string='Nurse name', domain=[
                                    ('groups_id.name', '=', 'is_Nurse')])
    clinic = fields.Selection([('dental', 'Dental - عيادة الأسنان'), ('dermatology', 'Dermatology - عيادة الجلدية'), ('practitioner', 'Practitioner - عيادة الممارس العام'),
                               ('medicine', 'Medicine - عيادة الباطنة'), ('nose_and_ear',
                                                                          'Nose and ear - عيادة انف واذن'), ('nutrition', 'Nutrition - عيادة التغذية'),
                               ('obstetrics_and_gynecology',
                                'Obstetrics and gynecology - عيادة امراض النساء والتوليد'),
                               ('ophthalmology', 'Ophthalmology عيادة طب العيون'), (
                                   'orthopedic', 'Orthopedic - عيادة تقويم العظام'),
                               ('pediatric', 'Pediatric - عيادة أطفال'), ('physiotherapy',
                                                                          'Physiotherapy - عيادة العلاج الطبيعي'),
                               ('radiology', 'Radiology - مركز الأشعة'), ('urology', 'Urology - عيادة المسالك البولية')], string='clinic type',
                              default='dental')
    date = fields.Date(string='Date', default=datetime.today())
    user_id = fields.Many2one('res.users', string='Created by',
                              default=lambda self: self.env.uid, readonly=True)
    group_ids = fields.One2many('nurse.group.line', 'nurse_id', readonly=True)

    def onchange_group_id(self):
        group_ids = []
        nurse_group_ids = self.env['res.groups'].search(
            [('name', '=', 'Nurse')])
        if self.user_nurse_id:
            for group_id in nurse_group_ids:
                if group_id not in self.group_ids.group_id:
                    for user in group_id.users:
                        if user.name == self.user_nurse_id.name:
                            group_ids.append((0, 0, {
                                'group_id': group_id.id,
                                'user_id': self.user_nurse_id.id,
                            }))
                else:
                    pass
            self.group_ids = group_ids

    @api.constrains('user_nurse_id', 'clinic')
    def _check_duplicate(self):
        check = self.env['nurse.change'].search(
            [('user_nurse_id', '=', self.user_nurse_id.name), ('clinic', '=', self.clinic)])
        if len(check) > 1:
            raise exceptions.ValidationError("this record is already exist")

    def action_nurse(self):
        users = self.env['res.users'].search(
            [('login', '=', self.user_nurse_id.login)])
        if self.clinic == 'dental':
            dental_group = self.env.ref('ksc_dental.ksc_dental_nurse')
            dental_group.users = [(4, users.id)]
        elif self.clinic == 'dermatology':
            dermatology_group = self.env.ref(
                'ksc_dermatology.ksc_dermatology_nurse')
            dermatology_group.users = [(4, users.id)]
        elif self.clinic == 'pediatric':
            pediatric_group = self.env.ref('ksc_pediatric.ksc_pediatric_nurse')
            pediatric_group.users = [(4, users.id)]
        elif self.clinic == 'radiology':
            radiology_group = self.env.ref('ksc_radiology.ksc_radiology_nurse')
            radiology_group.users = [(4, users.id)]
        elif self.clinic == 'urology':
            urology_group = self.env.ref('ksc_urology.ksc_urology_nurse')
            urology_group.users = [(4, users.id)]
        elif self.clinic == 'practitioner':
            general_practitioner_group = self.env.ref(
                'ksc_general_practitioner.ksc_practitioner_nurse')
            general_practitioner_group.users = [(4, users.id)]
        elif self.clinic == 'medicine':
            internal_medicine_group = self.env.ref(
                'ksc_internal_medicine.ksc_medicine_nurse')
            internal_medicine_group.users = [(4, users.id)]
        elif self.clinic == 'nose_and_ear':
            nose_and_ear_group = self.env.ref(
                'ksc_nose_and_ear.ksc_nose_and_ear_nurse')
            nose_and_ear_group.users = [(4, users.id)]
        elif self.clinic == 'nutrition':
            nutrition_group = self.env.ref('ksc_nutrition.ksc_nutrition_nurse')
            nutrition_group.users = [(4, users.id)]
        elif self.clinic == 'ophthalmology':
            ophthalmology_group = self.env.ref(
                'ksc_ophthalmology.ksc_ophthalmology_nurse')
            ophthalmology_group.users = [(4, users.id)]
        elif self.clinic == 'obstetrics_and_gynecology':
            obstetrics_and_gynecology_group = self.env.ref(
                'ksc_obstetrics_and_gynecology.ksc_obstetrics_and_gynecology_nurse')
            obstetrics_and_gynecology_group.users = [(4, users.id)]
        elif self.clinic == 'physiotherapy':
            physiotherapy_group = self.env.ref(
                'ksc_physiotherapy.ksc_physiotherapy_nurse')
            physiotherapy_group.users = [(4, users.id)]
        elif self.clinic == 'orthopedic':
            orthopedic_group = self.env.ref(
                'ksc_orthopedic.ksc_orthopedic_nurse')
            orthopedic_group.users = [(4, users.id)]

        self.onchange_group_id()
