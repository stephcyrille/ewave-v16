# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .libs import generate_ean


class NextewaveGroupingPackageLine(models.Model):
    _name = 'nextewave.grouping.package.line'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'NEXTeWave grouping Package line model'

    item_id = fields.Many2one('nextewave.grouping.item', string='Item', required=False, tracking=True)
    product_qty = fields.Float('Quantity', readonly=True, tracking=True, compute='_compute_qty')
    total_price = fields.Float('Total price', readonly=True, tracking=True,
                               compute='_compute_total_price')
    total_weight = fields.Float("Total weight (Kg)", compute='_compute_total_weight', tracking=True,
                                readonly=True)
    total_capacity = fields.Float("Total capacity (m3)", tracking=True, compute='_compute_total_capacity',
                                  readonly=True)
    grouping_package_id = fields.Many2one('nextewave.grouping.package', ondelete='cascade', invisible=True)

    @api.depends('item_id')
    def _compute_qty(self):
        """
        Trigger compute quantity.
        """
        for rec in self:
            if rec.item_id:
                rec.product_qty = rec.item_id.quantity
            else:
                rec.product_qty = 0

    @api.depends('item_id', 'product_qty')
    def _compute_total_price(self):
        """
        Trigger the recompute the total price.
        """
        for rec in self:
            if rec.item_id:
                rec.total_price = rec.item_id.quantity * rec.item_id.price
            else:
                rec.total_price = 0

    @api.depends('item_id', 'product_qty')
    def _compute_total_weight(self):
        """
        Trigger the recompute the weight.
        """
        for rec in self:
            if rec.item_id:
                rec.total_weight = rec.item_id.quantity * rec.item_id.weight
            else:
                rec.total_weight = 0

    @api.depends('item_id', 'product_qty')
    def _compute_total_capacity(self):
        """
        Trigger the recompute the capacity.
        """
        for rec in self:
            if rec.item_id:
                rec.total_capacity = rec.item_id.quantity * rec.item_id.capacity
            else:
                rec.total_capacity = 0


class NextewaveGroupingPackage(models.Model):
    _name = 'nextewave.grouping.package'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'NEXTeWave grouping Package model'
    _rec_name = 'ref'

    ref = fields.Char('Reference', tracking=True, readonly=True, required=True, index=True,
                      copy=False, default="New")
    barcode = fields.Char('Barcode', tracking=True, readonly=True)
    warehouse_id = fields.Many2one("stock.warehouse", string="Origin warehouse", tracking=True,
                                   required=True)
    actual_warehouse_id = fields.Many2one("stock.warehouse", string="Destination warehouse",
                                          tracking=True, required=False)
    location_id = fields.Many2one('stock.location', string='Current location', tracking=True,
                                  required=False)
    total_weight = fields.Float("Total weight", default=0, tracking=True, readonly=True,
                                compute='_compute_total_weight')
    total_capacity = fields.Float("Total volume", default=0, tracking=True, readonly=True,
                                  compute='_compute_total_capacity')
    creation_date = fields.Date("Creation date", tracking=True, default=fields.Date.today(),
                                readonly=True)
    departure_date = fields.Date("Estimated departure", tracking=True)
    # pack_type = fields.Many2one("product.packaging", string="Package type", tracking=True, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked', 'Checked'),
        ('locked', 'Locked'),
        ('canceled', 'Canceled'),
        ('confirmed', 'Confirmed'),
        ('loaded', 'Loaded'),
        ('unloaded', 'Unloaded')], string='Status',
        copy=False, default='draft', index=True, readonly=True, tracking=True)
    now_is_locked = fields.Boolean(readonly=True, default=False, tracking=True)
    items_lines_ids = fields.One2many('nextewave.grouping.package.line', 'grouping_package_id',
                                         string='Package Items', tracking=True, required=True)

    @api.model
    def create(self, vals):
        res = super(NextewaveGroupingPackage, self).create(vals)
        res["ref"] = self.env["ir.sequence"].next_by_code("grouping.package.sequence") or "New"
        return res

    @api.depends('items_lines_ids')
    def _compute_total_capacity(self):
        for rec in self:
            total_capacity = 0
            for line in rec.items_lines_ids:
                total_capacity += line.total_capacity or 0.0
            rec.total_capacity = total_capacity

    @api.depends('items_lines_ids')
    def _compute_total_weight(self):
        for rec in self:
            total_weight = 0
            for line in rec.items_lines_ids:
                total_weight += line.total_weight or 0.0
            rec.total_weight = total_weight

