from datetime import timedelta
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NextewaveCrmSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        res = super(NextewaveCrmSaleOrder, self).create(vals)
        if res.opportunity_id:
            # Check if we already have a vendor order
            crm_stage_obj = self.env['crm.stage']
            stage = crm_stage_obj.sudo().search([('sequence', '=', 6)])
            res.opportunity_id.write({
                'quotation_count': 1,
                'state': 'customer_so_created',
                'stage_id': stage.id
            })
        return res