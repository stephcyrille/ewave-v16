# -*- coding: utf-8 -*-
{
    'name': "NEXTeWave Purchase CRM Addons",

    'summary': """NEXTeWave Purchase CRM Lead Addon module""",

    'description': """
NEXTeWave Purchase CRM Addons
====================
NEXTeWave purchase module for enhance CRM operations
    """,
    'author': "Stephane Cyrille Mebenga",
    'website': "https://stephanemebenga.site",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'NEXTeWave/Addons',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['crm', 'nextewave_crm', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        # 'data/crm_seller_template.xml',
        # 'data/crm_stage_data.xml',

        'views/crm_purchase.xml',
    ],
}
