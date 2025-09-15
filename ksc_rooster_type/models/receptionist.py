# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, exceptions
from datetime import datetime

all_clinic = [('dental', 'Dental - عيادة الأسنان'), ('dermatology', 'Dermatology - عيادة الجلدية'), ('practitioner', 'Practitioner - عيادة الممارس العام'),
              ('medicine', 'Medicine - عيادة الباطنة'), ('nose_and_ear',
                                                         'Nose and ear - عيادة انف واذن'), ('nutrition', 'Nutrition - عيادة التغذية'),
              ('obstetrics_and_gynecology',
               'Obstetrics and gynecology - عيادة امراض النساء والتوليد'),
              ('ophthalmology', 'Ophthalmology عيادة طب العيون'), ('orthopedic',
                                                                   'Orthopedic - عيادة تقويم العظام'),
              ('pediatric', 'Pediatric - عيادة أطفال'), ('physiotherapy',
                                                         'Physiotherapy - عيادة العلاج الطبيعي'),
              ('laboratory', 'Laboratory - المعمل'),
              ('radiology', 'Radiology - مركز الأشعة'), ('urology', 'Urology - عيادة المسالك البولية')]


class ReceptionistGroupLine(models.Model):
    _name = 'receptionist.group.line'
    _description="receptionist group line"

    group_id = fields.Many2one('res.groups', 'Group Name')
    user_id = fields.Many2one('res.users')
    receptionist_id = fields.Many2one('rec.change')

    def delete_user(self):
        if self.group_id:
            self.group_id.users = [(3, self.user_id.id)]
            self.unlink()


class Change(models.Model):
    _name = 'rec.change'
    _description = 'change the clinic for Rec and receptionist'

    user_receptionist_id = fields.Many2one('res.users', string='Receptionist name', domain=[
                                           ('groups_id.name', '=', 'is_Receptionist')])
    clinic = fields.Selection(selection=all_clinic,
                              string='clinic type', default='dental')

    date = fields.Date(string='Date', default=datetime.today())
    user_id = fields.Many2one('res.users', string='Created by',
                              default=lambda self: self.env.uid, readonly=True)
    group_ids = fields.One2many(
        'receptionist.group.line', 'receptionist_id', readonly=True)

    def onchange_group_id(self):
        group_ids = []
        receptionist_group_ids = self.env['res.groups'].search(
            [('name', '=', 'Receptionist')])
        if self.user_receptionist_id:
            for group_id in receptionist_group_ids:
                if group_id not in self.group_ids.group_id:
                    for user in group_id.users:
                        if user.name == self.user_receptionist_id.name:
                            group_ids.append((0, 0, {
                                'group_id': group_id.id,
                                'user_id': self.user_receptionist_id.id,
                            }))
                else:
                    pass
            self.group_ids = group_ids

    @api.constrains('user_receptionist_id', 'clinic')
    def _check_duplicate(self):
        check = self.env['rec.change'].search(
            [('user_receptionist_id', '=', self.user_receptionist_id.name), ('clinic', '=', self.clinic)])
        if len(check) > 1:
            raise exceptions.ValidationError("this record is already exist")

    def action_receptionist(self):
        users = self.env['res.users'].search(
            [('name', '=', self.user_receptionist_id.name)])
        if self.clinic == 'dental':
            dental_group = self.env.ref('ksc_dental.ksc_dental_receptionist')
            dental_group.users = [(4, users.id)]
        elif self.clinic == 'dermatology':
            dermatology_group = self.env.ref(
            'ksc_dermatology.ksc_dermatology_receptionist')
            dermatology_group.users = [(4, users.id)]
        elif self.clinic == 'pediatric':
            pediatric_group = self.env.ref(
            'ksc_pediatric.ksc_pediatric_receptionist')
            pediatric_group.users = [(4, users.id)]
        elif self.clinic == 'radiology':
            radiology_group = self.env.ref(
            'ksc_radiology.ksc_radiology_receptionist')
            radiology_group.users = [(4, users.id)]
        elif self.clinic == 'urology':
            urology_group = self.env.ref('ksc_urology.ksc_urology_receptionist')
            urology_group.users = [(4, users.id)]
        elif self.clinic == 'practitioner':
            general_practitioner_group = self.env.ref(
            'ksc_general_practitioner.ksc_practitioner_receptionist')
            general_practitioner_group.users = [(4, users.id)]
        elif self.clinic == 'medicine':
            internal_medicine_group = self.env.ref(
            'ksc_internal_medicine.ksc_medicine_receptionist')
            internal_medicine_group.users = [(4, users.id)]
        elif self.clinic == 'nose_and_ear':
            nose_and_ear_group = self.env.ref(
            'ksc_nose_and_ear.ksc_nose_and_ear_receptionist')
            nose_and_ear_group.users = [(4, users.id)]
        elif self.clinic == 'nutrition':
            nutrition_group = self.env.ref(
            'ksc_nutrition.ksc_nutrition_receptionist')
            nutrition_group.users = [(4, users.id)]
        elif self.clinic == 'ophthalmology':
            ophthalmology_group = self.env.ref(
            'ksc_ophthalmology.ksc_ophthalmology_receptionist')
            ophthalmology_group.users = [(4, users.id)]
        elif self.clinic == 'obstetrics_and_gynecology':
            obstetrics_and_gynecology_group = self.env.ref(
            'ksc_obstetrics_and_gynecology.ksc_obstetrics_and_gynecology_receptionist')
            obstetrics_and_gynecology_group.users = [(4, users.id)]
        elif self.clinic == 'physiotherapy':
            physiotherapy_group = self.env.ref(
            'ksc_physiotherapy.ksc_physiotherapy_receptionist')
            physiotherapy_group.users = [(4, users.id)]
        elif self.clinic == 'orthopedic':
            orthopedic_group = self.env.ref(
            'ksc_orthopedic.ksc_orthopedic_receptionist')
            orthopedic_group.users = [(4, users.id)]
        elif self.clinic == 'laboratory':
            laboratory_group = self.env.ref(
            'ksc_laboratory.ksc_laboratory_receptionist')
            laboratory_group.users = [(4, users.id)]

        self.onchange_group_id()
