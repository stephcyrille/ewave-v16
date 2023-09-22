# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class NextewaveSaleGroupingItem(models.Model):
    _name = 'nextewave.grouping.item'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave grouping item'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char('Name', required=True, tracking=True)
    origin_document = fields.Char('Origin document', tracking=True)
    customer_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    material = fields.Selection([
        ('other', 'Other'),
        ('electronic', 'Electronic'),
        ('textile', 'Textile'),
        ('cosmetic', 'Cosmetic'),
        ('shoes', 'Shoes')], string='Material',
        copy=False, default='other', index=True, tracking=True)
    quantity = fields.Float('Quantity', tracking=True, required=True)
    # Compute the next 3 fields
    price = fields.Float('Unit price', default=0, tracking=True, help="Estimated unit price")
    weight = fields.Float("Unit Weight", default=0, tracking=True, help="Unit Weight (in Kg)")
    capacity = fields.Float("Unit Capacity", default=0, tracking=True, help="Unit Capacity (in m3)")
    grouping_package_request_id = fields.Many2one('nextewave.grouping.package.request',
                                                  ondelete='cascade', invisible=True)
    location_id = fields.Many2one("stock.location", string="Location", tracking=True, readonly=True,
                                  compute="_compute_location")
    status = fields.Selection([
        ('arrival', 'Arrival'),
        ('in_stock', 'In stock'),
        ('in_transit', 'In transit'),
        ('almost_there', 'Almost there'),
        ('picked_off', 'Picked off'),
        ('available', 'Available')], string='arrival',
        copy=False, default='arrival', index=True, tracking=True)
    is_locked = fields.Boolean('Is locked', default=False, tracking=True, readonly=True,
                               help="When the item is locked it is not possible to get it "
                                    "in grouping package request, it is lock for a specific "
                                    "grouping package, till the delivery or cancelling grouping package")

    @api.depends('grouping_package_request_id')
    def _compute_location(self):
        for rec in self:
            if rec.grouping_package_request_id:
                rec.location_id = rec.grouping_package_request_id.current_location_id.id
            else:
                rec.location_id = False

