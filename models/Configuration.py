from odoo import api, fields, models

class Configuration(models.TransientModel):
    _inherit = 'res.config.settings'

    smig = fields.Integer(string="SMIG",default=20000)

    def set_values(self):
        super(Configuration, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('apprenti.smig', self.smig)

    @api.model
    def get_values(self):
        res = super(Configuration, self).get_values()
        res['smig'] = int(self.env['ir.config_parameter'].sudo().get_param('apprenti.smig', default=20000))
        return res