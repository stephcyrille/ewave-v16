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
