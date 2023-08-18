from datetime import timedelta
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NextewaveLeadCrmPurchase(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    quotation_count = fields.Integer(string="Number of Quotations", default=0)

    def action_goto_purchase_order_form(self):
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_partner_ref': self.name,
            'default_opportunity_id': self.id
        }

        action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
        return action
