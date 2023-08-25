# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _


class CampaignProductLine(models.Model):
    _name = 'campaign.product.line'
    _inherit=['mail.thread']
    _description = 'Nextewave Campaign product'

    product_id = fields.Many2one('product.product', string='Product', required=False, tracking=True)
    description = fields.Text('Description')
    product_qty = fields.Float('Quantity', required=True, tracking=True)
    price_unit = fields.Float('Price', compute='_compute_unit_price')
    total_price = fields.Float('Total price', readonly=True, tracking=True,
                               compute='_compute_total_price')
    buying_campaign_id = fields.Many2one('buying.campaign', ondelete='cascade', invisible=True)
    buying_request_id = fields.Many2one('buying.campaign.request', ondelete='cascade', invisible=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_total_price(self):
        self.ensure_one()
        """
        Trigger the recompute the total price.
        """
        if self.price_unit and self.product_qty:
            self.total_price = self.price_unit * self.product_qty
        else:
            self.total_price = 0

    @api.depends('product_id')
    def _compute_unit_price(self):
        self.ensure_one()
        """
        Trigger the recompute the total price.
        """
        if self.product_id:
            self.price_unit = self.product_id.list_price
        else:
            self.price_unit = 0
