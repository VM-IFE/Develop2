# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    project_id = fields.Many2one("project.project", "Project")
    task_id = fields.Many2one("project.task", "Task")
    task_count = fields.Integer(compute='_compute_all_task_count')

    @api.model
    def default_get(self, fields_list):
        res = super(CalendarEvent, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'project.task':
            if self.env.context.get('active_id'):
                res.update({
                    'task_id': self.env.context.get('active_id'),
                })
                task_id = self.env['project.task'].sudo().browse(
                    self.env.context.get('active_id'))
                if task_id and task_id.project_id:
                    res.update({
                        'project_id': task_id.project_id.id
                    })
        return res

    def _compute_all_task_count(self):
        self.task_count = self.env['project.task'].search_count([
            ('id', '=', self.task_id.id)
        ])

    @api.model
    def create(self, vals):
        res = super(CalendarEvent, self).create(vals)
        if res.task_id:
            res.task_id.calendar_id = res.id
        return res

    @api.model
    def _get_public_fields(self):
        res = super(CalendarEvent, self)._get_public_fields()
        fields = ['project_id', 'task_id']
        for field in fields:
            res.add(field)
        return res


# Create Task from Calendar Meeting


    def create_task(self):
        self.ensure_one()
        return {
            'name': 'Create Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.task',
            'context': {'default_calendar_id': self.id},
            'type': 'ir.actions.act_window',
            'target': 'new'
        }
