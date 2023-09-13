# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class NextewaveSourcingForYou(http.Controller):
    @http.route('/sourcing-4-you', type='http', auth='public', website=True)
    def sourcing_for_you(self, **kwagrs):
        if kwagrs:
            print("ARGSSSSSSSSSS", kwagrs)
            print('BAAAAAAAAAAAAAAAA=========', kwagrs.get('var'))
        return request.render('nextewave_web_template.source_for_you_form', {})

