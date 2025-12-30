from odoo import api, models, fields,_
from odoo.exceptions import UserError


#we have added this module just for testing
class Station(models.Model):
    _name = "station"

    _description = "station de l'ADC"
    
    name = fields.Char(string="station", required=True )
   