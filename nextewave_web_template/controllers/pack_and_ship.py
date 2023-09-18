# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class NextewavePackAndShipForYou(http.Controller):
    @http.route('/pack-and-ship-4-you', type='http', auth='public', website=True)
    def sourcing_for_you(self, **kwagrs):
        return request.render('nextewave_web_template.pack_and_ship_for_you_template', {})