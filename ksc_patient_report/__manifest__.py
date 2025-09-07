# -*- coding: utf-8 -*-
{
    'name': "Patient Report",
    'author': "ASG.TEAM",
    'website': "http://www.github.com/",
    'category': 'Clinic',
    'version': '17.0.0.0.1',
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': [

        'base',
        'contacts',
        # 'ksc_clinic_base',
        # 'sequence_reset_period'
        # 'ksc_radiology',
        # 'ksc_laboratory',
        # 'ksc_dental',
        # 'ksc_dermatology',
        # 'ksc_general_practitioner',
        # 'ksc_internal_medicine',
        # 'ksc_nose_and_ear',
        # 'ksc_nutrition',
        # 'ksc_obstetrics_and_gynecology',
        # 'ksc_ophthalmology',
        # 'ksc_orthopedic',
        # 'ksc_pediatric',
        # 'ksc_physiotherapy',
        # 'ksc_urology',
        # 'ksc_rooster_type',
        # 'ksc_prescription_model',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'report/patient_common_info.xml',
        # 'report/patient_report.xml',
        'views/view.xml',
        'wizard/wizard.xml'
        # 'report/dental_report.xml',
        # 'report/derma_patient_file.xml',
        # 'report/practitioner_patient_file.xml',
        # 'report/urology_patient_file.xml',
        # 'report/physio_patient_file.xml',
        # 'report/pediatric_patient_file.xml',
        # 'report/nose_ear_patient_file.xml',
        # 'report/mdeicin_patient_file.xml',
        # 'report/nutrition_patient_file.xml',
        # 'report/opth_patient_file.xml',
        # 'report/ortho_patient_file.xml',
    ],
}
