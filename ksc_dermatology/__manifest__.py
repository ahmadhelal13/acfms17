# -*- coding: utf-8 -*-
{
    'name': "dermatology",
    'author': "",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ksc_clinic_base', 'sale', 'ksc_prescription_model', 'ksc_rooster_type',
                'account', 'stock', 'contacts', 'mail', 'ksc_laboratory', 'ksc_radiology',
                'purchase', 'website_partner', 'crm', 'payment', 'ksc_physiotherapy',
                'ksc_patient_report'
                ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/medical_advice.xml',
        'report/medical_report.xml',
        'report/medical_history.xml',
        'report/special_report.xml',
        'report/dermatology_and_venerology.xml',
        'report/endorsement_laser_hair_removal.xml',
        'report/approval_of_filler_treatment.xml',
        'report/filler_instruction.xml',
        'report/derma_patient_file.xml',
        'report/approval_of_varicose_veins.xml',
        'report/potex_treatment.xml',
        'views/views.xml',
        'views/res_config.xml',
        'views/appointment.xml',
        'views/menu_item.xml',
        'views/hide_menu.xml',
    ],
}
