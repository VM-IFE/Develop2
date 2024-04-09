odoo.define('webeditor_extras.toolbar_extras', function (require) {
    'use strict';

    const Toolbar = require('web_editor.toolbar');

    Toolbar.include({
        xmlDependencies: (Toolbar.prototype.xmlDependencies || []).concat(
            ['/webeditor_extras/static/src/xml/editor.xml']),
    });

});


