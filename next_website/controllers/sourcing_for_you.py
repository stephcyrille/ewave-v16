# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class NextewaveSourcingForYou(http.Controller):

    @http.route('/sourcing-4-you/submit', type='http', auth='public', website=True, csrf=False, methods=['POST'])
    def post_source_and_buy_for_you(self, **kwagrs):
        partner_obj = request.env['res.partner']
        crm_lead_obj = request.env['crm.lead']
        crm_product_pic_obj = request.env['nextewave.product.picture']

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
            email = kwagrs.get("email")
            phone = kwagrs.get("phone_number")
            company_type = 'company' if kwagrs.get("company_name") != '' else 'person'
            user_val = {
                "name": kwagrs.get("company_name") if company_type == 'company' else  kwagrs.get("name"),
                "email": email,
                "phone": phone,
                "company_type": company_type
            }
            partner = partner_obj.sudo().create(user_val)

        usages = ''
        if kwagrs.get("personal_use") is not None:
            usages += kwagrs.get("personal_use")
        if kwagrs.get("commercial_use") is not None:
            usages += ', '
            usages += kwagrs.get("commercial_use")
        if kwagrs.get("buy_and_sell") is not None:
            usages += ', '
            usages += kwagrs.get("buy_and_sell")

        try:
            products_more_info = ''
            products_line = []

            print("\n\n\n\n")
            print(kwagrs)
            print("\n\n")

            for i in range(1, int(counter) + 1):
                # Compose dict key for list product attributes
                key_product_name = f'product_name_{i}'
                key_quantity = f'quantity_{i}'
                key_description = f'product_description_{i}'

                key_picture_1 = f'product_picture_{i}_1'
                key_picture_2 = f'product_picture_{i}_2'
                key_picture_3 = f'product_picture_{i}_3'
                key_picture_4 = f'product_picture_{i}_4'

                print("\n\n\n\n")
                print(kwagrs.get(key_picture_1))
                print(kwagrs.get(key_picture_2))
                print(kwagrs.get(key_picture_3))
                print(kwagrs.get(key_picture_4))
                print("\n")
                print(i)
                print("\n\n")

                val = {
                    "product_pic1": base64.encodebytes(kwagrs.get(key_picture_1).read()) if kwagrs.get(key_picture_1) else None,
                    "product_pic2": base64.encodebytes(kwagrs.get(key_picture_2).read()) if kwagrs.get(key_picture_2) else None,
                    "product_pic3": base64.encodebytes(kwagrs.get(key_picture_3).read()) if kwagrs.get(key_picture_3) else None,
                    "product_pic4": base64.encodebytes(kwagrs.get(key_picture_4).read()) if kwagrs.get(key_picture_4) else None
                }

                product_pic = crm_product_pic_obj.sudo().create(val)

                line = (
                    0, 0, {
                        'product_qty': int(kwagrs.get(key_quantity)),
                        'description': kwagrs.get(key_product_name),
                        "product_picture_id": product_pic.id
                    }
                )
                products_line.append(line)

                products_more_info += f'\n--------- Product {i} ---------\n'
                products_more_info += f'Name: {kwagrs.get(key_product_name)}\n'
                products_more_info += f'Quantity: {kwagrs.get(key_quantity)}\n'
                products_more_info += f'Description: {kwagrs.get(key_description)}\n\n'

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
                "description": lead_description,

                "partner_id": partner.id,
                'crm_product_ids': products_line
            }
            crm_lead_obj.sudo().create(post_crm_val)
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
            return request.render('next.sourcing_for_you_page', context)


