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
    price_unit = fields.Float('Price', required=False)
    total_price = fields.Float('Total price', readonly=True, tracking=True,
                               compute='_compute_total_price')
    buying_campaign_id = fields.Many2one('buying.campaign', ondelete='cascade', invisible=True)
    buying_request_id = fields.Many2one('buying.campaign.request', ondelete='cascade', invisible=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_total_price(self):
        for product_line in self:
            """
            Trigger the recompute the total price.
            """
            if product_line.price_unit and product_line.product_qty:
                product_line.total_price = product_line.price_unit * product_line.product_qty
            else:
                product_line.total_price = 0
