# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class NextewaveSaleGroupingPackageRequest(models.Model):
    _name = 'nextewave.grouping.package.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave grouping package request'
    _rec_name = 'ref'
    _order = 'ref'

    ref = fields.Char('Request reference', tracking=True, readonly=True, required=False, index=True,
                      copy=False, default="New")
    customer_id = fields.Many2one('res.partner', string='Customer', tracking=True, required=True)
    origin = fields.Char(string='From place', tracking=True, required=True)
    destination = fields.Char(string='Destination', tracking=True, required=True)
    departure_date = fields.Date("Estimated departure", tracking=True, required=True)
    arrival_date = fields.Date("Estimated arrival", tracking=True, required=True)
    source_warehouse_id = fields.Many2one("stock.warehouse", string="Origin WH", tracking=True)
    destination_warehouse_id = fields.Many2one("stock.warehouse", string="Destination WH", tracking=True)
    current_location_id = fields.Many2one("stock.location", string="Location", tracking=True,
                                          help="The item location must be an internal location type")
    material = fields.Selection([
        ('other', 'Other'),
        ('electronic', 'Electronic'),
        ('textile', 'Textile'),
        ('cosmetic', 'Cosmetic'),
        ('mixed', 'Mixed'),
        ('shoes', 'Shoes')], string='Package type',
        copy=False, default='other', index=True, tracking=True)
    total_price = fields.Float('Total price', tracking=True, default=0, readonly=True,
                               compute="_compute_total_price")
    total_weight = fields.Float("Total Weight (in Kg)", default=0, tracking=True, readonly=True,
                                compute="_compute_total_weight")
    total_capacity = fields.Float("Total Capacity (in m3)", default=0, tracking=True, readonly=True,
                                  compute="_compute_total_capacity")
    item_count = fields.Integer(string="Number of items", default=0, readonly=True,
                                compute="_compute_total_items")
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('validated', 'Validated'),
        ('canceled', 'Canceled')], string='Status',
        copy=False, default='new', index=True, readonly=True, tracking=True)
    items_lines_ids = fields.One2many('nextewave.grouping.item', 'grouping_package_request_id',
                                      string='Package items')

    # On save check if the items material are matching with the package request material
    # otherwise, we ask the user to use mixed type instead
    @api.model
    def create(self, vals):
        res = super(NextewaveSaleGroupingPackageRequest, self).create(vals)
        if res.items_lines_ids:
            for line in res.items_lines_ids:
                line.customer_id = res.customer_id
        res["ref"] = self.env["ir.sequence"].next_by_code("grouping.package.request.sequence") or "New"
        return res

    @api.depends('items_lines_ids')
    def _compute_total_items(self):
        for rec in self:
            if rec.items_lines_ids:
                rec.item_count = len(rec.items_lines_ids)
            else:
                rec.item_count = 0

    @api.depends('items_lines_ids')
    def _compute_total_price(self):
        for rec in self:
            if rec.items_lines_ids:
                for line in rec.items_lines_ids:
                    rec.total_price += (line.quantity * line.price)
            else:
                rec.total_price = 0

    @api.depends('items_lines_ids')
    def _compute_total_weight(self):
        for rec in self:
            if rec.items_lines_ids:
                for line in rec.items_lines_ids:
                    rec.total_weight += (line.quantity * line.weight)
            else:
                rec.total_weight = 0

    @api.depends('items_lines_ids')
    def _compute_total_capacity(self):
        for rec in self:
            if rec.items_lines_ids:
                for line in rec.items_lines_ids:
                    rec.total_capacity += (line.quantity * line.capacity)
            else:
                rec.total_capacity = 0

    def action_confirm(self):
        self.ensure_one()
        if not  self.items_lines_ids:
            raise ValidationError("You must add at least 1 item in the request")
        self.write({
            'state': 'confirmed'
        })

    def action_collect_items(self):
        self.ensure_one()
        for line in self.items_lines_ids:
            line.write({
                'status': 'in_stock'
            })
        self.write({
            'state': 'validated'
        })
