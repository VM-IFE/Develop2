# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class ShTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    start = fields.Datetime(
        help="Start date of an event, without time for full days events")
    stop = fields.Datetime(
        help="Stop date of an event, without time for full days events")

    def _get_duration(self, start, stop):
        """ Get the duration value between the 2 given dates. """
        if start and stop:
            diff = fields.Datetime.from_string(
                stop) - fields.Datetime.from_string(start)
            if diff:
                unit_amount = float(diff.days) * 24 + \
                    (float(diff.seconds) / 3600)
                return round(unit_amount, 2)
            return 0.0

    @api.onchange('start', 'stop')
    def onchange_duration_custom(self):
        if self and self.start and self.stop:
            start_date = self.start
            date = start_date.date()
            self.date = date
            self.unit_amount = self._get_duration(self.start, self.stop)
