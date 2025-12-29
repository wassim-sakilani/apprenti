from odoo import api, models, fields,_
from odoo.exceptions import UserError

class structure(models.Model):
    _name = "structure"

    _description = "Structeur de l'ADC"
    
    name = fields.Char(string="Structure", required=True ,tracking=True)
   