# -*- coding: utf-8 -*-
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#    LeafByte
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
{
    'name': "Hr Attendance Calendar View v17",
    'summary': """Hr Attendance Calendar View v17.""",
    'category': 'Human Resources/Attendances',
    'version': '17.0.0.0',
    'description': """
        This module will add calendar view for hr.attendance 
    """,
    'author': "LeafByte",
    'website': "",
    'depends': ['base','hr_attendance'],
    'data': [
        'views/inherit_hr_attendance_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}
