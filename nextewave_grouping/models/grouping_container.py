# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from .libs import generate_ean


class NextewaveGroupingContainerLine(models.Model):
    _name = 'nextewave.grouping.container.line'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'NEXTeWave grouping container line model'
    _rec_name = 'package_id'

    package_id = fields.Many2one("nextewave.grouping.package", string="Package", required=True,
                                 help="The package current warehouse must be the same as the container "
                                      "warehouse")
    weight = fields.Float("Weight", default=0, tracking=True, readonly=True,
                          compute='_compute_total_weight')
    capacity = fields.Float("Volume", default=0, tracking=True, readonly=True,
                            compute='_compute_total_capacity')
    grouping_package_container_id = fields.Many2one('nextewave.grouping.container', ondelete='cascade',
                                                    invisible=True)

    @api.depends('package_id')
    def _compute_total_weight(self):
        for rec in self:
            if rec.package_id:
                rec.weight = rec.package_id.total_weight
            else:
                rec.weight = 0

    @api.depends('package_id')
    def _compute_total_capacity(self):
        for rec in self:
            if rec.package_id:
                rec.capacity = rec.package_id.total_capacity
            else:
                rec.capacity = 0


class NextewaveGroupingContainer(models.Model):
    _name = 'nextewave.grouping.container'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'NEXTeWave grouping container model'
    _rec_name = 'ref'

    ref = fields.Char('Container Ref', tracking=True, readonly=True, required=True, index=True,
                      copy=False, default="New")
    transportation_way = fields.Selection([
        ('sea', 'Sea'),
        ('air', 'Air'),
        ('land', 'Land')], string='Transportation',
        copy=False, default='sea', index=True, tracking=True)
    from_warehouse_id = fields.Many2one("stock.warehouse", string="Origin WH",
                                        tracking=True, required=True)
    to_warehouse_id = fields.Many2one("stock.warehouse", string="Destination WH",
                                      tracking=True, required=True)
    current_location = fields.Char('Current location', tracking=True, readonly=True, index=True)
    total_weight = fields.Float("Total weight", default=0, tracking=True, readonly=True,
                                compute='_compute_total_weight')
    total_capacity = fields.Float("Total volume", default=0, tracking=True, readonly=True,
                                  compute='_compute_total_capacity')
    estimated_departure_date = fields.Date("Estimated departure", tracking=True, required=True)
    estimated_arrival_date = fields.Date("Estimated arrival", tracking=True, required=True)
    tracking_number = fields.Char("N° de tracking", readonly=True, index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked', 'Checked'),
        ('loaded', 'Loaded'),
        ('in_transit', 'In transit'),
        ('arrived', 'Arrived'),
        ('available', 'Available'),
        ('canceled', 'Canceled')], string='Status',
        copy=False, default='draft', index=True, readonly=True, tracking=True)
    packages_lines_ids = fields.One2many('nextewave.grouping.container.line',
                                         'grouping_package_container_id',
                                         string='Packages')

    @api.model
    def create(self, vals):
        res = super(NextewaveGroupingContainer, self).create(vals)
        res["ref"] = self.env["ir.sequence"].next_by_code("grouping.container.sequence") or "New"
        res["tracking_number"] = self.env["ir.sequence"].next_by_code("grouping.container.tracking.sequence") or "New"
        return res

    @api.depends('packages_lines_ids')
    def _compute_total_capacity(self):
        for rec in self:
            total_capacity = 0
            for line in rec.packages_lines_ids:
                total_capacity += line.capacity or 0.0
            rec.total_capacity = total_capacity

    @api.depends('packages_lines_ids')
    def _compute_total_weight(self):
        for rec in self:
            total_weight = 0
            for line in rec.packages_lines_ids:
                total_weight += line.weight or 0.0
            rec.total_weight = total_weight

