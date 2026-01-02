from odoo import api, fields, models


#The SMIG represents the basic wage, which we will use to calculate the amounts
class Configuration(models.TransientModel):
    _inherit = 'res.config.settings'

    smig = fields.Integer(string="SMIG", config_parameter='apprenti.smig',default=20000)

    rate_s2 = fields.Float(string="Taux S2", config_parameter='apprenti.rate_s2', default=0.3)
    rate_s1 = fields.Float(string="Taux S1", config_parameter='apprenti.rate_s1', default=0.2)
    rate_s3 = fields.Float(string="Taux S3", config_parameter='apprenti.rate_s3', default=0.5)
    rate_s4 = fields.Float(string="Taux S4", config_parameter='apprenti.rate_s4', default=0.5)
    rate_s5 = fields.Float(string="Taux S5", config_parameter='apprenti.rate_s5', default=0.6)
    rate_s6 = fields.Float(string="Taux S6", config_parameter='apprenti.rate_s6', default=0.8)
