# -*- coding: utf-8 -*-
{
    'name': "Smart Card Reader (PACI support)",

    'summary': """
        Read all the information from the Smart card in a single click with ability to search using a specific field. Supports PACI Kuwait""",
        
    'description': """
        Enables reading all information from the Smart card in a single click. It can read into any Odoo model and not limited to the “Contact”. Supports PACI Kuwait.
    """,

    'author': "Azkatech",
    'website': "http://www.azka.tech",

    'assets': {
        'web.assets_backend': [
            'azk_paci_card_reader/static/src/xml/buttons_templates.xml',
            'azk_paci_card_reader/static/src/js/azkatech_paci_reader.js'
        ]
    },

    'category': 'Tool',
    'version': '17.0.0.0',
    
    "license": "AGPL-3",
    "support": "support+apps@azka.tech ",
    
    "price": 59,
    "currency": "USD",

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    
    'application': False, 
    'images': ['static/description/banner.png'],
}
