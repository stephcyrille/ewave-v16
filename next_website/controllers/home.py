# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.portal.controllers.web import Home
from odoo.http import request


class CustomWebHomepage(Home):
    @http.route(auth='public')
    def index(self, **kw):
        super(CustomWebHomepage, self).index()

        campaign_products = request.env["product.product"].sudo().search([('in_campaign', '=', True)])
        print("\n\n\n")
        print(f"The size is {len(campaign_products)}")
        print("\n\n")

        values = ''

        # Check if we have a querystring first in the URL for avoiding crashing of the app
        if kw:
            if kw['state']:
                if kw['state'] == 'xgt':
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
            "form_alert": values,
            'products': campaign_products
        }
        return request.render('next_website.home', context)
