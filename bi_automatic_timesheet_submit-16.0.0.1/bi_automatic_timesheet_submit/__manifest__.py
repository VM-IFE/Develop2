# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Auto Create Timesheet from Attendance',
    'version': '16.0.0.1',
    "category": "Human Resources",
    'summary': 'Auto timesheet creation from attendance Auto timesheet create from attendance Auto submit timesheet from attendance automatic timesheet create via attendance timesheet creation from attendance timesheet creation via attendance auto timesheet create auto',
    'description': """
                    Odoo Timesheet,
                    Auto generate timesheet,
                    Auto generate timesheet from attendance,
                    auto submit timesheet,
                    auto generate and submit timesheet,
                    auto generate and submit timesheet from attendance,
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    'price': 19,
    'currency': "EUR",
    'depends': ['hr_attendance', 'bi_hr_timesheet_sheet'],
    'data': [
        'data/cron.xml',
        'views/res_config_settings.xml',
        'views/hr_employee.xml',
        'views/hr_attendance.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    "live_test_url": "https://youtu.be/Vy93-t4CcwY",
    'images': ["static/description/Banner.gif"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
