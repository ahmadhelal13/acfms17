# -*- coding: utf-8 -*-
{
    'name': "physiotherapy",
    'author': "ENG.Remon Salem",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ksc_clinic_base', 'ksc_prescription_model', 'ksc_rooster_type', 'product',
                'account', 'stock', 'contacts', 'mail', 'ksc_laboratory', 'ksc_radiology',
                'purchase', 'sale', 'website_partner', 'crm', 'payment', 'ksc_patient_report'
                ],

    # always loaded
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/medical_advice.xml',
        'report/medical_report.xml',
        'report/medical_history.xml',
        'report/special_report.xml',
        'report/physio_patient_file.xml',
        'views/res_config.xml',
        'views/appointment.xml',
        'views/physiotherapy_view.xml',
        'views/treatment_plan.xml',
        'views/views.xml',
        'views/date_template.xml',
        'views/menu_item.xml',
        'views/hide_menu.xml',
    ],
}
