# -*- coding: utf-8 -*-
{
    'name': "Roster",
    'summary': 'Hospital Management System for managing Hospital and medical facilities flows',
    'description': """ Hospital Management System for managing Clinics, Hospitals and medical facilities """,
     "author": "ASG.TEAM",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['ksc_clinic_base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/nurse.xml',
        'views/receptionist.xml',
        'views/search_customize_of_patient_view.xml',
        'views/menu_item.xml',
    ],
}
