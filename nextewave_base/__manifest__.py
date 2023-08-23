# -*- coding: utf-8 -*-
{
    'name': "NEXTeWave Operational module",

    'summary': 'NEXTeWave main operations - Buying, Logistic & Payment',

    'sequence': 2,

    'description': """
NEXTeWave Operations
====================
NEXTeWave module for managing:
    - Sourcing and Buy for you (Sale aggregation)
    - Sale campaign
    - Logistic Grouping
""",

    'author': "Stephane Cyrille Mebenga",
    'website': "https://stephanemebenga.site",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'NEXTeWave/Operations',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sourcing_for_you.xml',
        'views/crm_product_views.xml',
        'views/campaign_views.xml',
        # 'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}
