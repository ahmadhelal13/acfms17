# -*- coding: utf-8 -*-
{
    'name': "Prescription",
    'author': "ENG.Remon Salem",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ksc_clinic_base', 'contacts', 'base', 'ksc_patient_report'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/report.xml',
        'reports/prescription_list.xml',
        'reports/prescription_patient_file.xml',
        'views/view.xml',
        'views/menu_item.xml',
    ],
}
