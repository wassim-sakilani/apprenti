from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ApprentiReportWizard(models.TransientModel):
    _name = 'apprenti.report.wizard'
    _description = 'Wizard pour le rapport des apprentis'

    date_from = fields.Date(string="Date début (Contrat)")
    date_to = fields.Date(string="Date fin (Contrat)")
    
    structure_id = fields.Many2one('structure', string="Structure")
    department_id = fields.Many2one('hr.department', string="Département") 

    def action_print_report(self):
        domain = []
        
        if self.date_from:
            domain.append(('debut_apprendre', '>=', self.date_from))
        if self.date_to:
            domain.append(('debut_apprendre', '<=', self.date_to))

        if self.structure_id:
            domain.append(('structure_id', '=', self.structure_id.id))
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))

        semestre_actual = self.env['semestre'].search([('state', '=', 'en_cours')])
        apprenti_semestre_map = {}
        apprenti_ids = []
        if semestre_actual:
            apprenti_ids = semestre_actual.mapped('apprenti_id.id')
            for sem in semestre_actual:
                if sem.apprenti_id:
                    apprenti_semestre_map[sem.apprenti_id.id] = {
                        'semestre_type' : sem.semestre_type,
                        'montant_semestre':sem.montant_semestre,
                        'remuneration_maitre':sem.remuneration_maitre,
                    }
            
        if not apprenti_ids:
            raise UserError(_("Aucun apprenti trouvé avec ces critères."))
        
        domain.append(('id', 'in', apprenti_ids))

        apprentis = self.env['apprenti'].search(domain)
        if not apprentis:
            raise UserError(_("Aucun apprenti trouvé avec ces critères."))

        data = {
                'ids': apprentis.ids, 
                'model': 'apprenti',
                'apprenti_semestre_map': apprenti_semestre_map,
                }

        return self.env.ref('apprenti.action_report_apprenti_xlsx').report_action(apprentis.ids)
        