# from datetime import timedelta
import logging
import base64
from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)


class NextewavePackageRequestPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'NEXTeWave grouping package request Payment'

    grouping_package_request_id = fields.Many2one(
        'nextewave.grouping.package.request', string='Package request payment', check_company=True)

    @api.model
    def create(self, vals):
        res = super(NextewavePackageRequestPayment, self).create(vals)
        if res.grouping_package_request_id:
            grouping_package_request = self.env['account.payment'].sudo().search(
                [('grouping_package_request_id', '=', res.grouping_package_request_id.id)])
            # If we already have paid an opportunity, we don't need to edit his state
            if len(grouping_package_request) <= 1:
                res.grouping_package_request_id.write({
                    'state': 'paid'
                })

        return res


class NextewavePackageRequestInherited(models.Model):
    _inherit = 'nextewave.grouping.package.request'
    _description = 'NEXTeWave grouping package request inherited'

    payments_count = fields.Integer(string="Number of payment", default=0)
    payment_amount = fields.Float("Payment amount", default=0, tracking=True, readonly=True,
                                  compute='_compute_payment_count')

    def action_make_payment(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_account_payments")
        action['context'] = {
            'default_payment_type': 'inbound',
            'default_partner_type': 'customer',
            'default_partner_id': self.customer_id.id,
            'search_default_inbound_filter': 1,
            'default_move_journal_types': ('bank', 'cash'),
            'search_default_draft': 1,
            'default_grouping_package_request_id': self.id
        }

        action['views'] = [(self.env.ref('account.view_account_payment_form').id, 'form')]
        return action

    def action_view_payments(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_account_payments")
        action['context'] = {
            'search_default_partner_id': self.customer_id.id,
            'default_partner_id': self.customer_id.id,
            'default_grouping_package_request_idd': self.id
        }

        payment = self.env['account.payment'].sudo().search([('grouping_package_request_id', '=', self.id)])
        if len(payment) == 1:
            action['views'] = [(self.env.ref('account.view_account_payment_form').id, 'form')]
            action['res_id'] = payment.id
        return action

    def _compute_payment_count(self):
        self.ensure_one()
        """
            Count all payments for our grouping package request
        """
        payments = self.env['account.payment']. \
            sudo().search([('grouping_package_request_id', '=', self.id)])

        self.payments_count = len(payments)


