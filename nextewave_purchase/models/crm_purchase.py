import datetime
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
    def default_get(self, fields, context=None):
        if context is None:
            context = self.env.context
        res = super(NextewaveCrmPurchase, self).default_get(fields)
        print('\n\n\n===============\n')
        print(res)
        print('\n\n\n===============\n\n')
        crm_products = context.get('crm_products', False)
        opportunity_id = context.get('default_opportunity_id', False)
        order_line = []
        if opportunity_id:
            for product in crm_products:
                curr_product = self.env['product.product'].sudo().search([('id', '=', product['id'])])

                line = (
                    0, 0, {
                        'name': curr_product.name,
                        # 'display_type': False,
                        'date_planned': datetime.datetime.now(),
                        'product_id': curr_product.id,
                        'product_qty': product['qty'],
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
        res = super(NextewaveCrmPurchase, self).create(vals)
        if res.opportunity_id:
            crm_stage_obj = self.env['crm.stage']
            stage = crm_stage_obj.sudo().search([('sequence', '=', 5)])
            res.opportunity_id.write({
                'vendor_order_count': res.opportunity_id.vendor_order_count + 1,
                'state': 'po_created',
                'stage_id': stage.id
            })

        # print('\n\n\n===============\n')
        # print(res.id)
        # print(res.sequence)
        # print(res.product_uom)
        # print(res.product_id)
        # print(res.order_id)
        # print(res.company_id)
        # print(res.partner_id)
        # print(res.currency_id)
        # print(res.product_packaging_id)
        # print(res.create_uid)
        # print(res.write_uid)
        # print(res.state)
        # print(res.qty_received_method)
        # print(res.display_type)
        # print(res.analytic_distribution)
        # print(res.name)
        # print(res.product_qty)
        # print(res.product_qty)
        #
        # print(res._unit)
        # print(res.price_subtotal)
        # print(res.price_total)
        # print(res.qty_invoiced)
        # print(res.qty_received)
        # print(res.qty_received_manual)
        # print(res.qty_to_invoice)
        # print(res.date_planned)
        # print(res.create_date)
        # print(res.write_date)
        # print(res.product_uom_qty)
        # print(res.price_tax)
        # print(res.product_packaging_qty)
        # print(res.orderpoint_id)
        # print(res.product_descri)
        # print(res.ption_variants)
        # print(res.propagate_cancel)
        # print(res.sale_order_id)
        # print(res.sale_line_id)
        # print('\n\n\n===============\n\n')
        return res

