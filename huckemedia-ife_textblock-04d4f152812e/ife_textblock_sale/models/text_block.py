from odoo import fields, models, api


class TextBlock(models.Model):
    _inherit = 'text.block'

    sale_line_id = fields.Many2one(
        'sale.order.line',
        string="SO Line",
        readonly=True
    )
    not_print_custom_view = fields.Boolean(
        string="Not in Customer View",
        help="If checked the textblock will not be print at Customer View.",
        readonly=False
    )
    show_in_invoice = fields.Boolean(
        string="Show in Invoice",
        help="If checked the textblock will be shown in invoice.",
        readonly=False
    )


    @api.onchange('show_in_invoice')
    def _show_in_invoice(self):
        for record in self:
            account_move = self.env.ref('account.model_account_move')
            if record.show_in_invoice:
                if account_move not in record.model_id:
                    record.write({'model_id': [(4, account_move.id)]})


class TextBlockItem(models.Model):
    _inherit = "text.block.item"

    sale_order_id = fields.Many2one(
        'sale.order',
        string="SO",
        readonly=True)
    sale_order_pr_id = fields.Many2one(
        'sale.order',
        string="SO",
        readonly=True
    )
    sale_line_id = fields.Many2one(
        'sale.order.line',
        string="SO Line",
        readonly=True
    )
    not_print_custom_view = fields.Boolean(
        related='template_textblock.not_print_custom_view',
        string="Not in Customer View",
        help="If checked the textblock will not be print at Customer View.",
        readonly=False,
    )
    show_in_invoice = fields.Boolean(
        related="template_textblock.show_in_invoice",
        string="Show in Invoice",
        help="If checked the textblock will be shown in invoice.",
        readonly=False
    )
