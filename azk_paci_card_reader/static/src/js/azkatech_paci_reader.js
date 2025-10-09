/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { ListController } from "@web/views/list/list_controller";
import { KanbanController } from "@web/views/kanban/kanban_controller";
// import { SearchBar } from "@web/search/search_bar/search_bar";
import { useService } from "@web/core/utils/hooks";
// import { Dialog } from "@web/core/dialog/dialog";
// import { _t } from "@web/core/l10n/translation";

class PaciReader {
    // dictionary where the key is model name, and value is dictionary(1st key is url and value is url of the web server, 2nd key is mapping and value is 
    // dictionary where the key is paci field and value is odoo field
    paciMappingCache = {}; 
    my_rpc = useService("rpc");

    async loadCache(model) {
        let me = this;

        if(model in me.paciMappingCache) {
            console.log(`Model ${model} was already synced and cached.`);
            return;
        }
        
        console.log(`Loading cache for model:${model}`);
        
        await this.my_rpc("/web/dataset/call_kw/azk.card.model.mapping/get_fields_mapping", {
            model: 'paci.model.mapping',
            method: 'get_fields_mapping',
            args: [model],
            kwargs: {}
        }).then(function (modelMapping) {
            console.log(`Retrieved mapped fields for ${model}`)
            console.log(modelMapping); 
            
            //save the mapping locally
            me._saveMapping(model, modelMapping)
        });
		console.log('loadCache end');
    }

    checkReadModel(model, view_type){
        //is_creating = !(typeof state['ref'] === 'number');
        let me = this;
        if(me.paciMappingCache[model] && me.paciMappingCache[model]['is_mapped']) {
            console.log(`Model ${model} is mapped, will create paci buttons...`);
            
            // append the button if the user has a list search field and has mappings
            if(view_type == 'list' && me.paciMappingCache[model]['list_search_field'].length && Object.keys(me.paciMappingCache[model]['mapping']['mapping']).length) {
                return true;
            }
            // append the button if the user has a kanban search field and has mappings
            else if(view_type == 'kanban' && me.paciMappingCache[model]['kanban_search_field'].length && Object.keys(me.paciMappingCache[model]['mapping']['mapping']).length) {
                return true;
            }
            // append the button if the user has mapped fields to the current model
            else if(view_type == 'form') {
                if(Object.keys(me.paciMappingCache[model]['mapping']['mapping']).length) {
                    return true;
                }
            }
        }
        return false;
    }

    checkSearchModel(model){
        if(this.paciMappingCache[model] && this.paciMappingCache[model]['is_mapped'] && this.paciMappingCache[model]['form_search_paci'].length){
            return true;
        }
        return false;
    }

    readPaci(model, view_type){
        /* call the web server to get the fields read from  paci
        * @param paci_reader_url: url to be called to read from  paci
        * @param mapped_paci_to_odoo: dictionary, key --> paci field value --> odoo field
        * */
        let me = this;
        let mapped_paci_to_odoo = me.paciMappingCache[model]['mapping'];
        let paci_url_full_path = `${me.paciMappingCache[model]['url']}/azkatech/paci`;

        $.ajax({
            url: paci_url_full_path,
            type: 'Get',
            dataType: "json",
            crossDomain: true,
            format: "json",
        }).done(function(data) {
            console.log(`Received data from reader on url: ${paci_url_full_path}`)
            console.log(data);
            
            let mapped_paci_values = {};
            // key is Odoo field and value is the value read from paci
            let payload = data['payload']; 
            
            // check if the paci field in the model mapping is found in the fields read from the paci
            // if so, then add to the dictionary: key --> model field value --> paci field value
            $.each(payload, function(paci_field, paci_value) {
                if(paci_field in mapped_paci_to_odoo['mapping']) {
                    mapped_paci_values[mapped_paci_to_odoo['mapping'][paci_field]] = paci_value;
                }
            });
            
            console.log('Mapped from paci to odoo:')
            console.log(mapped_paci_values);
            
            me._fillPaciData(mapped_paci_values, model, view_type);
        }).fail(function(xhr, status, error) {
            console.log(`Could not call the url: ${paci_url_full_path}`);
            console.log(status);
            alert("Could not read PACI card.");
            // Dialog.alert(me, _t("Could not read PACI card."), {});
        });
    }

