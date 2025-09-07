odoo.define('ksc_dental.DentalView', function (require) {
    "use strict";

    const { useState, useRef, useContext } = owl.hooks;
    const { useListener } = require('web.custom_hooks');

    const Registries = require('ksc_dental.Registries');
    const DentalComponent = require('ksc_dental.DentalComponent');


    // Owl Components
    class DentalView extends DentalComponent {
        static template = 'DentalView';
        constructor() {
            super(...arguments);
            useListener('select-teeth-location', this.selectTeethLocation);
            useListener('select-category', this.selectCategory);
            useListener('select-line', this.selectLine);
            useListener('select-product', this.selectProduct);
            useListener('save', this.save);
            this.saveButton = useRef('save-button');
            this.loadingDiv = useRef('loading-div');

            this.do_action = this.props.webClient.do_action.bind(this.props.webClient),
                this.patient_id = odoo.patient_id
            this.user_id = odoo.user_id


            this.view_id = null


            this.patient = null
            this.user = null

            this.teeths = []
            this.categories = []
            this.products = []
            this.selected_paths = []

            this.man_upper_teeth = []
            this.man_lower_teeth = []
            this.child_upper_teeth = []
            this.child_lower_teeth = []


            this.state = useState({
                uiState: 'LOADING', // 'LOADING' | 'READY' | 'CLOSING'
                selectedTeeth: null,
                selectedLocations: [],
                selectedCategory: null,
                selectedLine: null,
                hideChildTeeth: true,
                lines: [],
                fullMouth: false,
            });

            this.addItem = this.addItem.bind(this);
            this.removeItem = this.removeItem.bind(this);
            this.clearItems = this.clearItems.bind(this);

            this.getFill = this.getFill.bind(this);

            this.removeLine = this.removeLine.bind(this);
        }
        hideChildTeeth() {
            this.state.hideChildTeeth = true
        }
        showChildTeeth() {
            this.state.hideChildTeeth = false
        }
        activeFullMouth() {
            this.state.fullMouth = true
        }
        unactiveFullMouth() {
            this.state.fullMouth = false
        }
        captureDiscountChange(event, line) {
            this.state.lines.find(x => x.id == line.id).discount = event.target.value
        }
        async inProgress() {
            if (!this.state.selectedLine) {
                alert('you most select line!')
                return
            }
            let line = this.state.lines.find(x => x.id == this.state.selectedLine)
            line.state = 'in_progress'
        }
        async completed() {
            if (!this.state.selectedLine) {
                alert('you most select line!')
                return
            }
            let line = this.state.lines.find(x => x.id == this.state.selectedLine)
            line.state = 'completed'
        }
        async deleteLine() {
            if (!this.state.selectedLine) {
                alert('you most select line!')
                return
            }
            let line = this.state.lines.find(x => x.id == this.state.selectedLine)
            this.removeLine(line)
        }
        async discard() {
            const self = this
            await this.rpc({
                route: '/web/action/load',
                params: {
                    action_id: "ksc_dental.action_ksc_dental_consultation"
                },
            }).then(function (action) {
                if (action.res_model === 'res.partner') {
                    window.location = `/web#id=${self.view_id.id}&action=${action.id}&model=${action.res_model}&view_type=form`;
                }
                else {
                    window.location = `/web#id=${self.view_id.id}&action=${action.id}&model=${action.res_model}&view_type=form`;
                }

                // window.location = `/web#id=${self.patient_id}&action=602&model=${action.res_model}&view_type=form`;
            });
        }
        loading() {
            this.loadingDiv.el.style.display = 'flex'
        }
        loaded() {
            this.loadingDiv.el.style.display = 'none'
        }
        async save() {
            let lines = this.state.lines
            lines.map(rec => {
                delete rec.name
                delete rec.date
                delete rec.dentist_name
                delete rec.teeth_name
            })
            await this.rpc({
                model: 'res.partner',
                method: 'new_create_lines',
                args: [this.patient_id, lines, this.state.hideChildTeeth]
            }).then(function (result) {
                console.log("save result: ", result)
            });

            await this.loadPatientMedicalHistory()
            setTimeout(() => this.loaded(), 500);
            await this.discard()
        }
        selectProduct(event) {
            const { product } = event.detail;
            if (!this.state.selectedTeeth && !this.state.selectedLocations.length && !this.state.fullMouth) {
                alert('you most select teeth and surface!')
                return
            }

            // if (!this.user.physician_id) {
            //     alert('you are not a physician!')
            //     return
            // }

            let selectedTeeth = this.teeths.find(x => x.id == this.state.selectedTeeth)

            let id = `DentalNewID_${(Math.random()).toString(36)}`;
            while (!!this.state.lines.find(rec => rec.id == id)) {
                id = `DentalNewID_${(Math.random()).toString(36)}`;
            }
            let line = {
                'create_date': new Date(),
                'date': new Date().toLocaleString(),
                'name': product.name,
                'description': product.id,
                'teeth_id': !this.state.fullMouth ? selectedTeeth.id : null,
                'teeth_name': this.state.fullMouth ? 'Full Mouth' : selectedTeeth.name,
                'state': 'planned',
                'detail_description': this.state.fullMouth ? 'Full Mouth' : this.state.selectedLocations.join(', '),
                'dentist': this.user.physician_id && this.user.physician_id[0],
                'dentist_name': this.user.name,
                'amount': product.lst_price,
                'discount': 0,
                'patient_id': this.patient_id,
                'id': id,
            }
            this.addLine(line)
            this.unactiveFullMouth()
        }
        selectCategory(event) {
            const { id } = event.detail;
            if (this.state.selectedCategory != id)
                this.state.selectedCategory = id
            else
                this.state.selectedCategory = null
        }
        selectLine(event) {
            const { id } = event.detail;
            if (this.state.selectedLine != id)
                this.state.selectedLine = id
            else
                this.state.selectedLine = null
        }
        selectTeethLocation(event) {
            const { teeth_code, location } = event.detail;
            if (this.state.selectedTeeth != teeth_code) {
                this.clearItems()
                this.addItem(location)
            } else if (this.getItemCheckedStatus(location)) {
                this.removeItem(location)
            } else {
                this.addItem(location)
            }
            this.state.selectedTeeth = teeth_code
        }
        addLine(line) {
            this.state.lines.unshift(line)
        }
        clearLines() {
            this.state.lines = []
        }
        removeLine(line) {
            this.state.lines.splice(this.state.lines.indexOf(line), 1);
        }
        addItem(item) {
            this.state.selectedLocations.push(item)
        }
        removeItem(item) {
            this.state.selectedLocations.splice(this.state.selectedLocations.indexOf(item), 1);
        }
        clearItems() {
            this.state.selectedLocations = []
        }
        getItemCheckedStatus(item) {
            return this.state.selectedLocations.indexOf(item) != -1;
        }
        getFill(teeth_code, location) {
            let fill = 'white'
            if (this.state.selectedTeeth == teeth_code) {
                fill = this.getItemCheckedStatus(location) ? 'orange' : fill
            }
            let oldLine = this.state.lines.find(rec => rec.teeth_id == teeth_code && rec.state != 'planned' && rec.detail_description.includes(location))
            if (!!oldLine)
                fill = 'teal'
            let plannedLine = this.state.lines.find(rec => rec.teeth_id == teeth_code && rec.state == 'planned' && rec.detail_description.includes(location))
            if (!!plannedLine)
                fill = 'orange'
            if (this.state.fullMouth)
                fill = 'darkseagreen'
            return fill
        }
        async willUnmount() {
            this.loading()
            await this.loadTeeths()
            await this.loadCategories()
            await this.loadProducts()
            await this.loadUser()
            await this.loadPatient()
            await this.loadAppointment()
            await this.loadPatientMedicalHistory()
            this.loaded()
            this.state.uiState = "LOADED"
        }
        async loadTeeths() {
            const self = this
            await this.rpc({
                model: 'teeth.code',
                method: 'search_read',
                kwargs: {
                    fields: ['id', 'name', 'upper', 'lower', 'child', 'man'],
                },
            }).then(function (result) {
                self.teeths = result;
                self.man_upper_teeth = result.filter(rec => rec.upper && rec.man).sort((a, b) => a.id - b.id);
                self.man_lower_teeth = result.filter(rec => rec.lower && rec.man).sort((a, b) => b.id - a.id);
                self.child_upper_teeth = result.filter(rec => rec.upper && rec.child).sort((a, b) => a.id - b.id);
                self.child_lower_teeth = result.filter(rec => rec.lower && rec.child).sort((a, b) => b.id - a.id);
            });
        }
        async loadCategories() {
            const self = this
            await this.rpc({
                model: 'product.category',
                method: 'search_read',
                kwargs: {
                    domain: [['treatment', '=', true]],
                    fields: ['id', 'name'],
                },
            }).then(function (result) {
                self.categories = result;
            });
        }
        async loadProducts() {
            const self = this
            await this.rpc({
                model: 'product.product',
                method: 'search_read',
                kwargs: {
                    domain: [['is_treatment', '=', true]],
                    fields: ['id', 'name', 'action_perform', 'categ_id', 'lst_price'],
                },
            }).then(function (result) {
                self.products = result;
            });
        }
        async loadUser() {
            const self = this
            await this.rpc({
                model: 'res.users',
                method: 'search_read',
                kwargs: {
                    domain: [['id', '=', this.user_id]],
                    fields: ['id', 'name', 'lang', 'company_id', 'partner_id'],
                },
            }).then(function (result) {
                self.user = result[0];
            });
        }
        async loadPatient() {
            const self = this
            await this.rpc({
                model: 'res.partner',
                method: 'search_read',
                kwargs: {
                    domain: [['id', '=', this.patient_id]],
                    fields: ['id', 'name', 'hide_child_teeth'],
                },
            }).then(function (result) {
                self.patient = result[0];
                self.state.hideChildTeeth = self.patient.hide_child_teeth
            });
        }
        async loadAppointment() {
            const self = this
            await this.rpc({
                model: 'ksc.dental.appointment',
                method: 'search_read',
                kwargs: {
                    domain: [['patient_id.id', '=', this.patient_id]],
                    fields: ['patient_id', 'start_date'],
                },
            }).then(function (result) {
                for (let index = 0; index < result.length; index++) {
                    const start_date = new Date(result[index].start_date);
                    const startDateDate = new Date(start_date.getFullYear(), start_date.getMonth(), start_date.getDate());
                    const today = new Date();
                    const todayDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
                    if (startDateDate.getTime() === todayDate.getTime()) {
                        self.view_id = result[index];
                        break;
                    } else {
                        self.view_id = result[0];
                    }
                }
            });
        }

        async loadPatientMedicalHistory() {
            const self = this
            await this.rpc({
                model: 'medical.teeth.treatment',
                method: 'search_read',
                kwargs: {
                    domain: [['patient_id', '=', this.patient_id]],
                    fields: ['id', 'patient_id', 'teeth_id', 'description', 'detail_description', 'state', 'total', 'dentist', 'amount', 'discount', 'compute_date_create'],
                },
            }).then(function (result) {
                self.clearLines()
                result.map(rec => {
                    let line = {
                        'id': rec.id,
                        'date': rec.compute_date_create,
                        'name': rec.description[1],
                        'description': rec.description[0],
                        'teeth_id': rec.teeth_id[0],
                        'teeth_name': rec.teeth_id[1],
                        'state': rec.state,
                        'detail_description': rec.detail_description,
                        'dentist': rec.dentist[0],
                        'dentist_name': rec.dentist[1],
                        'amount': rec.amount,
                        'discount': rec.discount,
                    }
                    self.addLine(line)
                })
            });
        }

    }

    Registries.Component.add(DentalView);

    return DentalView;

});

