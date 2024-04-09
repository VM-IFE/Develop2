{
    'name': 'IFE Textblock Invoice',
    'version': '16.0.1.7.1',
    'author': 'IFE GmbH',
    'category': 'Customizations/Reports',
    'website': 'https://www.ife.de/',
    "license": "LGPL-3",
    'summary': 'Insert Textblock in Invoices',
    'depends': [
        'base',
        'account',
        'ife_textblock',
        'account_reports',
    ],
    'data': [
        'views/account_move_view.xml',
        'views/text_block_view.xml',
        'report/report_invoice.xml',

    ],
    'sequence': 666,
    'installable': True,
    'application': False,
}
