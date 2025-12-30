from odoo import api, models, fields,_
from odoo.exceptions import UserError


#we have added this module just for testing
class Structure(models.Model):
    _name = "structure"

    _description = "Structeur de l'ADC"
    
    name = fields.Char(string="Structure", required=True ,tracking=True)
   