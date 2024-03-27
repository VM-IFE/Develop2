{
    'name': 'IFE Textblock Stock',
    'version': '16.0.1.3.1',
    'author': 'IFE GmbH',
    'category': 'Customizations/Reports',
    'website': 'https://www.ife.de/',
    "license": "LGPL-3",
    'summary': 'Insert Textblock in Delivery Orders.',
    'depends': [
        'base',
        'stock',
        'ife_textblock',
    ],
    'data': [
        'views/stock_picking_form_view_ext.xml',
        'views/text_block_view.xml',

        'report/report_deliveryslip.xml',
        'report/report_stockpicking_operations.xml',
    ],
    'sequence': 666,
    'installable': True,
    'application': False,
}
