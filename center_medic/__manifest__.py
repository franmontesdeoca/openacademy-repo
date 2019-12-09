# -*- coding: utf-8 -*-
{
    'name': "center_medic",

    'summary': """
        
       Center This module allows ordering of products to be exported and 
        treated by the appropriate personnel.""",

    'description': """
        Long description of module's Medic
    """,

    'author': "Franklin Montesdeoca",
    'website': "http://www.elipsys.ec",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock', 'product', 'report', 'board'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reportes/reports.xml',
        'views/session_board.xml',
    ],
    # only loaded in demonstration mode

}
