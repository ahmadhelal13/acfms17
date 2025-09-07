odoo.define('ksc_clinic_base.CalendarModel', function (require) {
    "use strict";

    var CalendarModel = require('web.CalendarModel');
    var localStorage = require('web.local_storage');

    CalendarModel.include({
        load: function (params) {
            this.fieldColumn = params.fieldColumn;
            this.forceFilters = params.forceFilters;
            return this._super.apply(this, arguments);
        },
        _loadCalendar: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._compute_columns(self.data, self.data.data);
            });
        }, 
        _getFilterDomain: function () {
            this._compute_filters();
            return this._super.apply(this, arguments);
        },
        _loadRecordsToFilters: function (element, events) {
            let res = this._super.apply(this, arguments)
            this._compute_filters();
            return res
        },
        changeFilter: function (filter) {
            localStorage.setItem(filter.value, filter.active)
            return this._super.apply(this, arguments);
        },
        _compute_filters: function () {
            if (this.data.filters && this.forceFilters) {
                let fieldName = this.data.filters[this.forceFilters.fieldName]
                if (fieldName) {
                    let filters = []
                    this.forceFilters.filters.map(obj => {
                        let active = localStorage.getItem(obj.value) == 'true'
                        filters.push({
                            'color_index': obj.color_index,
                            'value': obj.value,
                            'label': obj.label,
                            'avatar_model': undefined,
                            'active': active,
                            'display': true,
                        })
                    });
                    this.data.filters[this.forceFilters.fieldName].filters = filters
                }
            }
        },
        _compute_columns: function (element, events) {
            let key = false
            let domain = []
            if (!_.isEmpty(this.mapping.company_data)) {
                const clinic_model_list = [
                    'dental.appointment',
                    'dermatology.appointment',
                    'practitioner.appointment',
                    'medicine.appointment',
                    'nose_and_ear.appointment',
                    'nutrition.appointment',
                    'obstetrics_and_gynecology.appointment',
                    'ophthalmology.appointment',
                    'orthopedic.appointment',
                    'pediatric.appointment',
                    'physiotherapy.appointment',
                    'radiology.appointment',
                    'urology.appointment',
                ]
                key = clinic_model_list.find(model => this.modelName.includes(model))
                if (!!key) {
                    key = key.replace('.appointment', '');
                    const room_ids = this.mapping.company_data[`${key}_room_ids`]
                    if (!_.isEmpty(room_ids))
                        domain = [['id', 'in', room_ids]]
                }
            }
            if (this.fieldColumn) {
                var self = this;
                var columField = this.fields[this.fieldColumn];
                if (columField) {
                    return this._rpc({
                        model: columField.relation,
                        method: 'search_read',
                        fields: ['name'],
                        domain: domain,
                    })
                        .then(function (records) {
                            if (records.length) {
                                records = _.each(records, function (r) {
                                    return r.title = r.name;
                                });
                                self.data.resources = records;
                            } else {
                                self.data.resources = [{
                                    id: false,
                                    title: 'Unknown'
                                }];
                            }
                        });
                }
            } else {
                return Promise.resolve();
            }
        },
        _recordToCalendarEvent: function (evt) {
            var result = this._super.apply(this, arguments);
            if (this.fieldColumn) {
                var value = evt[this.fieldColumn];
                result.resourceId = _.isArray(value) ? value[0] : value;
            }
            return result;
        },
        _getFullCalendarOptions: function () {
            var result = this._super.apply(this, arguments);
            if (this.fieldColumn) {
                result.resources = [];
            }
            return result;
        },
        calendarEventToRecord: function (event) {
            var result = this._super.apply(this, arguments);
            if (event.resourceId) {
                result[this.fieldColumn] = event.resourceId;
            }
            return result;
        },
    });
});
