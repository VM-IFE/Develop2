{
    'name': 'IFE Textblock Purchase',
    'version': '16.0.1.4.1',
    'author': 'IFE GmbH',
    'category': 'Customizations/Reports',
    'website': 'https://www.ife.de/',
    "license": "LGPL-3",
    'summary': 'Insert Textblock in Purchase',
    'depends': [
        'base',
        'purchase',
        'ife_textblock',
    ],
    'data': [
        'views/purchase_order_view.xml',
        'views/text_block_view.xml',
        'report/purchase_quotation_report.xml',
        'report/purchase_report.xml',
    ],
    'sequence': 666,
    'installable': True,
    'application': False,
}
