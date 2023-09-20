# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class NextewavePackageSize(models.Model):
    _name = 'nextewave.package.size'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Nextewave package size'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char('Name', tracking=True, required=True, index=True, copy=False)
    max_weight = fields.Float("Max weight (Kg)", required=True, tracking=True)
    max_width = fields.Float("Max width (m)")
    max_height = fields.Float("Max height (m)")
    max_depth = fields.Float("Max depth (m)")

