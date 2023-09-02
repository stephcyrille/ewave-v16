# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class NextewaveInheritedCampaign(models.Model):
    _inherit = 'buying.campaign'
    _description = 'NEXTeWave campaign'

    customer_buying_count = fields.Integer(string="Buying request count", compute='_compute_req_qty')

    def _compute_req_qty(self):
        self.ensure_one()
        """
            Count all buying request for this campaign
        """
        buying_request = self.env['buying.campaign.request'].\
            sudo().search([('campaign_id', '=', self.id)])

        self.customer_buying_count = len(buying_request)

    def action_view_buying_requests(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("nextewave_base.nextewave_campaign_buy_request_action")
        action['context'] = {
            'search_default_campaign_id': self.id,
            'default_campaign_id': self.id
        }

        buying_req = self.env['buying.campaign.request'].\
            sudo().search([('campaign_id', '=', self.id)])
        if len(buying_req) == 1:
            action['views'] = [(self.env.ref('nextewave_base.nextewave_campaign_buying_form_view').id, 'form')]
            action['res_id'] = buying_req.id
        return action


