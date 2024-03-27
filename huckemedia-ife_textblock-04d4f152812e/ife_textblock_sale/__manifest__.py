{
    'name': 'IFE Textblock Sale',
    'version': '16.0.1.14.1',
    'author': 'IFE GmbH',
    'category': 'Customizations/Reports',
    'website': 'https://www.ife.de/',
    "license": "LGPL-3",
    'summary': 'Insert Textblock in Sales',
    'depends': [
        'base',
        'sale_management',
        'sales_team',
        'sale',
        'ife_textblock',
        'uom',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/sale_order_template_views.xml',
        'views/text_block_view.xml',
        'views/product_views.xml',

        'report/sale_report_template.xml',
        'report/sale_portal_templates.xml',

        'security/ir.model.access.csv',

    ],
    'sequence': 666,
    'installable': True,
    'application': False,
}
