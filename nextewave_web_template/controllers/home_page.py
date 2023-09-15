# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.portal.controllers.web import Home
from odoo.http import request
import pdb

class CustomWebHomepage(Home):
    @http.route(auth='public')
    def index(self, **kw):
        super(CustomWebHomepage, self).index()
        print("\n\n\n\n===================================================\n\n")
        print(kw)
        # print(request.env['ir.config_parameter'].sudo())
        print("\n\n====================================================\n\n\n\n")

        values = ''
        if kw['state']:
            if kw['state'] == 's4y':
                values = {
                    'color': 'success',
                    'title': 'Success!',
                    'message_header': 'Your application is well submitted, and it is under processing.',
                    'message_body': 'Now we will contact you these next days by phone or email for next step.',
                }
            else:
                values = {
                    'color': 'danger',
                    'title': 'Error!',
                    'message_header': 'An Error occurs when we tried to save your application!',
                    'message_body': 'Please, retry now or contact our support in the contact page.',
                }

        context = {
            "form_alert": values
        }
        return request.render('website.homepage', context)
