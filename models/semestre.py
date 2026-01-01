from odoo import api, models, fields,_
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

class Semestre(models.Model):
    _name = "semestre"
    _inherit = "mail.thread"
    _rec_name ="semestre_type"  
    _description = "Semestre"

    apprenti_id = fields.Many2one(comodel_name="apprenti",string="Apprenti",required=True,ondelete="cascade")

    nom_prenom = fields.Char(string= "Nom et Prenom" , compute="_compute_nom_prenom", store=True,readonly=True )
    
    semestre_type = fields.Selection([
        ('s1','S1'),
        ('s2','S2'),
        ('s3','S3'),
        ('s4','S4'),
        ('s5','S5'),
        ('s6','S6')
    ],required=True,tracking=True)

    SEMESTRE_RATES = {
        's1': 0.2,
        's2': 0.3,
        's3': 0.5,
        's4': 0.5,
        's5': 0.6,
        's6': 0.8,
    }

    annee_scolaire = fields.Char(string="Année Scolaire",required=True,help="Format: YYYY/YYYY (ex: 2024/2025)",tracking=True)

    debut_semestre = fields.Date(string="Debut de Semestre",required=True,tracking=True)
    fin_semestre = fields.Date(string="Fin de Semestre",required=True,tracking=True)

    state = fields.Selection([
        ('pas_encore', 'Ouvert'),
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé')
    ], string="Etat" ,compute="calcul_etat",store=True, readonly=True,tracking=True)

    certificat_scolaire = fields.Binary(string="Certificat Scolaire",tracking=True)
    remuneration_maitre = fields.Integer(string="Rémunération maitre d'apprentissage",required=True,tracking=True)

    montant_semestre = fields.Integer(string="Montant de cette semestre" , compute="calcul_montant" , readonly=True,tracking=True)
    #montant_mois = fields.Integer(string="Montant de cette mois" , compute="calcul_montant" , readonly=True)
    list_mois_ids = fields.One2many(comodel_name="semestre.mois",inverse_name="semestre_id",string="Mois du semestre",readonly=True)

    #methode pour calculer l'etat de semestre
    @api.depends('debut_semestre', 'fin_semestre')
    def calcul_etat(self):
        today = date.today()
        for rec in self:
            if not rec.debut_semestre or not rec.fin_semestre:
                rec.state = False
            elif today < rec.debut_semestre : 
                rec.state = 'pas_encore'
            elif rec.debut_semestre <= today and  today <= rec.fin_semestre :
                rec.state = 'en_cours'
            elif today > rec.fin_semestre  :
                rec.state = 'termine'

    #methode pour remplir le nom et le prénom
    @api.depends('apprenti_id.nom', 'apprenti_id.prenom')
    def _compute_nom_prenom(self):
        for rec in self:
            if rec.apprenti_id:
                rec.nom_prenom = f"{rec.apprenti_id.nom} {rec.apprenti_id.prenom}"
            else:
                rec.nom_prenom = False
    @api.model
    def create(self, vals):
        record = super(Semestre, self).create(vals)
        record.calcul_mois()
        return record
    
    def write(self, vals):
        res = super(Semestre, self).write(vals)
        if 'debut_semestre' in vals or 'fin_semestre' in vals or 'semestre_type' in vals:
            self.calcul_montant() 
            self.calcul_mois()
        return res

    #methode pour calculer le montant mensuelle
    @api.depends('semestre_type')
    def calcul_montant(self):
        smig_param = int(self.env['ir.config_parameter'].sudo().get_param('apprenti.smig', default=20000))
        smig =float(smig_param)
        for rec in self:
            rec.montant_semestre = 0
            if rec.semestre_type:
                percentage = self.SEMESTRE_RATES.get(rec.semestre_type, 0.0)
                rec.montant_semestre = percentage * smig
            else:
                rec.montant_semestre = 0


    #methode pour calculer les mois dans un semestre
    def calcul_mois(self):
        for rec in self:
            rec.list_mois_ids.unlink()
            if rec.debut_semestre and rec.fin_semestre :
                start = rec.debut_semestre.replace(day=1)
                end = rec.fin_semestre.replace(day=1)
                mois_vals = []
                while start <= end:
                    mois_vals.append({
                        'semestre_id': rec.id,
                        'mois': start.strftime('%B'),
                        'montant': rec.montant_semestre,
                        'remuneration_maitre': rec.remuneration_maitre,
                    })
                    start += relativedelta(months=1)
                if mois_vals:
                    self.env['semestre.mois'].create(mois_vals)

    #methode pour vérifier la durée de semestre s'il depasse 6 mois
    @api.constrains('debut_semestre', 'fin_semestre')
    def check_duration(self):
        for rec in self:
            if rec.debut_semestre and rec.fin_semestre:
                if rec.debut_semestre > rec.fin_semestre:
                    raise ValidationError("la fin du semestre doit être apres Le début du semestre.")
                six_months_later = rec.debut_semestre + relativedelta(months=6)
                if rec.fin_semestre > six_months_later:
                    raise ValidationError("La durée du semestre ne peut pas dépasser 6 mois.")
    
    #methode pour vérifier si l'apprenti a déjà étudié ce semestre.
    @api.constrains('apprenti_id','semestre_type')
    def check_semestre(self):
        for rec in self:
            search = self.env['semestre'].search([
            ('apprenti_id', '=', rec.apprenti_id.id),
            ('semestre_type', '=', rec.semestre_type),
            ('id', '!=', rec.id)
            ])
            if search :
                raise ValidationError(f"L'apprenti a déjà étudié le semestre {rec.semestre_type}.")

    #methode pour vérifier la structure de l'année scolaire entrer par l'utilisateur
    @api.constrains('annee_scolaire')
    def check_annee_scolaire(self):
        for rec in self:
            if rec.annee_scolaire:

                if '/' not in rec.annee_scolaire:
                    raise ValidationError("Le format de l'année scolaire doit être YYYY/YYYY (ex: 2024/2025)")

                parts = rec.annee_scolaire.split('/')
                if len(parts) != 2:
                    raise ValidationError("Le format de l'année scolaire doit être YYYY/YYYY (ex: 2024/2025)")
                
                try:
                    year1 = int(parts[0])
                    year2 = int(parts[1])

                    if year2 != year1 + 1:
                        raise ValidationError("La deuxième année doit être consécutive à la première (ex: 2024/2025)")

                except ValueError:
                    raise ValidationError("Le format de l'année scolaire doit contenir des années valides (ex: 2024/2025)")

    #methode pour vérifier si le semestre se situe dans l'année scolaire
    @api.constrains('debut_semestre', 'fin_semestre', 'annee_scolaire')
    def check_semestre_in_annee_scolaire(self):
        for rec in self:
            if rec.debut_semestre and rec.fin_semestre and rec.annee_scolaire:
                
                parts = rec.annee_scolaire.split('/')
                year1 = int(parts[0])
                year2 = int(parts[1])

                
                if not year1 or not year2:
                    continue

                # on suppose que l'année scholaire commancer le 1 september et terminer le 31 Août
                
                annee_debut_date = date(year1, 9, 1) 
                annee_fin_date = date(year2, 8, 31) 
                
                
                if rec.debut_semestre < annee_debut_date or rec.debut_semestre > annee_fin_date:
                    raise ValidationError(
                        f"La date de début du semestre ({rec.debut_semestre.strftime('%d/%m/%Y')}) "
                        f"doit être entre le 01/09/{year1} et le 31/08/{year2} "
                        f"pour l'année scolaire {rec.annee_scolaire}."
                    )
                
                if rec.fin_semestre < annee_debut_date or rec.fin_semestre > annee_fin_date:
                    raise ValidationError(
                        f"La date de fin du semestre ({rec.fin_semestre.strftime('%d/%m/%Y')}) "
                        f"doit être entre le 01/09/{year1} et le 31/08/{year2} "
                        f"pour l'année scolaire {rec.annee_scolaire}."
                    )
                if rec.debut_semestre < rec.apprenti_id.debut_apprendre or rec.fin_semestre > rec.apprenti_id.fin_apprendre :
                    raise ValidationError("La date de cette semestre doit étre inclu dans la periode d'aaprentissage de l'apprenti")
    
    #methode pour vérifier l'ordre de semestres
    @api.constrains('debut_semestre', 'fin_semestre', 'apprenti_id', 'semestre_type')
    def check_chronologie_semestres(self):
        
        sem_order = ['s1', 's2', 's3', 's4', 's5', 's6']
        
        for rec in self:
            if not rec.apprenti_id or not rec.semestre_type or not rec.debut_semestre or not rec.fin_semestre:
                continue

            overlap = self.search([
                ('apprenti_id', '=', rec.apprenti_id.id),
                ('id', '!=', rec.id), 
                ('debut_semestre', '<=', rec.fin_semestre),
                ('fin_semestre', '>=', rec.debut_semestre),
            ])
            if overlap:
                raise ValidationError(f"il ya un conflict avec semestre{overlap[0].semestre_type}.")

            try:
                current_idx = sem_order.index(rec.semestre_type)
            except ValueError:
                continue 

            previous_types = sem_order[:current_idx]
            if previous_types:
                prev_recs = self.search([
                    ('apprenti_id', '=', rec.apprenti_id.id),
                    ('semestre_type', 'in', previous_types),
                    ('id', '!=', rec.id)
                ])
                for prev in prev_recs:
                    if rec.debut_semestre <= prev.fin_semestre:
                         raise ValidationError(f"error in order : semestre{rec.semestre_type} Cela doit commencer après la date de fin du semestre {prev.semestre_type} ({prev.fin_semestre}).")


########################################################################################
#   This module represents the months in a semester,                                   #
#   allowing us to store the apprentice's and master's amounts.                        #
########################################################################################

class SemestreMois(models.Model):
    _name = "semestre.mois"
    _description = "Mois du semestre"

    semestre_id = fields.Many2one(comodel_name="semestre",ondelete="cascade")
    mois = fields.Char(required=True)
    montant = fields.Float(required=True)
    remuneration_maitre = fields.Integer(required=True)

    def action_open_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Modifier le mois',
            'res_model': 'edit.montant.mois.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_semestre_mois_id': self.id,
            }
        }