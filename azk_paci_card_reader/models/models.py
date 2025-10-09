# -*- coding: utf-8 -*-

from odoo import models, fields, api

PACI_CARD_FIELDS = [('arabic_name_1', 'Arabic Name 1'),
                ('arabic_name_2', 'Arabic Name 2'),
                ('arabic_name_3', 'Arabic Name 3'),
                ('arabic_name_4', 'Arabic Name 4'),
                ('arabic_name_full', 'Arabic Name Full'),
                ('english_name_1', 'English Name 1'),
                ('english_name_2', 'English Name 2'),
                ('english_name_3', 'English Name 3'),
                ('english_name_4', 'English Name 4'),
                ('english_name_full', 'English Name Full'),
                ('sex_arabic', 'Sex Arabic'),
                ('sex_english', 'Sex English'),
                ('nationality_arabic', 'Nationality Arabic'),
                ('nationality_english', 'Nationality English'),
                ('civil_id', 'Civil ID'),
                ('birthdate', 'Birthdate'),
                ('card_issue_date', 'Card Issue Date'),
                ('card_expiry_date', 'Card Expiry Date'),
                ('document_number', 'Document Number'),
                ('card_serial_number', 'Card Serial Number'),
                ('moi_reference', 'MOI Reference'),
                ('district', 'District'),
                ('block_number', 'Block Number'),
                ('street_name', 'Street Name'),
                ('building_plot_number', 'Building Plot Number'),
                ('unit_type', 'Unit Type'),
                ('unit_number', 'Unit Number'),
                ('floor_number', 'Floor Number'),
                ('blood_type', 'Blood Type'),
                ('guardian_civil_id', 'Guardian Civil ID'),
                ('telephone_1', 'Telephone 1'),
                ('telephone_2', 'Telephone 2'),
                ('e_mail_address', 'E Mail Address'),
                ('passport', 'Passport'),
                ('additional_f_1', 'Additional F1'),
                ('additional_f_2', 'Additional F2'),
                ('title', 'Title'),
                ('address_unique_key', 'Address Unique Key'),
                ('application_version', 'Application Version'),
                ('MOI_Reference_Indic', 'MOI Reference Indic')]

class PACICardReader(models.Model):
    _name = 'paci.card.reader'
    _description = 'PACI Card Reader'

    url = fields.Char(required=True, default="http://127.0.0.1")
    port = fields.Char(required=True, default=8060)
    name = fields.Char(required=True)
    is_default = fields.Boolean(required=True)
    
class PACIModel(models.Model):
    _name = 'paci.model'
    _description = 'PACI Model'
    _rec_name = 'model_id'
    
    model_id = fields.Many2one('ir.model', ondelete='cascade', required=True, help="Model to be mapped")
    model_name = fields.Char(compute='_compute_model_name', store=True)
    kanban_search_field = fields.Many2one('ir.model.fields', ondelete='cascade', help='Paci Field which will used to search upon in kanban.')
    list_search_field = fields.Many2one('ir.model.fields', ondelete='cascade', help='Paci Field which will be used to search upon in list.')
    form_search_paci = fields.Selection(selection=PACI_CARD_FIELDS, help='Paci field to read and fill in the form to search for it')
    form_search_field = fields.Many2one('ir.model.fields', ondelete='cascade')
    paci_model_mapping = fields.One2many('paci.model.mapping', 'paci_model')
    
    _sql_constraints = [('unique_model_id', 'unique(model_id)', 'You already mapped this model, if you want to change it make sure to change the already existing record.')]
    
    @api.depends('model_id')
    def _compute_model_name(self):
        for record in self:
            record.model_name = record.model_id.model
    
class PACIModelMapping(models.Model):
    _name = 'paci.model.mapping'
    _description = 'PACI Model Mapping'
    _rec_name = 'paci_field'
    
    paci_field = fields.Selection(selection=PACI_CARD_FIELDS, required=True, help='PACI card field to be mapped')
    paci_model = fields.Many2one('paci.model', required=True, help='Odoo model to be mapped to a paci field')
    model_field = fields.Many2one('ir.model.fields', ondelete='cascade', required=True, help='Odoo Field which will be mapped.')
    model_id = fields.Many2one('ir.model', related='paci_model.model_id')
        
    @api.model
    def get_fields_mapping(self, model_name):
        """
        To be called from the JS, given a parameter the model name and returns the mapping of the fields
        @param model_name: name of the model to get its fields mapping with paci fields
        @return: dictionary where the key is the paci field and the value is the Odoo field for the input model
        """
        model_mappings = self.env['paci.model'].search([('model_name', '=', model_name)])
        
        rt_val = {'url': 'http://localhost:8010', 'mapping': {}, 'kanban_search_field': '', 'list_search_field': '', 
                  'form_search_paci': '', 'form_search_field': '', 'is_mapped': False}
        
        rt_val['mapping'] = dict(map(lambda d: (d.paci_field, d.model_field.name), model_mappings.paci_model_mapping))
        rt_val['kanban_search_field'] = model_mappings.kanban_search_field.name
        rt_val['list_search_field'] = model_mappings.list_search_field.name
        rt_val['form_search_paci'] = model_mappings.form_search_paci
        rt_val['form_search_field'] = model_mappings.form_search_field.name
        
        # check if the current model is mapped to something
        if len(rt_val['mapping']) or rt_val['kanban_search_field'] or rt_val['list_search_field'] or rt_val['form_search_paci'] or rt_val['form_search_field']:
            rt_val['is_mapped'] = True
            
        return rt_val