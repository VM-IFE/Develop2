from odoo import fields, models, api


class TextBlockItem(models.Model):
    _inherit = "text.block.item"

    picking_id = fields.Many2one(
        'stock.picking',
        string="Picking",
        readonly=True
    )
    picking_pr_id = fields.Many2one(
        'stock.picking',
        string="Picking Pr",
        readonly=True
    )

