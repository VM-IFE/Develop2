from odoo import api, models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    daily_rate_24h = fields.Float(string="Daily Rate - 24h", store=True, compute="_compute_values_city")
    daily_rate_8h = fields.Float(string="Daily Rate - 8h", store=True, compute="_compute_values_city")
    percentage_for_breakfast = fields.Integer(string="Percentage for Breakfast", store=True,
                                              compute="_compute_values_city")
    percentage_for_lunch = fields.Integer(string="Percentage for Lunch", )
    percentage_for_dinner = fields.Integer(string="Percentage for Dinner", store=True, compute="_compute_values_city")
    city_ids = fields.One2many('res.city', 'country_id',
                               string='Cities that refers to country')

    @api.depends("city_ids")
    def _compute_values_city(self):
        for record in self:
            daily_rate_24h = 0
            daily_rate_8h = 0
            percentage_for_breakfast = 0
            percentage_for_lunch = 0
            percentage_for_dinner = 0
            if record.city_ids:
                if len(record.city_ids) == 1:
                    daily_rate_24h = record.city_ids[0].daily_rate_24h
                    daily_rate_8h = record.city_ids[0].daily_rate_8h
                    percentage_for_breakfast = record.city_ids[0].percentage_for_breakfast
                    percentage_for_lunch = record.city_ids[0].percentage_for_lunch
                    percentage_for_dinner = record.city_ids[0].percentage_for_dinner

            record.daily_rate_24h = daily_rate_24h
            record.daily_rate_8h = daily_rate_8h
            record.percentage_for_breakfast = percentage_for_breakfast
            record.percentage_for_lunch = percentage_for_lunch
            record.percentage_for_dinner = percentage_for_dinner
