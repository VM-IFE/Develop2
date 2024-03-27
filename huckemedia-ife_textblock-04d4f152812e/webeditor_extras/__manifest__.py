# -*- coding: utf-8 -*-
{
    'name': "Webeditor Extras",

    'description': "add option to toolbar text editor (to the wysiwyg web editor)",

    'author': "imad",
    'website': "",
    "license": "AGPL-3",

    
    'category': 'web editor',
    'version': '16.0.1.1',

    'depends': ['website','web_editor'],

    'data': [
    ],
    
    'assets' : {
        'web_editor.assets_wysiwyg': [
              'webeditor_extras/static/src/xml/editor.xml',
              'webeditor_extras/static/src/js/editor.js',
              'webeditor_extras/static/src/js/text_toolbar.js',
              'webeditor_extras/static/src/js/commands.js',
              'webeditor_extras/static/src/js/utils.js',
        ],
    }
}
