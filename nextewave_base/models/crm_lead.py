# from datetime import timedelta
import logging
import base64
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests


_logger = logging.getLogger(__name__)


class NextewaveBaseCrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    state = fields.Selection([
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('not_qualified', 'Not Qualified'),
        ('processing', 'Processing'),
        ('po_created', 'PO created'),
        ('customer_so_created', 'SO created'),
        ('client_accepted', 'Client accepted'),
        ('lost', 'Lost'),
        ('canceled', 'Canceled'),
        ('won', 'Won')], required=True, default='new', readonly=True, tracking=True)

