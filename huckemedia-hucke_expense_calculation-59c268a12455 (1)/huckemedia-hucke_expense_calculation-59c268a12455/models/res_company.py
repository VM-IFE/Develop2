from odoo import api, models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_de_document_title = fields.Char()

class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    l10n_de_document_title = fields.Char()