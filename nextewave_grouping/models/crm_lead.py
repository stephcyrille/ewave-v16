
import datetime
import logging
from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)


class GroupingCrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave Grouping CRM Lead'

    def action_set_won_rainbowman(self):
        self.ensure_one()
        self.action_set_won()
        items_line = []
        for product in self.crm_product_ids:
            curr_product = self.env['product.product'].sudo().search([('id', '=', product.product_id['id'])])
            line = (
                0, 0, {
                    'name': curr_product.name,
                    'origin_document': self.name,
                    'customer_id': self.partner_id.id,
                    'material': 'other',
                    'quantity': product['product_qty'],
                    'price': product['price_unit'],
                    'weight': curr_product.weight,
                    'capacity': curr_product.volume
                }
            )
            items_line.append(line)

        data = {
            'customer_id': self.partner_id.id,
            'origin': 'unknown',
            'destination': 'unknown',
            'departure_date': datetime.datetime.now() + datetime.timedelta(weeks=1),
            'arrival_date': datetime.datetime.now() + datetime.timedelta(weeks=7),
            'material': 'mixed',
            'items_lines_ids': items_line
        }

        self.env['nextewave.grouping.package.request'].create(data)

        message = self._get_rainbowman_message()
        if message:
            self.write({
                'state': 'won',
            })
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': message,
                    'img_url': '/web/image/%s/%s/image_1024' % (self.team_id.user_id._name,
                                                                self.team_id.user_id.id) if self.team_id.user_id.image_1024 else '/web/static/src/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
        return True
