from odoo import api, models, fields,_
from odoo.exceptions import UserError

class employe(models.Model):
    _name = "employe"

    _description = "employe de l'ADC"
    
    name = fields.Char(string="employe", required=True ,tracking=True)
   