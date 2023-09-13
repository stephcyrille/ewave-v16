# -*- coding: utf-8 -*-
{
    'name': "NEXTeWave Website",

    'summary': 'NEXTeWave Website custom module',

    'sequence': 11,

    'description': """
NEXTeWave Website module
====================
NEXTeWave module for the web front office that contain:
    - Landing page
    - Forms pages
    - And others
""",

    'author': "Stephane Cyrille Mebenga",
    'website': "https://stephanemebenga.site",

    'category': 'NEXTeWave/Website',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['website',
                'website_mail',
                'nextewave_base',
                'nextewave_crm',
                'nextewave_grouping'],

    # always loaded
    'data': [
        'views/source_for_you_view.xml'
    ],
}
