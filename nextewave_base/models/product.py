# from datetime import timedelta
import logging
import base64
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests


_logger = logging.getLogger(__name__)


class NextewaveCampaignProduct(models.Model):
    _inherit = 'product.template'
    _description = 'NEXTeWave campaign product'

    in_campaign = fields.Boolean('Is in campaign', default=False, tracking=True)