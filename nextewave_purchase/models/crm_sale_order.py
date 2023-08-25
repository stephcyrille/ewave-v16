from datetime import timedelta
import logging
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class NextewaveCrmSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, fields, context=None):
        if context is None:
            context = self.env.context
        res = super(NextewaveCrmSaleOrder, self).default_get(fields)
        crm_products = context.get('crm_products', False)
        opportunity_id = context.get('default_opportunity_id', False)
        order_line = []
        if opportunity_id:
            for product in crm_products:
                curr_product = self.env['product.product'].sudo().search([('id', '=', product['id'])])
                line = (
                    0, 0, {
                        'name': curr_product.name,
                        'product_id': curr_product.id,
                        'product_uom_qty': product['qty'],
                        'product_uom': curr_product.uom_id.id,
                        'price_unit': product['price']
                    }
                )
                order_line.append(line)
            res.update({
                'order_line': order_line,
            })
        return res

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

    def action_confirm(self):
        # self.get_current_balance()
        print("Ptrrrrrrrrrrrrrrrrrrrrrrrrr\n\n\n\n\n\n")
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True

    def action_confirm(self):
        self.ensure_one()
        self.get_current_balance()
        print("Ptrrrrrrrrrrrrrrrrrrrrrrrrr\n\n\n\n\n\n")
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        crm_stage_obj = self.env['crm.stage']
        stage = crm_stage_obj.sudo().search([('sequence', '=', 7)])
        self.opportunity_id.write({
            'state': 'order_paid',
            'stage_id': stage.id
        })
        return True

    def get_current_balance(self):
        self.ensure_one()
        sale_order_obj = self.env['sale.order']
        theoretical_balance = 0
        current_balance = 0
        active_order_amount = 0
        # Get user by context value and state sale
        order_list = sale_order_obj.sudo().search([('partner_id', '=', self.partner_id.id)])
        for o in order_list:
            active_order_amount += o.amount_total

        current_balance = theoretical_balance - active_order_amount
        print("\n\n===========================\n")
        print("Order total amount is ", active_order_amount)
        print("\n")
        print("Order total amount is ", current_balance)
        print("\n\n===========================\n\n\n\n")