from datetime import timedelta
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class NextewaveCrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    selected_vendor = fields.Many2one('res.partner', string='Vendor', required=False, readonly=True,
                                      tracking=True)
    crm_product_ids = fields.One2many('nextewave.product.line', 'crm_lead', string='Products', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('not_qualified', 'Not Qualified'),
        ('processing', 'Processing'),
        ('quotation_created', 'Quotation created'),
        ('vendor_selected', 'Vendor selected'),
        ('purchase_created', 'Purchase created'),
        ('lost', 'Lost'),
        ('canceled', 'Canceled'),
        ('won', 'Won')], required=True, default='new', readonly=True, tracking=True)

    # @api.onchange('stage_id')
    # def _change_stage_value(self):
    #     _logger.warning("\n\n\n\n\n=============================================================\n\n\n\n")
    #     for lead in self:
    #         if lead.stage_id:
    #             _logger.warning(f"\n>>>>>>>>>>>BABABA: {lead.stage_id.name}\n\n\n\n")
    #             if lead.stage_id.sequence == 5:
    #                 lead.stage_id = lead._stage_find(domain=[('fold', '=', False)]).id