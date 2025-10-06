# -*- coding: utf-8 -*-
{
    'name': "internal medicine",
    'summary': 'Hospital Management System for managing Hospital and medical facilities flows',
    'description': """ Hospital Management System for managing Clinics, Hospitals and medical facilities """,
     "author": "ASG.TEAM",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.2',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['ksc_clinic_base', 'ksc_prescription_model', 'ksc_rooster_type',
                'account', 'stock', 'contacts', 'mail', 'ksc_laboratory', 'ksc_radiology',
                'purchase', 'sale', 'website_partner', 'crm', 'payment', 'ksc_dermatology', 'ksc_physiotherapy', 'ksc_patient_report'
                ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/medical_advice.xml',
        'report/medical_report.xml',
        'report/medical_history.xml',
        'report/special_report.xml',
        'report/mdeicin_patient_file.xml',
        'views/views.xml',
        'views/res_config.xml',
        'views/appointment.xml',
        'views/menu_item.xml',
        'views/hide_menu.xml',
    ],
}
