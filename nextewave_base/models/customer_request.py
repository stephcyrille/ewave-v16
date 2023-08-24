# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _


class BuyingRequest(models.Model):
    _name = 'buying.campaign.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave Buying Campaign request'

    customer_id = fields.Many2one("res.partner", string="Customer", tracking=True, required=True)
    campaign_id = fields.Many2one("buying.campaign", string="Campaign", tracking=True, required=True)
    request_date = fields.Date("Request date", tracking=True, default=fields.Date.today(), readonly=True)
    request_amount = fields.Float("Request amount", default=0, tracking=True, readonly=True)
    description = fields.Html('Notes')
    delivery_expected_date = fields.Date("Delivery expected date", tracking=True, required=True)
    products_ids = fields.One2many('campaign.product.line', 'buying_request', string='Products', tracking=True)



    # customer_request_ids = fields.One2many('buying.campaign.request', 'campaign_id', string='Customers requests', tracking=True)
