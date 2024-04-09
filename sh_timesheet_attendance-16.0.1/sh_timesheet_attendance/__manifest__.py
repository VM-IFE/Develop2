# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': "Timesheet From Attendance",
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    "category": "Human Resources",
    'version': '16.0.1',
    "license": "OPL-1",
    "summary": "Timesheet Attendance,Timesheets From Attendance,Attendance From Timesheet,Timesheet from Attendance with Start and End Time,Schedule Timesheet,Timesheet By Week, Timesheet By Month, Timesheet With Calendar,manage timesheet,timesheet management Odoo",
    "description": """Throughout the day, when employees work on any project or task it is necessary to take the working details of the employee. so this module allows to create timesheet from the attendance. When checkout is done, you can create a timesheet by pressing the "Create Timesheet" button that is given on the attendance form. In the timesheet, you can mention the time used on each project.""",
    'depends': [
        'sh_timesheet_calendar', 'hr_attendance',
    ],
    'data': [
        'security/sh_timesheet_attendance_security.xml',
        'security/ir.model.access.csv',
        'views/hr_attendance_views.xml',
        'views/account_analytic_line_views.xml',
        'wizard/sh_add_timesheet_wizard_views.xml',
    ],
    'images': ['static/description/background.png', ],
    "price": 15,
    "currency": "EUR"
}
