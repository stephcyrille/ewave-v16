# from datetime import timedelta
import logging
import base64
from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)


class NextewaveCrmPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'NEXTeWave Campaign Customer request Payment'

    customer_request_id = fields.Many2one(
        'buying.campaign.request', string='Customer request payment', check_company=True)

    @api.model
    def create(self, vals):
        res = super(NextewaveCrmPayment, self).create(vals)
        if res.customer_request_id:
            customer_request_payments = self.env['account.payment'].sudo().search(
                [('customer_request_id', '=', res.customer_request_id.id)])
            # If we already have paid an opportunity, we don't need to edit his state
            if len(customer_request_payments) < 1:
                res.customer_request_id.write({
                    'state': 'paid'
                })
        return res