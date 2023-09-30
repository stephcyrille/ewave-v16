from datetime import timedelta
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NextewaveLeadCrmPurchase(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    vendor_order_count = fields.Integer(string="Number of Quotations", default=0)
    vendor_id = fields.Many2one('res.partner', string='Vendor', change_default=True, tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 help="You can find a vendor by its Name, TIN, Email or Internal Reference.")

    def action_goto_purchase_order_form(self):
        for rec in self:
            # if not rec.vendor_id:
            #     raise ValidationError("Vendor is missing: You must add a vendor for processing")
            # else:
            action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
            action['context'] = {
                'search_default_draft': 1,
                # 'search_default_partner_id': rec.vendor_id.id,
                # 'default_partner_id': rec.vendor_id.id,
                'default_partner_ref': rec.name,
                'default_opportunity_id': rec.id,
                'crm_products': [{'id': x.product_id.id, 'name': x.product_id.name, 'uom': x.product_id.uom_id.id, 'qty': x.product_qty, 'price': x.price_unit} for x in rec.crm_product_ids]
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
        if len(purchase_order) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchase_order.id
        return action

    def _prepare_opportunity_quotation_context(self):
        """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """
        self.ensure_one()
        quotation_context = {
            'default_opportunity_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': [(6, 0, self.tag_ids.ids)],
            'crm_products': [
                {'id': x.product_id.id, 'name': x.product_id.name, 'qty': x.product_qty, 'price': x.price_unit} for x in self.crm_product_ids]
        }
        if self.team_id:
            quotation_context['default_team_id'] = self.team_id.id
        if self.user_id:
            quotation_context['default_user_id'] = self.user_id.id
        return quotation_context
