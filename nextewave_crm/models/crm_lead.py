from datetime import timedelta

from odoo import models, fields, api, _


class NextewaveCrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    selected_vendor = fields.Many2one('res.partner', string='Vendor', required=False, readonly=True,
                                      tracking=True)
    crm_product_ids = fields.One2many('nextewave.product.line', 'crm_lead', string='Products', tracking=True)
