# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import datetime
from odoo.tools import format_datetime
from odoo import api, fields, models, exceptions, _


class AccountAnalyticLine(models.Model):
	_inherit = 'account.analytic.line'

	check_in = fields.Datetime("Check In")
	check_out = fields.Datetime("Check Out")


class HrAttendance(models.Model):
	_inherit = 'hr.attendance'

	check_in_date = fields.Date("Check In Date")
	check_out_date = fields.Date("Check Out Date")
	overtime_hours = fields.Float("Extra Hours", readonly=True)

	def auto_generate_timesheet(self):
		timesheet_env = self.env['hr_timesheet_sheet.sheet']
		today_date = datetime.datetime.today().date()
		temp = timesheet_env._default_date_from().split("-")
		chk_in_date = datetime.datetime.combine(datetime.date(int(temp[0]),int(temp[1]),int(temp[2])), datetime.time(0,0,0))
		temp = timesheet_env._default_date_to().split("-")
		chk_out_date = datetime.datetime.combine(datetime.date(int(temp[0]),int(temp[1]),int(temp[2])), datetime.time(23,59,59))
		attandance_ids = self.env["hr.attendance"].search([('check_in', '>=', chk_in_date),('check_out','<=',chk_out_date)])
		for attandance in attandance_ids:
			if attandance.check_out and attandance.employee_id.enable_auto_timesheet:
				timesheet_id = timesheet_env.search(
					[('state', '=', 'draft'), ('employee_id', '=', attandance.employee_id.id)])
				submitted_timesheet_id = timesheet_env.search(
					[('state', '=', 'confirm'), ('employee_id', '=', attandance.employee_id.id),
					 ('date_to', '=', today_date)])
				if submitted_timesheet_id:
					return True
				list = [(0, 0, {
					'date': today_date,
					'name': attandance.employee_id.description,
					'project_id': attandance.employee_id.project_id.id,
					'task_id': attandance.employee_id.task_id.id,
					'unit_amount': attandance.worked_hours,
					'employee_id': attandance.employee_id.id,
					'check_in': attandance.check_in,
					'check_out': attandance.check_out})]
				if timesheet_id:
					account_analytic_line_id = self.env['account.analytic.line'].search([
						('employee_id', '=', attandance.employee_id.id),
						('project_id', '=', attandance.employee_id.project_id.id),
						('check_in', '>=', attandance.check_in),
						('check_out', '<=', attandance.check_out),
						('unit_amount', '=', attandance.worked_hours)])
					for timesheet in timesheet_id:
						if not account_analytic_line_id:
							timesheet.update({'timesheet_ids': list})
				else:
					timesheet_env.create({
						'employee_id': attandance.employee_id.id,
						'date_from': timesheet_env._default_date_from(),
						'date_to': timesheet_env._default_date_to(),
						'timesheet_ids': list,
					})
			if attandance.employee_id.enable_auto_timesheet_submission:
				open_timesheet_id = False
				timesheet_id = timesheet_env.search(
					[('state', '=', 'draft'), ('employee_id', '=', attandance.employee_id.id),
					 ('date_to', '=', today_date)])
				if timesheet_id:
					for timesheet in timesheet_id:
						timesheet.action_timesheet_confirm()
						open_timesheet_id = timesheet_env.search(
							[('state', '=', 'draft'), ('employee_id', '=', attandance.employee_id.id), ('date_to', '<', timesheet_env._default_date_to())])
				if open_timesheet_id:
					for timesheet in open_timesheet_id:
						timesheet.action_timesheet_confirm()                        

	@api.model
	def create(self, vals):
		res = super(HrAttendance, self).create(vals)
		for data in res:
			if data.check_in:
				vals.update({
					'check_in_date': data.check_in.date()
				})
			if data.check_out:
				vals.update({
					'check_out_date': data.check_out.date()
				})
		attendance = self.env['hr.attendance'].search([
			('employee_id', '=', res.employee_id.id),
			('check_in', '<=', datetime.datetime.today().date()),
			('check_in', '>=', datetime.datetime.today().date())
		])
		if res != attendance:
			raise exceptions.ValidationError(
				_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in") % {
					'empl_name': res.employee_id.name,
				})
		return res

	def write(self, vals):
		res = super(HrAttendance, self).write(vals)
		attendance = self.env['hr.attendance'].search([
			('employee_id', '=', self.employee_id.id),
			('check_in', '<=', datetime.datetime.today().date()),
			('check_in', '>=', datetime.datetime.today().date())
		])
		if self != attendance:
			raise exceptions.ValidationError(
				_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in") % {
					'empl_name': self.employee_id.name,
				})
		return res
