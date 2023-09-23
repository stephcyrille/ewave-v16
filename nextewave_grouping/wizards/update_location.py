from odoo import api, fields, models, tools, _


class UpdateLocationWizard(models.Model):
    _name = 'nextewave.grouping.container.location'
    _rec_name = 'actual_location'
    _order = 'time desc'

    container_id = fields.Many2one("nextewave.grouping.container", string='Container', readonly=True)
    # TODO When we will mark as arrived, we will first check if there is another update location
    # for this container is arrived, then trigger a warning message
    is_arrived = fields.Boolean('is arrived', default=False, tracking=True)
    actual_location = fields.Char(string='Actual location', required=True)
    time = fields.Datetime("Date", tracking=True, readonly=True)
    comment = fields.Text(string='Comments')

    def action_save_update_location(self):
        self.ensure_one()
        self.container_id.write({
            'current_location': self.actual_location
        })
        return 0

