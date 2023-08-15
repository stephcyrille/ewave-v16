# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmProduct(models.Model):
    _name = 'nextewave.product.line'
    _inherit=['mail.thread']
    _description = 'Nextewave product field'

    product_id = fields.Many2one('product.product', string='Product', required=False, tracking=True)
    picture = fields.Binary(string="Picture", tracking=True)
    product_qty = fields.Float('Quantity', required=True, tracking=True)
    description = fields.Text('Description', required=True)
    vendor = fields.Many2one('res.partner', string='Vendor', required=False, tracking=True)
    price_unit = fields.Float('Price', required=False)
    total_price = fields.Float('Total price', required=False, readonly=True, tracking=True)
    crm_lead = fields.Many2one('crm.lead', ondelete='cascade', invisible=True)

    @api.onchange('price_unit')
    def _compute_total_price(self):
        """
        Trigger the recompute the total price.
        """
        if self.price_unit and self.product_qty:
            self.total_price = self.price_unit * self.product_qty
        else:
            pass