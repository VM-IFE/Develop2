# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    project_id = fields.Many2one('project.project', string='Project',store=True)
    task_id = fields.Many2one('project.task', string='Task', domain="[('project_id', '=', project_id)]",store=True)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update({
            'project_id': int(self.env['ir.config_parameter'].sudo().get_param('bi_automatic_timesheet_submit.project_id')),
            'task_id': int(self.env['ir.config_parameter'].sudo().get_param('bi_automatic_timesheet_submit.task_id')),
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        config_env = self.env['ir.config_parameter'].sudo()
        config_env.set_param('bi_automatic_timesheet_submit.project_id', self.project_id.id)
        config_env.set_param('bi_automatic_timesheet_submit.task_id', self.task_id.id)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
