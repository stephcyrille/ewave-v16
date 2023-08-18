from datetime import timedelta
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class NextewaveCrmPurchase(models.Model):
    _inherit = 'purchase.order'

    opportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', check_company=True,
        domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.model
    def create(self, vals):
        res = super(NextewaveCrmPurchase, self).create(vals)
        if res.opportunity_id:
            print("\n\n\n=++++++BAAAAAAMMMMMMMMMMM+++++\n\n")
        return res