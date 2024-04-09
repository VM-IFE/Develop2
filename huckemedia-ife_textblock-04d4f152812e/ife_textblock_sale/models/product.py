from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    blocks_ids = fields.One2many(comodel_name='product.list', inverse_name='list_id')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    blocks_ids = fields.One2many(comodel_name='product.list', inverse_name='list_id',
                                 related="product_tmpl_id.blocks_ids")


class ProductList(models.Model):
    _name = 'product.list'

    textblock_ids = fields.Many2one('text.block', string="TextBlock")
    preline_check = fields.Boolean('Pre-line')
    inline_check = fields.Boolean('In-line')
    postline_check = fields.Boolean('Post-line')
    list_id = fields.Many2one('product.template')


