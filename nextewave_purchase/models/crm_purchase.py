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
        # print('\n\n\n===============\n')
        # print(self.env.context)
        # print('\n\n\n===============\n\n')
        crm_products = context.get('crm_products', False)
        opportunity_id = context.get('default_opportunity_id', False)
        order_line = []
        if opportunity_id:
            for product in crm_products:
                line = (0, 0, {'product_id': product['id'], 'product_qty': product['qty']})
                order_line.append(line)
            res.update({
                'order_line': order_line,
            })
        return res

    @api.model
    def create(self, vals):
        res = super(NextewaveCrmPurchase, self).create(vals)
        if res.opportunity_id:
            print("\n\n\n=++++++BAAAAAAMMMMMMMMMMM+++++\n\n")
        return res