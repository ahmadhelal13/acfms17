# -*- coding: utf-8 -*-
{
    'name': "Dental",
    'author': "ENG.Remon Salem",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ksc_clinic_base', 'ksc_prescription_model', 'ksc_rooster_type',
                'account', 'stock', 'contacts', 'mail', 'ksc_laboratory', 'ksc_radiology',
                'purchase', 'sale', 'website_partner', 'crm', 'payment', 'ksc_dermatology', 'ksc_physiotherapy',
                'ksc_patient_report'
                ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_config.xml',
        'views/appointment.xml',
        'views/dental_view.xml',
        'views/menu_item.xml',
        'views/dental_index.xml',
        'views/hide_menu.xml',
        'data/dental_data.xml',
        'data/teeth_code.xml',
        'data/child_teeth_code.xml',
        'reports/planned_operation.xml',
        'reports/treatment_plan_details.xml',
        'reports/ortho_plan.xml',
        'views/views.xml',
        'reports/medical_advice.xml',
        'reports/medical_report.xml',
        'reports/medical_history.xml',
        'reports/special_report.xml',
        'reports/dental_patient_file.xml',
        'reports/all_operation_report.xml',
    ],
    'qweb': [
        'static/src/xml/DentalView.xml',
    ],
}
