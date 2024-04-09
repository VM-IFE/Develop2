# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    enable_auto_timesheet = fields.Boolean(string='Enable Auto TimeSheet')
    enable_auto_timesheet_submission = fields.Boolean(string='Auto Timesheet Submission')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task',domain="[('project_id', '=', project_id)]")
    description = fields.Char(string='Description')

    @api.onchange('enable_auto_timesheet')
    def onchange_enable_auto_timesheet(self):
        if self.enable_auto_timesheet:
            config_id = self.env['res.config.settings'].search([], limit=1).get_values()
            self.update({
                'project_id':config_id.get('project_id'),
                'task_id':config_id.get('task_id')})

class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    def unlink(self):
        self.timesheet_ids.unlink()
        return super(HrTimesheetSheet, self).unlink()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
