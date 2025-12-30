from odoo import api, models, fields,_
from odoo.exceptions import UserError

#we have added this module just for testing
class Etablissemen(models.Model):
    _name = "etablissement"

    _description = "etablissement de l'ADC"
    
    name = fields.Char(string="etablissement", required=True)
   