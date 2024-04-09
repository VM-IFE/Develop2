from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = "Inventory"

    above_text_block_item = fields.One2many(
        'text.block.item',
        'picking_id',
        string="Text Block Top"
    )
    bottom_text_block_item = fields.One2many(
        'text.block.item',
        'picking_pr_id',
        string="Text Block Bottom"
    )
    model = fields.Char(
        string='Model',
        default='stock.picking',
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
                model_id = self.env['ir.model'].search([('model', '=', 'stock.picking')], limit=1)
                record.model_id = model_id

    def convert_to_html(self, text_to_convert, order):
        """
        this function use the render_template of mail.template replacing template with an html field
        :return:
        """
        MailRendrerMixin = self.env['mail.render.mixin']
        text_record = MailRendrerMixin._render_template(text_to_convert,'stock.picking',  order.ids, engine='inline_template')[order.id]
        return text_record  

