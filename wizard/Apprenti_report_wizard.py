from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ApprentiReportWizard(models.TransientModel):
    _name = 'apprenti.report.wizard'
    _description = 'Wizard pour le rapport des apprentis'

    date_from = fields.Date(string="Date début (Contrat)")
    date_to = fields.Date(string="Date fin (Contrat)")
    
    structure_id = fields.Many2one('structure', string="Structure")
    department_id = fields.Many2one('hr.department', string="Département")
    state = fields.Selection([
        ('pas_encore', 'Ouvert'),
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé')
    ], string="Etat")

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
        if self.state:
            domain.append(('state', '=', self.state))

        apprentis = self.env['apprenti'].search(domain)

        if not apprentis:
            raise UserError(_("Aucun apprenti trouvé avec ces critères."))

        return self.env.ref('apprenti.action_report_apprenti_xlsx').report_action(apprentis)