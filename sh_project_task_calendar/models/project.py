# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    calendar_id = fields.Many2one("calendar.event", "Calendar")
    meetings_count = fields.Integer(compute='_compute_all_meeting_count')

    @api.model
    def create(self, vals):
        res = super(ProjectTask, self).create(vals)
        if res.calendar_id:
            res.calendar_id.task_id = res.id
        return res

    def _compute_all_meeting_count(self):
        if self:
            for rec in self:
                rec.meetings_count = self.env['calendar.event'].search_count([
                    ('task_id', '=', rec.id)
                ])

    def get_calendar_records(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Meetings",
            "view_mode": "tree,form",
            "res_model": "calendar.event",
            "domain": [("task_id", "=", self.id)],
        }

# Create Meeting from Task

    def create_meeting(self):
        self.ensure_one()
        return {
            'name': 'Create Meeting',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'calendar.event',
            'context': {'default_task_id': self.id},
            'type': 'ir.actions.act_window',
            'target': 'new'
        }


class ProjectProject(models.Model):
    _inherit = 'project.project'

    meetings_count = fields.Integer(compute='_compute_all_meeting_count')

    def _compute_all_meeting_count(self):
        self.meetings_count = self.env['calendar.event'].search_count([
            ('project_id', '=', self.id)
        ])
