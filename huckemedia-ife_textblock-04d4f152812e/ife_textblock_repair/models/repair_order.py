from odoo import fields, models, api


class RepairOrder(models.Model):
    _inherit = 'repair.order'
    _description = "Repair"

    above_text_block_item = fields.One2many(
        'text.block.item',
        'repair_id',
        string="Pre-Lines Textblocks",
    )
    bottom_text_block_item = fields.One2many(
        'text.block.item',
        'repair_pr_id',
        string="Post-Lines Textblocks",
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Technician',
    )
    model = fields.Char(
        string='Model',
        default='repair.order',
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
                model_id = self.env['ir.model'].search([('model', '=', 'repair.order')], limit=1)
                record.model_id = model_id

    def convert_to_html(self, text_to_convert, order):
        """
        this function use the render_template of mail.template replacing template with an html field
        :return:
        """
        MailRendrerMixin = self.env['mail.render.mixin']
        text_record = MailRendrerMixin._render_template(text_to_convert,'repair.order',  order.ids, engine='inline_template')[order.id]
        return text_record  
