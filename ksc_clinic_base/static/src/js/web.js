odoo.define('acs_hms.FormRenderer', function (require) {
    "use strict";
    var FormRenderer = require('web.FormRenderer');
    const { blockUI, unblockUI } = require("web.framework");

    FormRenderer.include({
        /**
         * Disable statusbar buttons and stat buttons so that they can't be clicked anymore
         *
         */
        disableButtons: function () {
            blockUI()
            this.$('button').attr('disabled', true);
            setTimeout(unblockUI, 200);
        },
        /**
         * Enable statusbar buttons and stat buttons so they can be clicked again
         *
         */
        enableButtons: function () {
            this.$('button').removeAttr('disabled');
        },
    });
});