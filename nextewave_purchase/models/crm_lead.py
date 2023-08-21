from datetime import timedelta
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NextewaveLeadCrmPurchase(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    vendor_order_count = fields.Integer(string="Number of Quotations", default=0)

    def action_goto_purchase_order_form(self):
        for rec in self:
            if not len(rec.crm_product_ids) > 0:
                raise ValidationError("Products details error: You must first add system product before to continue")
            else:
                action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
                action['context'] = {
                    'search_default_draft': 1,
                    'search_default_partner_id': rec.partner_id.id,
                    'default_partner_id': rec.partner_id.id,
                    'default_partner_ref': rec.name,
                    'default_opportunity_id': rec.id,
                    'crm_products': [{'id': x.product_id.id, 'name': x.product_id.name, 'qty': x.product_qty, 'price': x.price_unit} for x in rec.crm_product_ids]
                }

                action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
                return action

    def action_view_purchase_order(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id,
        }

        purchase_order = self.env['purchase.order'].sudo().search([('opportunity_id', '=', self.id)])
        if purchase_order:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchase_order.id
        return action

