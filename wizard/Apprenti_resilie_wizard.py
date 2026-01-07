from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Apprenti_resilie_wizard(models.TransientModel):
    _name = 'apprenti.resilie.wizard'
    _description = 'Wizard pour la résiliation d\'un apprenti'

    date_resiliation = fields.Date(string="Date de Résiliation", required=True)
    resiliation_document = fields.Binary(string="Document de Résiliation", required=True)

    def action_resilier_apprenti(self):
        active_id = self.env.context.get('active_id')
        if not active_id:
            raise UserError(_("Aucun apprenti sélectionné ou identifiant invalide."))

        apprenti = self.env['apprenti'].browse(active_id).exists()
        if not apprenti:
            raise UserError(_("Aucun apprenti sélectionné."))
        
        semestres = self.env['semestre'].search([('apprenti_id','=',active_id),
                                                ('state','in', ['en_cours', 'pas_encore'])])
        
        if semestres:
            for rec in semestres:
                rec.write({'state': 'resilie'})

        apprenti.write({
            'state': 'resilie',
            'date_resiliation': self.date_resiliation,
            'resiliation_document': self.resiliation_document,
        })
        return {'type': 'ir.actions.act_window_close'}
        