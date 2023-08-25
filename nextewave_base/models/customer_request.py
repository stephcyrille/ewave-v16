# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BuyingRequest(models.Model):
    _name = 'buying.campaign.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave Buying Campaign request'
    _rec_name = 'campaign_id'

    customer_id = fields.Many2one("res.partner", string="Customer", tracking=True, required=True)
    campaign_id = fields.Many2one("buying.campaign", string="Campaign", tracking=True,
                                  required=True, domain="[('state', '=', 'published')]")
    # Compute from the so
    request_date = fields.Date("Request date", tracking=True, default=fields.Date.today(), readonly=True)
    request_amount = fields.Float("Request amount", default=0, tracking=True, readonly=True)
    description = fields.Html('Notes')
    delivery_expected_date = fields.Date("Delivery expected", tracking=True, required=True)
    products_ids = fields.One2many('campaign.product.line', 'buying_request_id', string='Products',
                                   tracking=True)
    # Create a pack when the payment is made
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('order_created', 'Order created'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled')], required=True, default='new', readonly=True, tracking=True)

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

    def action_confirm(self):
        self.ensure_one()
        if len(self.products_ids) == 0:
            raise ValidationError("You need to add at least on product for the campaign")
        else:
            self.write({
                'state': 'confirmed'
            })

    def action_create_so(self):
        self.ensure_one()
        quotation_context = {
            'default_customer_buying_request_id': self.id,
            'default_partner_id': self.customer_id.id,
            'request_products': [
                {'id': x.product_id.id, 'name': x.product_id.name, 'qty': x.product_qty, 'price': x.price_unit} for x in
                self.products_ids]
        }
        if self.team_id:
            quotation_context['default_team_id'] = self.team_id.id
        if self.user_id:
            quotation_context['default_user_id'] = self.user_id.id
        return quotation_context

    def action_make_payment(self):
        self.ensure_one()
        self.write({
            'state': 'paid'
        })

    def action_cancel(self):
        self.ensure_one()
        self.write({
            'state': 'canceled'
        })

    def action_reinitialize(self):
        self.ensure_one()
        self.write({
            'state': 'new'
        })





