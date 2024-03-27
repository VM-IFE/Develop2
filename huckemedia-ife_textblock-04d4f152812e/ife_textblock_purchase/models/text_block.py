from odoo import fields, models, api
    

class TextBlock(models.Model):
    _inherit = 'text.block'

    purchase_order_line_id = fields.Many2one(
        'purchase.order.line',
        string="Purchase Order Line",
        readonly=True,
    )


class TextBlockItem(models.Model):
    _inherit = "text.block.item"

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string="Purchase Order",
        readonly=True,
    )
    purchase_order_pr_id = fields.Many2one(
        'purchase.order',
        string="Purchase Order Pr",
        readonly=True,
    )
    purchase_order_line_id = fields.Many2one(
        'purchase.order.line',
        string="Purchase Order Line",
        readonly=True,
    )
