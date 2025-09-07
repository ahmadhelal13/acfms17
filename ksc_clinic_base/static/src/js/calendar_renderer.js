odoo.define('ksc_clinic_base.CalendarRenderer', function (require) {
    "use strict";

    var CalendarRenderer = require('web.CalendarRenderer');
    var core = require('web.core');
    var session = require('web.session');

    var qweb = core.qweb;
    // var core = require('web.core');
    // var qweb = core.qweb;
    // var _t = core._t;
    CalendarRenderer.include({
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.column = params.column;
        },
        _getFullCalendarOptions: function () {
            var self = this;
            var fcOptions = this._super.apply(this, arguments);
            if (this.column) {
                fcOptions.plugins.push('resourceTimeGrid');
                fcOptions.resources = (info, resourceCB) => {
                    resourceCB(self.state.resources);
                };
                fcOptions.eventDrop = function (eventDropInfo) {
                    var event = self._convertEventToFC3Event(eventDropInfo.event);
                    if (eventDropInfo.newResource && eventDropInfo.newResource.id) {
                        event.resourceId = eventDropInfo.newResource.id;
                    }
                    self.trigger_up('dropRecord', event);
                };
                fcOptions.select = function (selectionInfo) {
                    // Clicking on the view, dispose any visible popover. Otherwise create a new event.
                    if (self.$('.o_cw_popover').length) {
                        self._unselectEvent();
                    }
                    var data = {start: selectionInfo.start, end: selectionInfo.end, allDay: selectionInfo.allDay};
                    if (self.state.context.default_name) {
                        data.title = self.state.context.default_name;
                    }
                    if (selectionInfo.resource && selectionInfo.resource.id) {
                        data.resourceID = selectionInfo.resource.id;
                    }
                    self.trigger_up('openCreate', self._convertEventToFC3Event(data));
                    if (self.state.scale === 'year') {
                        self.calendar.view.unselect();
                    } else {
                        self.calendar.unselect();
                    }
                };
                fcOptions.refetchResourcesOnNavigate = true;
            }
            return fcOptions;
        },
        _eventRender: function (event) {
            let color_index = event.extendedProps.color_index
            let record = event.extendedProps.record
            let filters = !!this.state.context.force_filters ? this.state.context.force_filters.filters : []
            let color_field = this.arch.attrs.color
            if (!!filters.length && !!color_field && record) {
                let value = record.hasOwnProperty(color_field) ? record[color_field] : false
                if (!!value) {
                    let item = filters.find(x => x.value == value);
                    if (!!item) {
                        color_index = item.color_index
                    }
                }
            }
            var qweb_context = {
                event: event,
                record: record,
                color: this.getColor(color_index),
                showTime: !self.hideTime && event.extendedProps.showTime,

                fields: this.state.fields,
                format: this._format.bind(this),
                read_only_mode: this.read_only_mode,
                user_context: session.user_context,
                widget: this,
            };
            this.qweb_context = qweb_context;
            if (_.isEmpty(qweb_context.record)) {
                return '';
            } else {
                return qweb.render("calendar-box", qweb_context);
            }
        },
        _convertEventToFC3Event: function (fc4Event) {
            var event = this._super.apply(this, arguments);
            if (fc4Event.resourceID) {
                event.resourceID = fc4Event.resourceID;
            }
            return event;
        }
    });
});
