import datetime
from datetime import timedelta
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class NextewaveCampaignPurchase(models.Model):
    _inherit = 'purchase.order'

    buy_campaign_id = fields.Many2one('buying.campaign', string='Campaign')

    @api.model
    def default_get(self, fields, context=None):
        if context is None:
            context = self.env.context
        res = super(NextewaveCampaignPurchase, self).default_get(fields)
        products_ids = context.get('products_ids', False)
        buy_campaign_id = context.get('default_buy_campaign_id', False)
        order_line = []
        if buy_campaign_id:
            for product in products_ids:
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


class NextewavePurchaseCampaign(models.Model):
    _inherit = 'buying.campaign'
    _description = 'NEXTeWave purchase campaign'

    purchases_count = fields.Integer(string="Purchase count", compute='_compute_purchase_qty')

    def _compute_purchase_qty(self):
        self.ensure_one()
        """
            Count all buying request for this campaign
        """
        purchases = self.env['purchase.order'].\
            sudo().search([('buy_campaign_id', '=', self.id)])

        self.purchases_count = len(purchases)

    def action_create_po(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['context'] = {
            'search_default_draft': 1,
            'default_buy_campaign_id': self.id,
            'default_origin': self.name,
            'default_company_id': self.company_id.id or self.env.company.id,
            'products_ids': [
                {'id': x.product_id.id, 'name': x.product_id.name, 'qty': x.product_qty, 'price': x.price_unit} for x in
                self.products_ids]
        }

        action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
        return action

    def action_view_purchase_order(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['context'] = {
            'default_buy_campaign_id': self.id,
        }

        purchase_order = self.env['purchase.order'].sudo().search([('buy_campaign_id', '=', self.id)])
        if len(purchase_order) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchase_order.id
        return action
