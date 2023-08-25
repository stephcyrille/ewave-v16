# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _


class CampaignProductLine(models.Model):
    _name = 'campaign.product.line'
    _inherit=['mail.thread']
    _description = 'Nextewave Campaign product'

    product_id = fields.Many2one('product.product', string='Product', required=False,
                                 tracking=True, domain="[('detailed_type', '=', 'product')]")
    description = fields.Text('Description')
    product_qty = fields.Float('Quantity', required=True, tracking=True)
    price_unit = fields.Float('Price', compute='_compute_unit_price')
    total_price = fields.Float('Total price', readonly=True, tracking=True,
                               compute='_compute_total_price')
    buying_campaign_id = fields.Many2one('buying.campaign', ondelete='cascade', invisible=True)
    buying_request_id = fields.Many2one('buying.campaign.request', ondelete='cascade', invisible=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_total_price(self):
        for rec in self:
            """
            Trigger the recompute the total price.
            """
            if rec.price_unit and rec.product_qty:
                rec.total_price = rec.price_unit * rec.product_qty
            else:
                rec.total_price = 0

    @api.depends('product_id')
    def _compute_unit_price(self):
        for rec in self:
            """
            Trigger the recompute the total price.
            """
            if rec.product_id:
                rec.price_unit = rec.product_id.list_price
            else:
                rec.price_unit = 0
