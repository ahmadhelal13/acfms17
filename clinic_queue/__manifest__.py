# -*- coding: utf-8 -*-
{
    'name': "Clinic Queue",
    'author': "ASG Gulf",
    'category': 'Clinic',
    'version': '17.0.0.0.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'ksc_clinic_base', 'ksc_dental', 'ksc_dermatology', 'ksc_general_practitioner', 'ksc_genetics', 'ksc_internal_medicine',
                'ksc_nose_and_ear', 'ksc_nutrition', 'ksc_obstetrics_and_gynecology', 'ksc_ophthalmology', 'ksc_orthopedic',
                'ksc_pediatric', 'ksc_physiotherapy', 'ksc_radiology', 'ksc_urology', 'ksc_laboratory', 'purchase'
                ],

    # always loaded
    'data': [
        'data/data.xml',
        'views/view.xml',
        'report/queue_report.xml',
        'report/receipt_report.xml',
        'report/template.xml',
    ],
}
