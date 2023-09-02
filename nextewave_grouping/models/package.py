# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .libs import generate_ean


class NextewaveGroupingPackageLine(models.Model):
    _name = 'nextewave.grouping.package.line'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'NEXTeWave grouping Package line model'

    product_id = fields.Many2one('product.product', string='Product', required=False,
                                 tracking=True, domain="[('detailed_type', '=', 'product')]")
    description = fields.Text('Description')
    product_qty = fields.Float('Quantity', required=True, tracking=True)
    price_unit = fields.Float('Price', compute='_compute_unit_price')
    total_price = fields.Float('Total price', readonly=True, tracking=True,
                               compute='_compute_total_price')
    weight = fields.Float("Weight (in Kg)", compute='_compute_weight', tracking=True)
    capacity = fields.Float("Capacity (in m3)", tracking=True, compute='_compute_volume')
    grouping_package_id = fields.Many2one('nextewave.grouping.package', ondelete='cascade', invisible=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_total_price(self):
        """
        Trigger the recompute the total price.
        """
        self.ensure_one()
        if self.price_unit and self.product_qty:
            self.total_price = self.price_unit * self.product_qty
        else:
            self.total_price = 0

    @api.depends('product_id')
    def _compute_unit_price(self):
        """
        Trigger the recompute the unit price.
        """
        self.ensure_one()
        if self.product_id:
            self.price_unit = self.product_id.list_price
        else:
            self.price_unit = 0

    @api.depends('product_id')
    def _compute_weight(self):
        """
        Trigger the recompute the weight.
        """
        self.ensure_one()
        if self.product_id:
            self.weight = self.product_id.weight
        else:
            self.weight = 0

    @api.depends('product_id')
    def _compute_volume(self):
        """
        Trigger the recompute the capicity.
        """
        self.ensure_one()
        if self.product_id:
            self.capacity = self.product_id.volume
        else:
            self.capacity = 0


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
    products_lines_ids = fields.One2many('nextewave.grouping.package.line', 'grouping_package_id',
                                         string='Products', tracking=True, required=True)

    # @api.model
    # def create(self, vals):
    #     res = super(NextewavePackage, self).create(vals)
    #     ean = generate_ean(str(res.id))
    #     res.barcode = ean
    #     res.ref = self.env['ir.sequence'].next_by_code("nextewave.grouping.pack") or 'New'
    #     return res

    # @api.depends('products_lines_ids')
    # def _compute_total_capacity(self):
    #     self.ensure_one()
    #     total_capacity = 0
    #     for line in self.products_lines_ids:
    #         total_capacity += line.capacity or 0.0
    #     self.total_capacity = total_capacity
    #
    # @api.depends('products_lines_ids')
    # def _compute_total_weight(self):
    #     self.ensure_one()
    #     total_weight = 0
    #     for line in self.products_lines_ids:
    #         total_weight += line.weight or 0.0
    #     self.total_weight = total_weight

