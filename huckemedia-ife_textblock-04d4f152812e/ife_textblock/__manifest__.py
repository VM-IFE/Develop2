{
    'name': 'IFE Textblock Global',
    'version': '16.0.1.10.1',
    'author': 'IFE GmbH',
    'category': 'Customizations/Reports',
    'website': 'https://www.ife.de/',
    "license": "LGPL-3",
    'summary': 'Global Textblock',
    'depends': [
        'base',
        'base_setup',
        'product',
        'web',
        'web_editor',
    ],
    'data': [
        'data/products.xml',

        'views/text_block_view.xml',
        'views/res_config_settings.xml',
        'views/views.xml',

        'security/ir.model.access.csv'
    ],
    'assets': {
        'web.assets_backend': [
            'ife_textblock/static/src/css/li_style.css',
        ],
    },
    'sequence': 666,
    'installable': True,
    'application': False,
}
