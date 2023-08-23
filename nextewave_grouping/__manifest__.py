{
    'name': "Nextewave Grouping Module",

    'summary': """NEXTeWave Grouping: Stock and inventory manager""",

    'description': """
NEXTeWave Stock inventory module
==================================
NEXTeWave module for grouping products and prepare for shipping
    """,
    'author': "Stephane Cyrille Mebenga",
    'website': "https://stephanemebenga.site",

    'category': 'NEXTeWave/Addons',

    # any module necessary for this one to work correctly
    'depends': [
        'stock',
        'account',
        'mail',
        'delivery',
        'product',
        'portal',
        'utm',
        'nextewave_base',
        'nextewave_crm',
        'nextewave_purchase'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ]
}
# -*- coding: utf-8 -*-
