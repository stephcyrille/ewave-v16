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
    total_price = fields.Float('Total price', required=False, readonly=True, tracking=True)
    buying_campaign = fields.Many2one('buying.campaign', ondelete='cascade', invisible=True)

    @api.onchange('price_unit')
    def _compute_total_price(self):
        """
        Trigger the recompute the total price.
        """
        if self.price_unit and self.product_qty:
            self.total_price = self.price_unit * self.product_qty
        else:
            pass