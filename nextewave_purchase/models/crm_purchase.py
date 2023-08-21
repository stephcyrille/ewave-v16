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
    def default_get(self, fields):
        res = super(NextewaveCrmPurchase, self).default_get(fields)
        context = self.env.context
        # print('\n\n\n===============\n')
        # print(self.env.context)
        # print('\n\n\n===============\n\n')
        crm_products = context.get('crm_products', False)
        opportunity_id = context.get('default_opportunity_id', False)
        order_line = []
        if opportunity_id:
            for product in crm_products:
                data = {
                    'name': product['name'],
                    'product_qty': product['qty'],
                    'product_id': product['id'],
                    'price_unit': product['price'],
                    'order_id': self.id,
                    'date_planned': self.date_planned,
                }
                line = (0, 0, data)
                order_line.append(line)
            res.update({
                'order_line': order_line,
            })
        return res

    @api.model
    def create(self, vals):
        res = super(NextewaveCrmPurchase, self).create(vals)
        if res.opportunity_id:
            # Check if we already have a vendor order
            if res.opportunity_id.vendor_order_count == 0:
                crm_stage_obj = self.env['crm.stage']
                stage = crm_stage_obj.sudo().search([('sequence', '=', 4)])
                res.opportunity_id.write({
                    'vendor_order_count': 1,
                    'state': 'quotation_created',
                    'stage_id': stage.id
                })
        return res

