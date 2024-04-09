from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_ife_textblock_sale = fields.Boolean("Sale Textblock")
    module_ife_textblock_invoice = fields.Boolean("Invoice Textblock")
    module_ife_textblock_purchase = fields.Boolean("Purchase Textblock")
    module_ife_textblock_stock = fields.Boolean("Stock Textblock")
    module_ife_textblock_repair = fields.Boolean("Repair Textblock")
