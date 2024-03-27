from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_textblock = fields.Boolean('is Textblock')
