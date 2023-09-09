# from datetime import timedelta
import logging
import base64
from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)


class NextewaveCrmPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'NEXTeWave CRM Payment'

    opportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', check_company=True,
        domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.model
    def create(self, vals):
        res = super(NextewaveCrmPayment, self).create(vals)
        if res.opportunity_id:
            crm_stage_obj = self.env['crm.stage']
            stage = crm_stage_obj.sudo().search([('sequence', '=', 7)])
            opportunity_payments = self.env['account.payment'].sudo().search(
                [('opportunity_id', '=', res.opportunity_id.id)])
            # If we already have paid an opportunity, we don't need to edit his state
            if len(opportunity_payments) <= 1:
                res.opportunity_id.write({
                    'state': 'client_accepted',
                    'stage_id': stage.id
                })

        return res


class Crm(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    payments_count = fields.Integer(string="Number of payment", default=0)
    payment_amount = fields.Float("Payment amount", default=0, tracking=True, readonly=True,
                                  compute='_compute_payment_count')

    def action_goto_payment_form(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_account_payments")
        action['context'] = {
            'default_payment_type': 'inbound',
            'default_partner_type': 'customer',
            'default_partner_id': self.partner_id.id,
            'search_default_inbound_filter': 1,
            'default_move_journal_types': ('bank', 'cash'),
            'search_default_draft': 1,
            'default_opportunity_id': self.id
        }

        action['views'] = [(self.env.ref('account.view_account_payment_form').id, 'form')]
        return action

    def action_view_payments(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_account_payments")
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id,
        }

        payment = self.env['account.payment'].sudo().search([('opportunity_id', '=', self.id)])
        if len(payment) == 1:
            action['views'] = [(self.env.ref('account.view_account_payment_form').id, 'form')]
            action['res_id'] = payment.id
        return action

    def _compute_payment_count(self):
        self.ensure_one()
        """
            Count all payments for our CRM opportunity
        """
        payments = self.env['account.payment']. \
            sudo().search([('opportunity_id', '=', self.id)])

        if payments:
            self.payments_count = len(payments)
        else:
            self.payments_count = 0
