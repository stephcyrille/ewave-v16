# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BuyingCampaign(models.Model):
    _name = 'buying.campaign'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave Buying Campaign'
    _rec_name = "ref"

    ref = fields.Char('Reference', tracking=True, readonly=True, index=True,
                      copy=False, default="New")
    name = fields.Char(string="Name", required=True)
    start_date = fields.Date("Start date", tracking=True, required=True)
    end_date = fields.Date("End date", tracking=True, required=True)
    product_count = fields.Integer(string='Number of products', compute='_count_products',
                                   readonly=True)
    expected_revenue = fields.Float("Expected revenue", default=0, tracking=True,
                                    compute='_compute_expected_revenue', readonly=True)
    current_revenue = fields.Float("Current revenue", default=0, tracking=True,
                                   compute='_compute_current_revenue', readonly=True)
    order_id = fields.Many2one('sale.order', string='Sale order', tracking=True)
    products_ids = fields.One2many('campaign.product.line', 'buying_campaign_id', string='Products', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('canceled', 'Canceled')], required=True, default='new', readonly=True, tracking=True)
    user_id = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user,
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)
    company_id = fields.Many2one(
        'res.company', string='Company', index=True,
        compute='_compute_company_id', readonly=False, store=True)
    user_company_ids = fields.Many2many(
        'res.company', compute='_compute_user_company_ids',
        help='UX: Limit to lead company or all if no company')

    @api.model
    def create(self, vals):
        res = super(BuyingCampaign, self).create(vals)
        res["ref"] = self.env["ir.sequence"].next_by_code("buying.campaign.sequence") or "New"
        return res

    def _count_products(self):
        self.product_count = len(self.products_ids)

    @api.depends('products_ids')
    def _compute_expected_revenue(self):
        for rec in self:
            rec.expected_revenue = 0
            if rec.products_ids:
                for product in rec.products_ids:
                    value = (product.price_unit - product.vendor_unit_price) * product.product_qty
                    rec.expected_revenue += value

    @api.depends('products_ids')
    def _compute_current_revenue(self):
        for rec in self:
            rec.current_revenue = 0

    @api.depends('company_id')
    def _compute_user_company_ids(self):
        all_companies = self.env['res.company'].search([])
        for campaign in self:
            if not campaign.company_id:
                campaign.user_company_ids = all_companies
            else:
                campaign.user_company_ids = campaign.company_id

    @api.depends('user_id')
    def _compute_company_id(self):
        """ Compute company_id coherency. """
        for campaign in self:
            campaign.company_id = False

    def action_confirm(self):
        self.ensure_one()
        if self.expected_revenue <= 0:
            raise ValidationError("Expected revenue must be greater than 0")
        if len(self.products_ids) == 0:
            raise ValidationError("You need to add at least on product for the campaign")
        else:
            self.write({
                'state': 'confirmed'
            })

    def action_publish(self):
        self.ensure_one()
        all_campaign = self.env['buying.campaign'].search(['state', '=', 'published'])
        if len(all_campaign) > 0:
            for campaign in all_campaign:
                for product in campaign.products_ids:
                    product.write({
                        'in_campaign': False
                    })
                campaign.write({
                    'state': 'closed'
                })
        for p in self.products_ids:
            p.product_id.write({
                'in_campaign': True
            })
        self.write({
            'state': 'published'
        })

    def action_close_campaign(self):
        self.ensure_one()
        for p in self.products_ids:
            p.product_id.write({
                'in_campaign': False
            })
        self.write({
            'state': 'closed'
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



