# from datetime import timedelta
import logging
import base64
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests


_logger = logging.getLogger(__name__)


class CrmProductPicture(models.Model):
    _name = 'nextewave.product.picture'
    _description = 'Nextewave product picture'

    product_pic1 = fields.Binary(string="Picture 1")
    product_pic2 = fields.Binary(string="Picture 2")
    product_pic3 = fields.Binary(string="Picture 3")
    product_pic4 = fields.Binary(string="Picture 4")

    def name_get(self):
        res = []
        for fields in self:
            related_crm_product = self.env['nextewave.product.line'].sudo().search(
                [('product_picture_id', '=', fields.id)])
            if len(related_crm_product) > 0:
                res.append((fields.id, f"Pictures/{related_crm_product[0].description}"))
            else:
                res.append((fields.id, f"Pictures/{fields.id}"))
        return res

