odoo.define('webeditor_extras.text_toolbar', function (require) {
    "use strict";

    var core = require('web.core');
    var FieldTextHtml = require('web_editor.FieldTextHtml');

    FieldTextHtml.include({
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.toolbarOptions.buttons.push({
                    name: 'font_family',
                    icon: 'fa fa-font',
                    title: 'Font Family',
                    type: 'dropdown',
                    items: [
                        { name: 'Arial', text: 'Arial' },
                        { name: 'Verdana', text: 'Verdana' },
                        { name: 'Oswald', text: 'Oswald' },
                        { name: 'Raleway', text: 'Raleway' },
                        { name: 'Roboto', text: 'Roboto' },
                        { name: 'Tajawal', text: 'Tajawal' },
                        
                        // Add more font family options as needed
                    ],
                    onClick: self.setFontFamily.bind(self),
                });
            });
        },

        setFontFamily: function (ev) {
            // Get the selected font family option and apply it to the selected text or caret position
            var fontFamily = ev.target.dataset.name;
            this.format('fontName', fontFamily);
        },
    });

});