    searchPaci(model) {
        /* call the web server to get the fields read from  paci
         * @param paci_reader_url: url to be called to read from paci card
         * @param formSearch: dictionary, key --> form_search_field/form_search_paci value --> odoo field
         * */
        let me = this;
        let formSearch = {'form_search_field': me.paciMappingCache[model]['form_search_field'], 'form_search_paci': me.paciMappingCache[model]['form_search_paci'] }
        let paci_url_full_path = `${me.paciMappingCache[model]['url']}/azkatech/paci`;
        
        $.get(paci_url_full_path, {}, function(data) {
            console.log(`Received data from reader on url: ${paci_url_full_path}`);
            console.log(data);
            
            let paciFieldValue = data['payload'][formSearch['form_search_paci']], // get the paci field value
                el = $('[name='+formSearch['form_search_field']+']'); // get the element in the form to fill the above value with
                
            if(el.find('input').length) {
                el = el.find('input');
            }
            
            console.log(`Search on element "${formSearch['form_search_field']}" using the paci field "${formSearch['form_search_paci']}" of value "${paciFieldValue}"`);
            el.val(paciFieldValue).trigger('change').trigger('keydown');
        }).fail(function() {
            console.log(`Could not call the url: ${paci_url_full_path}`);
            
            alert("Could not read PACI card.");
            // Dialog.alert(me, _t("Could not read PACI card."), {});
        });
    }
    
    _saveMapping(model_name, modelMapping) {
        /* save the mapping in the cache
         * @param model_name: model name to be used as key in the cache dictionary
         * @param  modelMapping: dictionary, key --> paci field value --> odoo field
         * */
        let me = this;
        
        me.paciMappingCache[model_name] = {};
        me.paciMappingCache[model_name]['url'] = modelMapping.url;
        me.paciMappingCache[model_name]['mapping'] = modelMapping;
        me.paciMappingCache[model_name]['kanban_search_field'] = modelMapping.kanban_search_field;
        me.paciMappingCache[model_name]['list_search_field'] = modelMapping.list_search_field;
        me.paciMappingCache[model_name]['form_search_field'] = modelMapping.form_search_field;
        me.paciMappingCache[model_name]['form_search_paci'] = modelMapping.form_search_paci;
        me.paciMappingCache[model_name]['is_mapped'] = modelMapping.is_mapped;
        
        console.log(`Saved the mapping of the model: ${model_name} with mapping: `);
        console.log(modelMapping);
    }
    
    _fillPaciData(data, model, view_type) {
        /* after retrieving the data from the web server this method will be called to
         * show the data retrieved in the form or tree
         * @data: dictionary, key --> model_field value --> value read from the paci
         * */
        
        let me = this;
        
        if(view_type == 'form') {
            $.each(data, function(key, val) {
                let el = $('[name='+key+']');
                // check if el is a div, if so then get the input of it
                // this will be in the case we have a selection field, or input inside a div...
                if( el.find('input').length ) {
                    el = el.find('input');
                }
				el.val(val).trigger('change').trigger('keydown'); // make sure to trigger change in order for the values to be picked when saving the form
				// make sure to trigger keydown in order for the values in the selections to be shown
            });
            
        } else if(view_type == 'list' || view_type == 'kanban' || view_type == 'search') { // it is "search" in case of popup
            let modelFieldValue = data[me.paciMappingCache[model][`${view_type}_search_field`]];
            $('[role=searchbox]').val(modelFieldValue);
            
            console.log(`Search in "${view_type}" using the field "${me.paciMappingCache[model][`${view_type}_search_field`]}" of value "${modelFieldValue}"`);
        }
    }
}

patch(FormController.prototype, {

    paciReader : PaciReader,
    setup() {
        super.setup();
		this.initPaci();
    },

	async initPaci(){
		this.paciReader = new PaciReader();
        await this.paciReader.loadCache(this.props.resModel, 'form');
        this.props.ShowReadPaci = this.paciReader.checkReadModel(this.props.resModel, 'form');
        // this.props.ShowSearchPaci = this.paciReader.checkSearchModel(this.props.resModel);
    },

    onClickSyncPaci() {
        this.paciReader.readPaci(this.props.resModel, 'form');
    },

    onClickSearchPaci() {
        this.paciReader.searchPaci(this.props.resModel);
    },
});

patch(ListController.prototype, {

    paciReader : PaciReader,
    setup() {
        super.setup();
		this.initPaci();
    },

	async initPaci(){
		this.paciReader = new PaciReader();
        await this.paciReader.loadCache(this.props.resModel, 'list');
        this.props.ShowReadPaci = this.paciReader.checkReadModel(this.props.resModel, 'list');
	},

    onClickSyncPaci() {
        this.paciReader.readPaci(this.props.resModel, 'list');
    }
});

patch(KanbanController.prototype, {

    paciReader : PaciReader,
    setup() {
        super.setup();
		this.initPaci();
    },

	async initPaci(){
		this.paciReader = new PaciReader();
        await this.paciReader.loadCache(this.props.resModel, 'kanban');
        this.props.ShowReadPaci = this.paciReader.checkReadModel(this.props.resModel, 'kanban');
    },

    onClickSyncPaci() {
        this.paciReader.readPaci(this.props.resModel, 'kanban');
		// this.env.searchModel.search();
    }
});
