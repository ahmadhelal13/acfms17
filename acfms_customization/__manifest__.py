# -*- coding: utf-8 -*-
{
    'name': "ACFMS Customization",
    'summary': 'Hospital Management System for managing Hospital and medical facilities flows',
    'description': """ Hospital Management System for managing Clinics, Hospitals and medical facilities """,
    'author': "ENG.Remon Salem",
    'website': "http://www.github.com/remonSalem",
    'version': '17.0.0.0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['ksc_clinic_base', 'product', 'account'],

    # always loaded
    'data': [
        'data/civi_gender.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/customization.xml',
        'reports/payment_today_all_clinic.xml',
        'reports/payment_today_all_clinic_without_affia.xml',
    ],
}
