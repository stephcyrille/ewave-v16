# from datetime import timedelta
import logging
import base64
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests


_logger = logging.getLogger(__name__)


class NextewaveCrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'NEXTeWave CRM Lead'

    selected_vendor = fields.Many2one('res.partner', string='Vendor', required=False, readonly=True,
                                      tracking=True)
    crm_product_ids = fields.One2many('nextewave.product.line', 'crm_lead', string='Products', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('not_qualified', 'Not Qualified'),
        ('processing', 'Processing'),
        ('quotation_created', 'Quotation created'),
        ('vendor_selected', 'Vendor selected'),
        ('purchase_created', 'Purchase created'),
        ('lost', 'Lost'),
        ('canceled', 'Canceled'),
        ('won', 'Won')], required=True, default='new', readonly=True, tracking=True)
    url = fields.Char('URL', default='https://www.nextewave.com')
    product_pic1_url = fields.Char(string="Picture 1 URL", required=False)
    product_pic1 = fields.Binary(string="Picture 1", compute='_compute_image_1_url', readonly=False, store=True)
    product_pic2_url = fields.Char(string="Picture 2 URL", required=False)
    product_pic2 = fields.Binary(string="Picture 2", compute='_compute_image_2_url', readonly=False, store=True)
    product_pic3_url = fields.Char(string="Picture 3 URL", required=False)
    product_pic3 = fields.Binary(string="Picture 3", compute='_compute_image_3_url', readonly=False, store=True)
    product_pic4_url = fields.Char(string="Picture 4 URL", required=False)
    product_pic4 = fields.Binary(string="Picture 4", compute='_compute_image_4_url', readonly=False, store=True)

    def get_image_from_url(self, url):
        """
        :return: Returns a base64 encoded string.
        """
        data = ""
        try:
            data = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
        except Exception as e:
            _logger.warning("Can't load the image from URL %s" % url)
            logging.exception(e)
        return data

    @api.depends("product_pic1_url")
    def _compute_image_1_url(self):
        for record in self:
            image = None
            if record.product_pic1_url:
               image = self.get_image_from_url(record.product_pic1_url)
               self.check_access_rule(image)
            record.update({"product_pic1": image, })

    @api.depends("product_pic2_url")
    def _compute_image_2_url(self):
        for record in self:
            image = None
            if record.product_pic2_url:
               image = self.get_image_from_url(record.product_pic2_url)
               self.check_access_rule(image)
               record.update({"product_pic2": image, })

    @api.depends("product_pic3_url")
    def _compute_image_3_url(self):
       for record in self:
           image = None
           if record.product_pic3_url:
               image = self.get_image_from_url(record.product_pic3_url)
               self.check_access_rule(image)
           record.update({"product_pic3": image, })

    @api.depends("product_pic4_url")
    def _compute_image_4_url(self):
       for record in self:
           image = None
           if record.product_pic4_url:
               image = self.get_image_from_url(record.product_pic4_url)
               self.check_access_rule(image)
           record.update({"product_pic4": image, })

    def action_set_won_rainbowman(self):
        self.ensure_one()
        self.action_set_won()

        message = self._get_rainbowman_message()
        if message:
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

    def action_button_qualify_lead(self):
        if self.expected_revenue == 0:
            raise ValidationError("Expected revenue must be greater than 0 !")
        if not self.partner_id:
            raise ValidationError("You need to add a partner before to continue")
        if not self.street:
            raise ValidationError("Address Error: Please fill the street on extra information before to continue !")
        elif not self.city:
            raise ValidationError("Address Error: Please fill the city on extra information before to continue !")
        elif not self.country_id:
            raise ValidationError("Address Error: Please fill the country on extra information before to continue !")
        elif not self.mobile:
            raise ValidationError("Contact missing: Please fill the mobile phone number before to continue !")
        else:
            # Set stage_id and synchronize it with custom state. If stage doesn't exist, we will create it
            crm_stage_obj = self.env['crm.stage']
            stage = crm_stage_obj.sudo().search([('sequence', '=', 2)])
            if not stage:
                raise ValidationError("You need to create qualified step that has sequence = 2")
            for rec in self:
                rec.write({
                    'state': 'qualified',
                    'stage_id': stage.id
                })

    def button_contact_salesperson(self):
        if not self.user_id:
            raise ValidationError("Please fill the salesperson before !")
        else:
            self.ensure_one()
            ir_model_data = self.env['ir.model.data']

            try:
                # template_id = ir_model_data.get_object_reference('nextewave_crm', 'crm_seller_template')[1]
                template_id = ir_model_data.sudo()._xmlid_lookup('nextewave_crm.crm_seller_template')[2]
            except ValueError:
                template_id = False
            try:
                compose_form_id = ir_model_data.sudo()._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
                # compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
            except ValueError:
                compose_form_id = False

            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            link = "%s/web#id=%s&view_type=form&model=crm.lead" % (web_base_url, self.id)
            for rec in self:
                rec.write({'url': link})

            ctx = {
                'default_model': 'crm.lead',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'mark_so_as_sent': True,
                'force_email': True,
                'mark_seller_added': True,
            }

            return {
                'name': _('Compose Email'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form_id, 'form')],
                'view_id': compose_form_id,
                'target': 'new',
                'context': ctx,
            }

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_seller_added'):
            # Set stage_id and synchronize it with custom state. If stage doesn't exist, we will create it
            crm_stage_obj = self.env['crm.stage']
            stage = crm_stage_obj.sudo().search([('sequence', '=', 3)])
            if not stage:
                raise ValidationError("You need to create qualified step that has sequence = 2")
            self.filtered(lambda o: o.state == 'qualified').write({'state': 'processing', 'stage_id': stage.id})
        return super(NextewaveCrmLead, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

