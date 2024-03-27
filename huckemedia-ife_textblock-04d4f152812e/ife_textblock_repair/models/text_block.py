from odoo import fields, models, api


class TextBlockItem(models.Model):
    _inherit = "text.block.item"

    repair_id = fields.Many2one(
        'repair.order',
        string="Repair",
        readonly=True
    )
    repair_pr_id = fields.Many2one(
        'repair.order',
        string="Repair Pr",
        readonly=True
    )

