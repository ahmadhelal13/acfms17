# -*- coding: utf-8 -*-
{
    "name": "Attendance Call OpenApi",
    "author": "ENG.Ahmed Mokhtar",
    "website": "http://www.github.com/ahmedsayed100",
    "category": "APIs",
    "version": "17.0.0.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": [
        "openapi",
        "hr_attendance",
        "hr",
        "base_api",
        "base",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/employee_inherit.xml",
        "views/company_inherit.xml",
        "views/user_inherit.xml",
        # "views/attend.xml",
    ],
}
