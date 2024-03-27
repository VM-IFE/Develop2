from odoo import models, fields, api, exceptions


class SaleOrderTemplateOption(models.Model):
    _inherit = 'sale.order.template.option'

    sequence = fields.Integer(
        string='Sequence'
    )
    pos = fields.Integer(
        'Pos.',
        related='sequence',
        store=True
    )
    image_1024 = fields.Binary(
        'Product-image',
        related='product_id.image_1024'
    )
    is_textblock = fields.Boolean(
        related='product_id.is_textblock',
        string='is TextBlock'
    )

    text_block = fields.Many2one(
        'text.block',
        string="Text Block"
    )
    t_body = fields.Html(
        related='text_block.text',
        string='Contents',
        store=True, default='',
        sanitize_style=True,
        strip_classes=True
    )
    model = fields.Char(
        string='Model',
        default='sale.order.template.option',
    )
    model_id = fields.Many2many(
        'ir.model',
        compute='compute_model',
        string='Model records'
    )

    @api.depends('model')
    def compute_model(self):
        for record in self:
            if not record.id:
                record.model_id = False
            elif record.model and record.id:
                model_id = self.env['ir.model'].search([('model', '=', 'sale.order.template.option')], limit=1)
                record.model_id = model_id

    @api.model
    def create(self, vals):
        res = super(SaleOrderTemplateOption, self).create(vals)
        if res.product_id.is_textblock:
            res.product_uom_qty = 0.0
        return res

    def write(self, vals):
        res = super(SaleOrderTemplateOption, self).write(vals)
        for record in self:
            if 'product_id' in vals:
                product = self.env['product.product'].search([('id', '=', vals.get('product_id'))], limit=1)
                if product and product.is_textblock:
                    record.product_uom_qty = 0.0
        return res
