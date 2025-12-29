from odoo import api, models, fields,_
from odoo.exceptions import UserError

class Edit_Montant_mois(models.TransientModel):
    _name = "edit.montant.mois.wizard" 
    _description = "Pour modifier les valeur d'un mois "

    semestre_id = fields.Many2one(comodel_name="semestre",ondelete="cascade")
    montant = fields.Float(required=True)
    remuneration_maitre = fields.Integer(required=True)
    mois = fields.Char(required=True,readonly=True)
    
    def action_modifier(self):
        self.ensure_one()

        if not self.semestre_id or not self.mois:
            raise UserError(_("Aucun semestre sélectionné"))
        
        record = self.env['semestre.mois'].search([
            ('semestre_id', '=', self.semestre_id.id),
            ('mois', '=', self.mois)
        ])

        record.write({
        'montant': self.montant,
        'remuneration_maitre': self.remuneration_maitre,})


    @api.model
    def default_get(self, fields_list):

        res = super().default_get(fields_list)
        semestre_mois_id = self.env.context.get('default_semestre_mois_id')
        if semestre_mois_id:
            line = self.env['semestre.mois'].browse(semestre_mois_id)
            if line :
                res.update({
                    
                    'semestre_id': line.semestre_id.id,
                    'mois':line.mois,
                    'montant': line.montant,
                    'remuneration_maitre': line.remuneration_maitre,
                })
                return res
        raise UserError(_("Error"))