# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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
    current_warehouse_id = fields.Many2one("stock.warehouse", string="Current WH",
                                           tracking=True, help="It could be for the first time the boat"
                                                               " internal warehouse (abstract WH)")
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
    history_lines_ids = fields.One2many('nextewave.grouping.container.location', 'container_id',
                                        string='History lines')

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

    def action_button_checked(self):
        self.ensure_one()
        if not self.packages_lines_ids:
            raise ValidationError("You must add at least 1 package in the container")
        self.write({
            'state': 'checked'
        })

    def action_button_load(self):
        self.ensure_one()
        if self.packages_lines_ids:
            # First check that the current warehouse is different of origin and from WH
            if self.from_warehouse_id == self.current_warehouse_id:
                raise ValidationError("The origin Warehouse must not be the same "
                                      "as the current Warehouse in this stage")
            elif self.to_warehouse_id == self.current_warehouse_id:
                raise ValidationError("The destination Warehouse must not be the same "
                                      "as the current Warehouse in this stage")
            else:
                for pack_line in self.packages_lines_ids:
                    location = self.env['stock.location'].sudo().search(
                        [('warehouse_id', '=', self.current_warehouse_id.id)])
                    if len(location) < 0:
                        raise ValidationError(
                            "You must create at least one location for the current Warehouse ")
                    else:
                        loc_id = location[0].id
                    pack_line.package_id.write({
                        'state': 'loaded',
                        'location_id': loc_id
                    })
                self.write({
                    'state': 'loaded'
                })

    @api.depends('packages_lines_ids')
    def action_button_start_the_journey(self):
        self.ensure_one()
        if self.packages_lines_ids:
            for pack_line in self.packages_lines_ids:
                for line in pack_line.package_id.items_lines_ids:
                    line.item_id.write({
                        'status': 'in_transit'
                    })
            self.write({
                'state': 'in_transit'
            })

    def action_update_location(self):
        self.ensure_one()
        ctx = {
            'default_container_id': self.id,
            'default_time': datetime.datetime.now(),
        }

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'nextewave.grouping.container.location',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': ctx,
        }

    @api.depends('history_lines_ids', 'packages_lines_ids')
    def action_set_is_arrived(self):
        self.ensure_one()
        is_arrived = False

        if self.history_lines_ids:
            # Check all container locations, if we have one line arrived, the container
            # is_arrived attribute will set to true
            for line in self.history_lines_ids:
                if line.is_arrived:
                    is_arrived = True
            # Here we update the state of the container only, if the state is set arrived and
            # the previous container state was in_transit
            if is_arrived:
                self.write({
                    'state': 'arrived'
                })
                # Then update also items status, because
                for pack_line in self.packages_lines_ids:
                    for line in pack_line.package_id.items_lines_ids:
                        line.item_id.write({
                            'status': 'almost_there'
                        })
            else:
                raise ValidationError("At least one location history must be set arrived!")


