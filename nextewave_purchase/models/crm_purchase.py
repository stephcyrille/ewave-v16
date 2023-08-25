import datetime
from datetime import timedelta
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NextewaveCrmPurchase(models.Model):
    _inherit = 'purchase.order'

    opportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', check_company=True,
        domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.model
    def default_get(self, fields, context=None):
        if context is None:
            context = self.env.context
        res = super(NextewaveCrmPurchase, self).default_get(fields)
        print('\n\n\n===============\n')
        print(res)
        print('\n\n\n===============\n\n')
        crm_products = context.get('crm_products', False)
        opportunity_id = context.get('default_opportunity_id', False)
        order_line = []
        if opportunity_id:
            for product in crm_products:
                curr_product = self.env['product.product'].sudo().search([('id', '=', product['id'])])

                line = (
                    0, 0, {
                        'name': curr_product.name,
                        # 'display_type': False,
                        'date_planned': datetime.datetime.now(),
                        'product_id': curr_product.id,
                        'product_qty': product['qty'],
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
        res = super(NextewaveCrmPurchase, self).create(vals)
        if res.opportunity_id:
            crm_stage_obj = self.env['crm.stage']
            stage = crm_stage_obj.sudo().search([('sequence', '=', 5)])
            res.opportunity_id.write({
                'vendor_order_count': res.opportunity_id.vendor_order_count + 1,
                'state': 'po_created',
                'stage_id': stage.id
            })
        return res

