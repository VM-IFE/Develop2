# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, _
from odoo.exceptions import UserError


class ShAttendance(models.Model):
    _inherit = 'hr.attendance'

    sh_timesheet_id = fields.Many2one(
        'account.analytic.line', string='Timesheet')
    sh_project_id = fields.Many2one(
        'project.project', string='Project')
    sh_task_id = fields.Many2one(
        'project.task', string='Task')

    def sh_create_timesheet(self):
        if self:
            if not self.check_out:
                raise UserError(
                    _("You are not allow to Create Timesheet without Check Out !"))
            else:
                if self.check_in and self.check_out:
                    diff = fields.Datetime.from_string(
                        self.check_out) - fields.Datetime.from_string(self.check_in)
                    if diff:
                        duration = float(diff.days) * 24 + \
                            (float(diff.seconds) / 3600)
                        total_hours = round(duration, 2)

                return {
                    'name': 'Create Timesheet',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sh.add.timesheet.wizard',
                    'target': 'new',
                    'context': {'default_sh_start': self.check_in,
                                'default_sh_stop': self.check_out,
                                'default_sh_employee_id': self.employee_id.id,
                                'default_duration': total_hours,
                                },
                }

    def open_timesheet(self):
        if self:
            timesheet_obj = self.env['account.analytic.line'].search(
                [('sh_attendance_id', '=', self.id)], limit=1)
            if timesheet_obj:
                return {
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'view_id': self.env.ref('hr_timesheet.timesheet_view_form_user').id,
                    'res_model': 'account.analytic.line',
                    'target': 'current',
                    'domain': [('sh_attendance_id', '=', self.id)],
                    'res_id': timesheet_obj.id,
                }
            else:
                raise UserError(
                    _("There is not any Timesheet for this Attendance !"))
