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

    'category': 'Website/Theme',
    'version': '16.1.0',

    # any module necessary for this one to work correctly
    'depends': ['website',
                'nextewave_base',
                'nextewave_crm'],

    # always loaded
    'data': [
        'views/snippets/head_meta.xml',
        'views/layout.xml',
        'views/header.xml',
        'views/footer.xml',
        'views/index.xml',
        'views/services.xml',
        'views/sourcing.xml',
        'views/sourcing-for-you.xml',
        'views/pack-and-ship.xml',
        'views/campaign.xml',
        'views/pack-and-ship-for-you.xml',
        'views/success-stories.xml',
        'views/about-us.xml',
        'views/contact-us.xml',
    ],
    'assets': {
         'web.assets_frontend': [
             "https://kit.fontawesome.com/b2b52c5522.js",
             "/next_website/static/src/js/index.js",
             # 'nextewave_web_template/static/src/scss/theme.scss',
             # 'nextewave_web_template/static/src/js/theme.js',
            # 'nextewave_web_template/static/css/global.css',
            # 'nextewave_web_template/static/css/output.css',
            # 'nextewave_web_template/static/css/index.css',

            # 'nextewave_web_template/static/js/jquery-111.js',
            # 'nextewave_web_template/static/js/index.js',
            # 'nextewave_web_template/static/js/carousel.js',
            # 'nextewave_web_template/static/js/timer.js',
            # 'nextewave_web_template/static/js/fontawesome.js'
            # "https://fonts.googleapis.com/css2?family=Karla:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,500&amp;family=Montserrat&amp;display=swap"
         ]
    },
    'installable': True,
    'application': False
}
# -*- coding: utf-8 -*-
