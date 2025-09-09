# -*- coding: utf-8 -*-
{
    'name': "Clinic",
    'summary': 'Hospital Management System for managing Hospital and medical facilities flows',
    'description': """ Hospital Management System for managing Clinics, Hospitals and medical facilities """,
    'author': "ENG.Remon Salem",
    'website': "http://www.github.com/remonSalem",
    'category': 'Clinic',
    'version': '17.0.0.0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['contacts', 'portal', 'sale', 'product', 'account', 'base', 'ksc_patient_report'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/patient_barcodelabels.xml',
        'report/payment_today_report.xml',
        'report/medical_advice.xml',
        'report/medical_report.xml',
        'report/invoice_A5.xml',
        'report/patient_common_info.xml',
        'report/patient_report.xml',
        'data/sequence.xml',
        'views/views.xml',
        'views/cron_job.xml',
        'views/appointment.xml',
        'views/payment.xml',
        'views/evaluation_view.xml',
        'wizard/wizard.xml',
        'wizard/patient_barcode_wizard.xml',
        'wizard/change_physician.xml',
        'views/menu_item.xml',
    ],

    # "assets": {
    #     "web.assets_backend": [
    #         "ksc_clinic_base/static/src/js/web_calendar.js",
    #         "ksc_clinic_base/static/src/js/calendar_view.js",
    #         "ksc_clinic_base/static/src/js/calendar_model.js",
    #         "ksc_clinic_base/static/src/js/calendar_renderer.js",
    #         "ksc_clinic_base/static/src/js/calendar_controller.js",
    #         "ksc_clinic_base/static/src/js/web.js",
    #     ],
    # },
    'qweb': ['static/src/xml/*.xml'],
}
