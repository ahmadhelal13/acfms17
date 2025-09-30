# -*- coding: utf-8 -*-
{
    "name": "Ministry Monthly Report",
    "descrption": """
    This module is a customization for the ministry of health in Kuwait.
    """,
    "summary": """
    This module is a customization for the ministry of health in Kuwait.
    """,
    "sequence": 1,
    "author": "Eng Ahmed Mokhtar",
    "website": "http://www.github.com/ahmedelsayed100",
    "category": "ODOO 14",
    "version": "17.0.0.1.2",
    # any module necessary for this one to work correctly
    "depends": [
        "ksc_clinic_base",
        # clinics
        "ksc_clinic_base",
        "ksc_dental",
        "ksc_dermatology",
        "ksc_general_practitioner",
        "ksc_internal_medicine",
        "ksc_nose_and_ear",
        "ksc_nutrition",
        "ksc_obstetrics_and_gynecology",
        "ksc_ophthalmology",
        "ksc_orthopedic",
        "ksc_pediatric",
        "ksc_physiotherapy",
        "ksc_radiology",
        "ksc_urology",
    ],
    # always loaded
    "data": [
        # seucrity
        "security/ir.model.access.csv",
        # views
        # reports
        "reports/ministry_monthly_report.xml",
        "reports/ministry_monthly_report_of_phyicians.xml",
        # wizard
        "wizard/ministry_report_wizard.xml",
    ],
    "licence": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
