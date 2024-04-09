from odoo import api, fields, models, _


class TextBlock(models.Model):
    _name = 'text.block'
    _order = 'sequence'
    _description = 'Text block that can added to reports in related models'

    name = fields.Char(
        string='TextBlock'
    )
    model_id = fields.Many2many(
        comodel_name='ir.model',
        string='Model records',
        ondelete='cascade',
        required=True,
    )
    model = fields.Char(
        related='model_id.model',
        string='Model'
    )
    text = fields.Html(
        string='Text',
        translate=True
    )
    page_break = fields.Boolean(
        string="Page Break"
    )
    sequence = fields.Integer(
        string='Sequence',
        help="Gives the sequence order when displaying a list of textblock."
    )
    not_print = fields.Boolean(
       string="Not on Reports",
       help="If checked the textblock will not be print at documents."
    )

    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)

    company_ids = fields.Many2many(
        'res.company', 
        string='Companies'
    )


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # filtering record for companies selected
        if self.env.user.company_id:
            args += ['|',('company_ids', 'in',self.env.company.id),('company_ids', '=', False)]
        return super(TextBlock, self).search(args, offset, limit, order, count)
    

    def default_get(self, fields):
        res = super().default_get(fields)
        default_model_id = self._context.get('textblock_model')
        if default_model_id:
            model_id = self.env['ir.model'].search([('model', '=', default_model_id)], limit=1)
            res['model_id'] = [(6, 0, model_id.ids)]
        return res

class TextBlockItem(models.Model):
    _name = "text.block.item"
    _description = "Item Textblock"

    name = fields.Char(
        related='template_textblock.name',
        string='Name',
        readonly=True
    )
    model_id = fields.Many2many(
        related='template_textblock.model_id',
        string='Model records',
    )
    page_break = fields.Boolean(
        string="Page Break"
    )

    template_textblock = fields.Many2one(
        'text.block',
        string="Template"
    )
    model = fields.Char(
        string='Model',
        readonly=True
    )
    text = fields.Html(
        string='Text'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    not_print = fields.Boolean(
        string="Not on Reports",
        help="If checked the textblock will not be print at documents."
    )


    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)

    company_ids = fields.Many2many( 
        related='template_textblock.company_ids',
        string='Companies'
    )

    @api.onchange('template_textblock')
    def _onchange_textblock(self):
        if self.template_textblock:
            lang = self.env.user.lang
            record_partner_id = self.env.context.get('partner_id', False)
            if record_partner_id:
                lang = self.env['res.partner'].browse(record_partner_id)[0].lang

            self.text = self.template_textblock.with_context(lang=lang).text
            self.page_break = self.template_textblock.page_break
            self.not_print = self.template_textblock.not_print



class IrModel(models.Model):
    _inherit = "ir.model"

    color = fields.Integer('Color Index')
