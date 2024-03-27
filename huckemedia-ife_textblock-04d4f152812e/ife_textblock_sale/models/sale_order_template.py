from odoo import models, fields, api, exceptions


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    above_text_block = fields.Many2many(
        'text.block',
        'sale_order_template_text_block_above',
        string="Text Block"
    )
    bottom_text_block = fields.Many2many(
        'text.block',
        'sale_order_template_text_block_bottom',
        string="Text Block"
    )
    customer_reference = fields.Char(
        'Customer Reference'
    )
    model = fields.Char(
        string='Model',
        default='sale.order.template',
    )
    model_id = fields.Many2many(
        'ir.model',
        compute='compute_model',
        string='Model records',
        store=True
    )

    @api.depends('model')
    def compute_model(self):
        for record in self:
            if record.model:
                model_id = self.env['ir.model'].search([('model', '=', record.model)], limit=1)
                record.model_id = model_id

