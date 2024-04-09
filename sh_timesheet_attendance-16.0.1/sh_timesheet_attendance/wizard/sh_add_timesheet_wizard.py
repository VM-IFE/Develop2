# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ShAddTimesheetWizard(models.TransientModel):
    _name = 'sh.add.timesheet.wizard'
    _description = 'Sh Add Timesheet Wizard'

    sh_date = fields.Date(default=lambda self: self._context.get(
        'Date', fields.Date.context_today(self)), required=True)
    sh_start = fields.Datetime(
        'Start', help="Start date of an event, without time for full days events", readonly=True)
    sh_stop = fields.Datetime(
        'Stop', help="Stop date of an event, without time for full days events", readonly=True)
    sh_project_id = fields.Many2one(
        'project.project', string='Project', required=True)
    sh_task_id = fields.Many2one('project.task', string='Task')
    sh_description = fields.Text('Description', required=True)
    sh_employee_id = fields.Many2one(
        'hr.employee', string='Employee', readonly=True)
    duration = fields.Float(readonly=True)

    def action_add_timesheet(self):
        entry_vals = {}
        context = dict(self._context or {})
        active_id = context.get('active_id', False)

        entry_vals.update({'date': self.sh_date,
                           'start': self.sh_start,
                           'stop': self.sh_stop,
                           'project_id': self.sh_project_id.id,
                           'task_id': self.sh_task_id.id,
                           'name': self.sh_description,
                           'employee_id': self.sh_employee_id.id,
                           'unit_amount': self.duration,
                           'sh_attendance_id': active_id,
                           })

        created_timesheet_id = self.env['account.analytic.line'].create(
            entry_vals)

        self.env['hr.attendance'].search(
            [('id', '=', active_id)], limit=1).sudo().write({'sh_timesheet_id': created_timesheet_id.id,
                                                             'sh_project_id': created_timesheet_id.project_id,
                                                             'sh_task_id': created_timesheet_id.task_id, })

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('hr_timesheet.timesheet_view_form_user').id,
            'res_model': 'account.analytic.line',
            'target': 'current',
            'res_id': created_timesheet_id.id,
        }
