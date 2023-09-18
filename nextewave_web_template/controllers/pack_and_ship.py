# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class NextewavePackAndShipForYou(http.Controller):
    @http.route('/pack-and-ship-4-you', type='http', auth='public', website=True)
    def sourcing_for_you(self, **kwagrs):
        return request.render('nextewave_web_template.pack_and_ship_for_you_template', {})

    @http.route('/pack-and-ship-4-you/submit', type='http', auth='public', website=True, csrf=False)
    def post_source_and_buy_for_you(self, **kwagrs):
        partner_obj = request.env['res.partner']
        pack_req_obj = request.env['nextewave.grouping.package.request']
        counter = kwagrs.get('product_counter')
        if counter is None:
            counter = 1

        try:
            # Check if partner exist
            req_partner = partner_obj.sudo().search([('email', '=', kwagrs.get("email"))])

            if req_partner.id:
                # If user exist, make reservation with the user account
                partner = req_partner
            else:
                # Create a new client
                name = kwagrs.get("company_name")
                email = kwagrs.get("email")
                phone = kwagrs.get("phone_number")
                company_type = "company"
                user_val = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "company_type": company_type
                }
                partner = partner_obj.sudo().create(user_val)

            products_line = []
            for i in range(1, int(counter) + 1):
                # Compose dict key for list product attributes
                key_product_name = f'product_name_{i}'
                key_material = f'product_material_{i}'
                key_quantity = f'quantity_{i}'
                key_weight = f'product_weight_{i}'
                key_capacity = f'product_capacity_{i}'
                key_price = f'product_price_{i}'
                line = (
                    0, 0, {
                        'origin_document': f'WEB/REQ/CUST/{req_partner.id}',
                        'name': kwagrs.get(key_product_name),
                        'material': kwagrs.get(key_material),
                        'quantity': int(kwagrs.get(key_quantity)),
                        'weight': float(kwagrs.get(key_weight)),
                        'capacity': float(kwagrs.get(key_capacity)),
                        'price': float(kwagrs.get(key_price)),
                    }
                )
                products_line.append(line)

            pack_req_dict = {
                'customer_id': partner.id,
                'origin': kwagrs.get("from_place"),
                'destination': kwagrs.get("to_place"),
                'departure_date': kwagrs.get("start_date"),
                'arrival_date': kwagrs.get("end_date"),
                'items_lines_ids': products_line
            }

            pack_req_obj.sudo().create(pack_req_dict)
            return request.redirect('/?state=xgt')
        except Exception as e:
            values = {
                'color': 'danger',
                'title': 'Error!',
                'message_header': 'An Error occurs when we tried to save your application!',
                'message_body': e.__str__(),
            }
            context = {
                "form_alert": values
            }
            return request.render('nextewave_web_template.pack_and_ship_for_you_template', context)


