# -*- coding: utf-8 -*-
{
    'name': "Prescription",
    'summary': 'Hospital Management System for managing Hospital and medical facilities flows',
    'description': """ Hospital Management System for managing Clinics, Hospitals and medical facilities """,
    'author': "ENG.Remon Salem",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.1',
    'license': 'LGPL-3',
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
