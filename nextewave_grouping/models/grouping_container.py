# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .libs import generate_ean


class NextewaveGroupingContainer(models.Model):
    _name = 'nextewave.grouping.container'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'NEXTeWave grouping container model'

    _rec_name = 'ref'

    ref = fields.Char('Container Ref', tracking=True, readonly=True, required=True, index=True,
                      copy=False, default="New")

    total_weight = fields.Float("Total weight", default=0, tracking=True, readonly=True,
                                compute='_compute_total_weight')
    total_capacity = fields.Float("Total volume", default=0, tracking=True, readonly=True,
                                  compute='_compute_total_capacity')
    creation_date = fields.Date("Creation date", tracking=True, default=fields.Date.today(),
                                readonly=True)
    estimated_departure_date = fields.Date("Estimated departure", tracking=True, required=True)
    estimated_arrival_date = fields.Date("Estimated arrival", tracking=True, required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked', 'Checked'),
        ('locked', 'Locked'),
        ('canceled', 'Canceled'),
        ('confirmed', 'Confirmed'),
        ('loaded', 'Loaded'),
        ('unloaded', 'Unloaded')], string='Status',
        copy=False, default='draft', index=True, readonly=True, tracking=True)

    @api.model
    def create(self, vals):
        res = super(NextewaveGroupingContainer, self).create(vals)
        res["ref"] = self.env["ir.sequence"].next_by_code("grouping.container.sequence") or "New"
        ean = generate_ean(str(res.id))
        res.barcode = ean
        return res