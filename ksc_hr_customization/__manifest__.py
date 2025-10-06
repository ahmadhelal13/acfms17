# -*- coding: utf-8 -*-
{
    "name": "Ksc Hr Customization",
    "summary": "Ksc Hr Customization",
    "description": "Ksc Hr Customization",
    "author": "ASG.TEAM _ Ahmed Mokhtar",
    "website": "http://www.github.com/",
    "category": "Clinic",
    "version": "17.0.0.0.3",
    # any module necessary for this one to work correctly
    "depends": ["base", "hr", "hr_attendance", "hr_holidays"],
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/cron.xml",
        # reports
        "report/employee_lateness_report.xml",
        "report/warning_latter_report.xml",
        "report/interruption_from_work_report.xml",
        "report/late_latter_report.xml",
        "report/deduction_latter_report.xml",
        "report/ar_late_leave_request_latter_report.xml",
        "report/en_late_leave_request_latter_report.xml",
        # wizard
        "wizard/employee_monthly_view.xml",
        "wizard/warning_letter_wizard.xml",
        "wizard/en_permission_wizard.xml",
        "wizard/ar_permission_wizard.xml",
        "wizard/delay_memo_wizard.xml",
        "wizard/work_interruption_wizard.xml",
        "wizard/late_leave_request_wizard.xml",
        "wizard/deduction_letter_wizard.xml",
        # views
        "views/permission_request.xml",
        "views/employee_lateness.xml",
        "views/late_policy.xml",
        "views/hr_employee_view.xml",
        "views/hr_attendance.xml",
        "views/hr_leave_allocation_model.xml",
        "views/menu_items.xml",
    ],
}
