# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class NextEwavePackAndShipForYou(http.Controller):
    @http.route('/pack-and-ship-4-you/submit', type='http', auth='public', website=True, csrf=False, methods=['POST'])
    def post_source_and_buy_for_you(self, **kwargs):
        partner_obj = request.env['res.partner']
        pack_req_obj = request.env['nextewave.grouping.package.request']
        counter = kwargs.get('product_counter')
        if counter is None:
            counter = 1

        try:
            # Check if partner exist
            req_partner = partner_obj.sudo().search([('email', '=', kwargs.get("email"))])

            if req_partner.id:
                # If user exist, make reservation with the user account
                partner = req_partner
            else:
                # Create a new client
                name = kwargs.get("company_name")
                email = kwargs.get("email")
                phone = kwargs.get("phone_number")
                company_type = "company"
                user_val = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "company_type": company_type,
                    "comment": f"Customer name is {kwargs.get('name')}"
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
                        'name': kwargs.get(key_product_name),
                        'material': kwargs.get(key_material),
                        'quantity': int(kwargs.get(key_quantity)),
                        'weight': float(kwargs.get(key_weight)),
                        'capacity': float(kwargs.get(key_capacity)),
                        'price': float(kwargs.get(key_price)),
                    }
                )
                products_line.append(line)

            pack_req_dict = {
                'customer_id': partner.id,
                'origin': kwargs.get("from_place"),
                'destination': kwargs.get("to_place"),
                'departure_date': kwargs.get("start_date"),
                'arrival_date': kwargs.get("end_date"),
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
            return request.render('next.pack_and_ship_for_you', context)


