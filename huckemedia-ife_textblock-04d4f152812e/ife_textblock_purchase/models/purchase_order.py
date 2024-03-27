from odoo import models, fields, api, exceptions


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = "Purchase"

    above_text_block_item = fields.One2many(
        'text.block.item',
        'purchase_order_id',
        string="Pre-Lines Textblocks",
    )
    bottom_text_block_item = fields.One2many(
        'text.block.item',
        'purchase_order_pr_id',
        string="Post-Lines Textblocks"
    )
    model = fields.Char(
        string='Model',
        default='purchase.order',
    )
    model_id = fields.Many2many(
        'ir.model',
        compute='compute_model',
        string='Model records',
        store=True,
    )

    @api.depends('model')
    def compute_model(self):
        for record in self:
            if record.model:
                model_id = self.env['ir.model'].search([('model', '=', 'purchase.order')], limit=1)
                record.model_id = model_id

    def convert_to_html(self, text_to_convert, order):
        """
        this function use the render_template of mail.template replacing template with an html field
        :return:
        """
        MailRendrerMixin = self.env['mail.render.mixin']
        text_record = MailRendrerMixin._render_template(text_to_convert,'purchase.order',  order.ids, engine='inline_template')[order.id]
        return text_record  


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    model = fields.Char(
        string='Model',
        default='purchase.order.line',
    )
    text_block = fields.Many2one(
        'text.block',
        string="Text Block"
    )
    text_block_item = fields.Many2one(
        'text.block.item',
        string="Text Block Item"
    )
    t_body = fields.Html(
        'Contents',
        store=True,
        compute='compute_text',
        default='',
        sanitize_style=True,
        strip_classes=True
    )
    is_textblock = fields.Boolean(
        related='product_id.is_textblock',
        string='is TextBlock'
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
                model_id = self.env['ir.model'].search([('model', '=', 'purchase.order.line')], limit=1)
                record.model_id = model_id

    @api.depends('text_block_item.text')
    def compute_text(self):
        for record in self:
            if record.text_block_item.text:
                record.t_body = record.text_block_item.text
            else:
                record.t_body = ""

    @api.model
    def create(self, vals):
        res = super(PurchaseOrderLine, self).create(vals)
        if res.product_id.is_textblock:
            res.product_qty = 0.0
            res.taxes_id = [(6, 0, [])]
        return res

    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        for record in self:
            if 'product_id' in vals:
                product = self.env['product.product'].search([('id', '=', vals.get('product_id'))], limit=1)
                if product and product.is_textblock:
                    record.product_qty = 0.0
                    record.taxes_id = [(6, 0, [])]
        return res
