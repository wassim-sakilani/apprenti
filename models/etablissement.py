from odoo import api, models, fields,_
from odoo.exceptions import UserError

class etablissemen(models.Model):
    _name = "etablissement"

    _description = "etablissement de l'ADC"
    
    name = fields.Char(string="etablissement", required=True)
   