from odoo import fields, models, api


class TextBlock(models.Model):
    _inherit = 'text.block'

    account_move_line_id = fields.Many2one(
        'account.move.line',
        string="Move Line",
        readonly=True,
    )


class TextBlockItem(models.Model):
    _inherit = "text.block.item"

    move_id = fields.Many2one(
        'account.move',
        string="Invoice",
        readonly=True,
    )
    move_pr_id = fields.Many2one(
        'account.move',
        string="Invoice Pr",
        readonly=True,
    )
    account_move_line_id = fields.Many2one(
        'account.move.line',
        string="Move Line",
    )

