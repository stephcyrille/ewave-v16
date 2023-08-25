# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _


class BuyingRequest(models.Model):
    _name = 'buying.campaign.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave Buying Campaign request'

    customer_id = fields.Many2one("res.partner", string="Customer", tracking=True, required=True)
    campaign_id = fields.Many2one("buying.campaign", string="Campaign", tracking=True,
                                  required=True, domain="[('state', '=', 'published')]")
    request_date = fields.Date("Request date", tracking=True, default=fields.Date.today(), readonly=True)
    request_amount = fields.Float("Request amount", default=0, tracking=True, readonly=True)
    description = fields.Html('Notes')
    delivery_expected_date = fields.Date("Delivery expected", tracking=True, required=True)
    products_ids = fields.One2many('campaign.product.line', 'buying_request_id', string='Products',
                                   tracking=True)

    @api.onchange('campaign_id')
    def _compute_products(self):
        for rec in self:
            if rec.campaign_id:
                rec.products_ids = rec.campaign_id.products_ids

                # Put the qty at o of each product
                for p in rec.products_ids:
                    p.product_qty = 1
            else:
                rec.products_ids = False
