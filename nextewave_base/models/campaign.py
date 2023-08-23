# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _


class BuyingRequest(models.Model):
    _name = 'buying.campaign'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave Buying Campaign'

    name = fields.Char(string="Name", required=True)
    start_date = fields.Date("Start date", tracking=True, required=True)
    end_date = fields.Date("End date", tracking=True, required=True)
    product_count = fields.Integer(string='Number of products', compute='_count_products',
                                   readonly=True)
    expected_revenue = fields.Float("Expected revenue", default=0, tracking=True, required=True)
    order_id = fields.Many2one('sale.order', string='Sale order', tracking=True)
    products_ids = fields.One2many('campaign.product.line', 'buying_campaign', string='Products', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('canceled', 'Canceled')], required=True, default='new', readonly=True, tracking=True)

    def _count_products(self):
        self.product_count = len(self.products_ids)

