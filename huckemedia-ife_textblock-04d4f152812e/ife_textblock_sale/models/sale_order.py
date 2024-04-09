from odoo import models, fields, api, exceptions


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "Sales"

    above_text_block_item = fields.One2many(
        'text.block.item',
        'sale_order_id',
        string="Pre-Lines Textblocks",
        store=True
    )
    bottom_text_block_item = fields.One2many(
        'text.block.item',
        'sale_order_pr_id',
        string="Post-Lines Textblocks",
        store=True
    )
    template_id = fields.Many2one(
        'sale.order.template'
    )
    model = fields.Char(
        string='Model',
        default='sale.order',
    )
    model_id = fields.Many2many(
        'ir.model',
        compute='compute_model',
        string='Model records',
        store=True
    )

    @api.depends('model')
    def compute_model(self):
        model_id = self.env['ir.model'].search([('model', '=', 'sale.order')], limit=1)
        for record in self:
            if record.model:
                record.model_id = model_id

    def _compute_line_data_for_template_change(self, line):
        vals = super(SaleOrder, self)._compute_line_data_for_template_change(line)
        vals['text_block'] = line.text_block and line.text_block.id or False
        return vals


    @api.onchange('order_line')
    def onchange_product(self, sequence=99):
        textblock_obj = self.env['text.block.item']
        for line in self.order_line:
            if line.product_id.blocks_ids:
                for block in line.product_id.blocks_ids:
                    if block.preline_check:
                        textb_lock = textblock_obj.create({'sequence': sequence,
                                                           'template_textblock': block.textblock_ids.id,
                                                           'text': block.textblock_ids.text})
                        self.above_text_block_item = [(4, textb_lock.id)]
                    elif block.postline_check:
                        textb_lock = textblock_obj.create({'sequence': sequence,
                                                           'template_textblock': block.textblock_ids.id,
                                                           'text': block.textblock_ids.text})
                        self.bottom_text_block_item = [(4, textb_lock.id)]


    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        account_move = self.env.ref('account.model_account_move').id
        above_text_blocks = self.above_text_block_item.filtered(
            lambda t: t.show_in_invoice and account_move in t.model_id.ids)
        bottom_text_blocks = self.bottom_text_block_item.filtered(lambda t: t.show_in_invoice and account_move in t.model_id.ids)
        if above_text_blocks:
            result['above_text_block_item'] = [(6, 0, above_text_blocks.ids)]

        if bottom_text_blocks:
            result['bottom_text_block_item'] = [(6, 0, bottom_text_blocks.ids)]
        return result

    def convert_to_html(self, text_to_convert, order):
        """
        this function use the render_template of mail.template replacing template with an html field
        :return:
        """
        MailRendrerMixin = self.env['mail.render.mixin']
        text_record = MailRendrerMixin._render_template(text_to_convert,'sale.order',  order.ids, engine='inline_template')[order.id]
        return text_record


    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

            # reset textblock items on template onchange
            self.above_text_block_item = [(6, 0, [])]
            self.bottom_text_block_item = [(6, 0, [])]

            # get templates textblock
            above_text_block = template.above_text_block
            bottom_text_block = template.bottom_text_block

            # create above textblock sale
            if above_text_block:
                for above_text in above_text_block.sorted(lambda o: o.sequence):
                    above_text_sale = self.env['text.block.item'].create({'sale_order_id': self.id,
                                                                          'name': above_text.name,
                                                                          'template_textblock': above_text.id,
                                                                          'model': 'sale.order',
                                                                          'text': above_text.text,
                                                                          'sequence': above_text.sequence,
                                                                          'not_print':above_text.not_print,
                                                                          'page_break': above_text.page_break,
                                                                          })
                    above_text_sale._onchange_textblock()

            # create bottom textblock sale
            if bottom_text_block:
                for bottom_text in bottom_text_block.sorted(lambda o: o.sequence):
                    bottom_text_sale = self.env['text.block.item'].create({'sale_order_pr_id': self.id,
                                                                           'name': bottom_text.name,
                                                                           'template_textblock': bottom_text.id,
                                                                           'model': 'sale.order',
                                                                           'text': bottom_text.text,
                                                                           'sequence': bottom_text.sequence,
                                                                           'not_print': bottom_text.not_print,
                                                                           'page_break': bottom_text.page_break,
                                                                           })
                    bottom_text_sale._onchange_textblock()
        return super(SaleOrder, self)._onchange_sale_order_template_id()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sequence = fields.Integer(
        string='Sequence'
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
    text_block_item = fields.Many2one(
        'text.block.item',
        store=True,
        string="In-Lines Textblocks"
    )

    t_body = fields.Html(
        'Contents',
        store=True,
        sanitize_style=True,
        strip_classes=True
    )
    model = fields.Char(
        string='Model',
        default='sale.order.line',
    )
    model_id = fields.Many2many(
        'ir.model',
        compute='compute_model',
        string='Model records',
        store=True
    )

    @api.depends('model')
    def compute_model(self):
        model_id = self.env['ir.model'].search([('model', '=', 'sale.order.line')], limit=1)
        for record in self:
            if record.model:
                record.model_id = model_id

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        if res.product_id.is_textblock:
            res.product_uom_qty = 0.0
        if res.text_block_item:
            res.text_block_item.write({'sale_line_id': res.id})
        return res

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for record in self:
            if 'product_id' in vals:
                product = self.env['product.product'].search([('id', '=', vals.get('product_id'))], limit=1)
                if product and product.is_textblock:
                    record.product_uom_qty = 0.0
                    record.tax_id = [(4, 0, [])]
        return res

    @api.onchange('product_id')
    def onchange_product(self):
        textblock_obj = self.env['text.block.item']
        if self.product_id.blocks_ids:
            for block in self.product_id.blocks_ids:
                if block.inline_check:
                    self.text_block_item = textblock_obj.create({'sequence': self.id, 'sale_line_id': self.id,
                                                                 'template_textblock': block.textblock_ids.id,
                                                                 'text': block.textblock_ids.text})


    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        account_move = self.env.ref('account.model_account_move').id
        above_text_blocks = self.text_block_item.filtered(lambda t: t.show_in_invoice and account_move in t.model_id.ids)
        if above_text_blocks:
            res['text_block_item'] = self.text_block_item.id
        return res


    def _compute_line_data_for_template_change(self, line):
        vals = super(SaleOrderLine, self)._compute_line_data_for_template_change(line)
        vals['text_block'] = line.text_block and line.text_block.id or False
        return vals
