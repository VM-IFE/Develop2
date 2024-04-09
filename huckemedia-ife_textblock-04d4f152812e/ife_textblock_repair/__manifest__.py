{
    'name': 'IFE Textblock Repair',
    'version': '16.0.1.3.1',
    'author': 'IFE GmbH',
    'category': 'Customizations/Reports',
    'website': 'https://www.ife.de/',
    "license": "LGPL-3",
    'summary': 'Insert Textblock in Repair.',
    'depends': [
        'base',
        'repair',
        'ife_textblock',
    ],
    'data': [
        'views/text_block_view.xml',
        'views/repair_view.xml',

        'report/repair_templates_repair_order.xml',
    ],
    'sequence': 666,
    'installable': True,
    'application': False,
}
