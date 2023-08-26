from datetime import timedelta
import logging
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class BuyingRequestSaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_buying_request_id = fields.Many2one('buying.campaign.request',
                                                 string='Customer buying request', )

    @api.model
    def default_get(self, fields, context=None):
        if context is None:
            context = self.env.context
        res = super(BuyingRequestSaleOrder, self).default_get(fields)
        # print('\n\n\n===============\n')
        # print(res)
        # print('\n\n\n===============\n\n')
        buying_products = context.get('request_products', False)
        buying_req_id = context.get('default_customer_buying_request_id', False)
        order_line = []
        if buying_req_id:
            for product in buying_products:
                curr_product = self.env['product.product'].sudo().search([('id', '=', product['id'])])

                line = (
                    0, 0, {
                        'name': curr_product.name,
                        'product_id': curr_product.id,
                        'product_uom_qty': product['qty'],
                        'product_uom': curr_product.uom_id.id,
                        'price_unit': product['price']
                    }
                )
                order_line.append(line)
            res.update({
                'order_line': order_line,
            })
        return res

    @api.model
    def create(self, vals):
        res = super(BuyingRequestSaleOrder, self).create(vals)
        if res.customer_buying_request_id:
            res.customer_buying_request_id.write({
                'sale_order_count': res.customer_buying_request_id.sale_order_count + 1,
                'state': 'order_created'
            })
        return res
