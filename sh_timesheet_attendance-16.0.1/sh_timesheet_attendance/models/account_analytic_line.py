# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, _
from odoo.exceptions import UserError


class ShTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    sh_attendance_id = fields.Many2one('hr.attendance', string='Attendance')

    def open_attendance(self):
        if self and self.sh_attendance_id.id:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_id': self.env.ref('hr_attendance.hr_attendance_view_form').id,
                'res_model': 'hr.attendance',
                'target': 'current',
                'res_id': self.sh_attendance_id.id,
            }
        else:
            raise UserError(
                _("There is not any Attendance for this Timesheet !"))
