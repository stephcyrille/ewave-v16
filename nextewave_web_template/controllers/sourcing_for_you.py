# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class NextewaveSourcingForYou(http.Controller):
    @http.route('/sourcing-4-you', type='http', auth='public', website=True)
    def sourcing_for_you(self, **kwagrs):
        if kwagrs:
            print("ARGSSSSSSSSSS", kwagrs)
            print('BAAAAAAAAAAAAAAAA=========', kwagrs.get('var'))
        return request.render('nextewave_web_template.source_for_you_form', {})

    @http.route('/sourcing-4-you/submit', type='http', auth='public', website=True, csrf=False)
    def post_source_and_buy_for_you(self, **kwagrs):
        partner_obj = request.env['res.partner']
        crm_lead_obj = request.env['crm.lead']
        crm_product_line = request.env['nextewave.product.line']
        counter = kwagrs.get('product_counter')
        if counter is None:
            counter = 1

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
            # partner = partner_obj.sudo().create(user_val)

        usages = ''
        if kwagrs.get("personal_use") is not None:
            usages += kwagrs.get("personal_use")
        if kwagrs.get("commercial_use") is not None:
            usages += ', '
            usages += kwagrs.get("commercial_use")
        if kwagrs.get("buy_and_sell") is not None:
            usages += ', '
            usages += kwagrs.get("buy_and_sell")

        # TODO We need first to create a product dict list
        products_more_info = ''
        products_line = []
        all_pictures = []

        counter = 2
        for i in range(1, int(counter)):

            # Compose dict key for list product attributes
            key_picture = 'product_picture_' + str(i)
            key_product_name = 'product_name_' + str(i)
            key_quantity = 'quantity_' + str(i)
            key_description = 'product_description_' + str(i)

            print('\n\n\n\n')
            print(f"Datat {key_picture}, {key_product_name}, {key_quantity}, {key_description}")
            print('\n')
            print(kwagrs)
            print('\n\n\n\n')

            line = (
                0, 0, {
                    'product_qty': int(kwagrs.get(key_quantity)),
                    'description': kwagrs.get(key_description),
                }
            )

            products_line.append(line)
            all_pictures.append(kwagrs.get(key_picture))

            products_more_info += f'\n--------- Product {i} ---------\n'
            products_more_info += f'Name: {kwagrs.get(key_product_name)}\n'
            products_more_info += f'Quantity: {kwagrs.get(key_quantity)}\n'
            products_more_info += f'Description: {kwagrs.get(key_description)}\n\n'

            # product_widget = {
            #     "product_qty": kwagrs.get(q),  # TODO Make and integrity test of this data
            #     "picture": base64.encodebytes(p_file.read()) if p_file else False,
            #     "description": p_name_concat,
            # }
            i += 1

        lead_description = f"{kwagrs.get('company_name')}'s opportunity\n----------------------\n\n"
        lead_description += f"Number of items : {counter}\n"
        lead_description += f"Usage(s) : {usages}\n"
        lead_description += f"Additional information :{kwagrs.get('more_information')}\n\n"
        lead_description += products_more_info

        post_crm_val = {
            "state": "new",
            "name": "Opportunity for %s" % (kwagrs.get("company_name")),
            "phone": kwagrs.get("phone_number"),
            "email_from": kwagrs.get("email"),
            "contact_name": kwagrs.get("name"),
            "mobile": kwagrs.get("phone_number"),
            "partner_name": kwagrs.get("company_name"),
            "user_id": None,
            "team_id": None,
            "description": lead_description,

            # "partner_id": partner.id,
            "partner_id": False,
            'crm_product_ids': products_line,
            # "picture": base64.encodebytes(p_file.read()) if p_file else False,
        }

        print("\n\n\n\n===================================================\n\n")
        print(post_crm_val)
        print("\n\n\n\n")


