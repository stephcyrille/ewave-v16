{
    'name': "Nextewave Grouping Module",

    'summary': """NEXTeWave Grouping: Stock and grouping operation""",

    'description': """
NEXTeWave Grouping module
==================================
NEXTeWave module for grouping products and prepare for shipping
    """,
    'author': "Stephane Cyrille Mebenga",
    'website': "https://stephanemebenga.site",

    'category': 'NEXTeWave/Addons',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'nextewave_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/grouping_pack_req_seq.xml',
        'data/grouping_package_seq.xml',
        'views/grouping_package_views.xml',
        'views/items_views.xml',
        'views/grouping_package_request_views.xml',
        'views/grouping_pack_req_payment.xml',
        'views/grouping_package_line_views.xml',
    ]
}
# -*- coding: utf-8 -*-
