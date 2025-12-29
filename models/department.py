from odoo import api, models, fields,_
from odoo.exceptions import UserError

class department(models.Model):
    _name = "department"
    _description = "Department de l'ADC"
    
    name = fields.Char(string="Department", required=True )
    structure_id = fields.Many2one(comodel_name="structure" , string="Structure")
   