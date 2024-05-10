# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Project Task to Calendar and Calendar to Task Easy Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "category": "Project",
    "summary":
    "manage project task app, meeting from task module, create task from meeting, task management, meeting management, calendar to task odoo",
    "description":
    """This module allows Create Task from Meeting and Create Meeting from Task.""",
    "depends": ['project', 'calendar'],
    "data": [
        'views/project_task_calendar.xml',
        'views/calendar_event_views.xml',
    ],
    "images": [
        "static/description/background.jpg",
    ],
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "45",
    "currency": "EUR",
}
