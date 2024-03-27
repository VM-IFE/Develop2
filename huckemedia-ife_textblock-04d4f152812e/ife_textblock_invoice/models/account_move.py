from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = "Invoice"

    above_text_block_item = fields.One2many(
        'text.block.item', 'move_id',
        string="Pre-Lines Textblocks"
    )
    bottom_text_block_item = fields.One2many(
        'text.block.item',
        'move_pr_id',
        string="Post-Lines Textblocks 2"
    )
    customer_reference = fields.Char(
        'Customer Reference'
    )
    model = fields.Char(
        string='Model',
        default='account.move'
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
                model_id = self.env['ir.model'].search([('model', '=', 'account.move')], limit=1)
                record.model_id = model_id

    def convert_to_html(self, text_to_convert, order):
        """
        this function use the render_template of mail.template replacing template with an html field
        :return:
        """
        MailRendrerMixin = self.env['mail.render.mixin']
        text_record = MailRendrerMixin._render_template(text_to_convert,'account.move',  order.ids, engine='inline_template')[order.id]
        return text_record  

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    sequence = fields.Integer(
        string='Sequence'
    )
    model = fields.Char(
        string='Model',
        default='account.move.line',
    )
    text_block_item = fields.Many2one(
        'text.block.item',
        string="Text Block",
        index=True
    )
    t_body = fields.Html(
        'Contents',
        store=True,
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
                model_id = self.env['ir.model'].search([('model', '=', 'account.move.line')], limit=1)
                record.model_id = model_id

    @api.model_create_multi
    def create(self, vals):
        res = super(AccountMoveLine, self).create(vals)
        for move_line in res:
            if move_line.text_block_item:
                if move_line.text_block_item.text:
                    move_line.t_body = move_line.text_block_item.text
            if move_line.product_id.is_textblock:
                move_line.quantity = 0.0
        return res

    def write(self, vals):
        for record in self:
            if 'product_id' and 'text_block_item' in vals:
                text_block_item = self.env['text.block.item'].browse(vals['text_block_item'])
                if text_block_item.text:
                    record.t_body = text_block_item.text
            if 'product_id' in vals:
                product = self.env['product.product'].search([('id', '=', vals.get('product_id'))], limit=1)
                if product and product.is_textblock:
                    record.quantity = 0.0
        return super(AccountMoveLine, self).write(vals)

