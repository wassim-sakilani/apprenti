from odoo import api, models, fields,_
from odoo.exceptions import UserError
from datetime import date
class Apprenti(models.Model):
    _name = "apprenti"
    
    _inherit = ['mail.thread','image.mixin']
    _description = "apprenti de l'ADC"
    _order = "matricule desc"


    
    
    # matricule de l'apprenti , va genére automatiquement par le sequenceur
    matricule = fields.Char(string="Matricule" , readonly=True
                            ,copy=False,default=lambda self:_('Nouveau')) 
    #Numéro de Contrat
    num_contrat = fields.Integer(string="Numéro de Contrat",required=True ,tracking=True )
    nom = fields.Char(string="Nom", required=True,tracking=True)
    prenom = fields.Char(string="Prénom", required=True,tracking=True)
    #Date de naissance 
    date_naiss = fields.Date(string="Date de naissance ",required=True,tracking=True)
    #Lieu de naissance 
    lieu_naiss = fields.Char(string="Lieu de naissance",required=True,tracking=True)
    telephone = fields.Char(string="Téléphone",required=True,tracking=True)
    email = fields.Char(string="Email",required=True,tracking=True)
    adress = fields.Char(string="Adress",required=True,tracking=True)
    photo = fields.Image(
    string="Photo",max_width=1024,max_height=1024,tracking=True)
    speciality = fields.Char(string="Spécialité",tracking=True)
    # Structure : réference de structure
    structure_id = fields.Many2one(comodel_name="structure",string="Structure",required=True,tracking=True)
    # departement : réference de departement
    department_id = fields.Many2one(comodel_name="hr.department",string="Departement",required=True,tracking=True)
    # station : réference de station
    station_id = fields.Many2one(comodel_name="station",string="Station",tracking=True)
    # etablissement : réference de etablissement
    etablissement_id = fields.Many2one(comodel_name="etablissement",string="Etablissement",required=True,tracking=True)
    # Nom maitre d'apprentisage: réference de l'employe
    maitre_id = fields.Many2one(comodel_name="hr.employee",string="Maitre D'apprentisage",required=True,tracking=True)
    #L'etat de l'apprenti
    state = fields.Selection([
        ('pas_encore', 'Ouvert'),
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé')
    ], string="Etat" ,compute="calcul_etat", store=True, readonly=True,tracking=True)
    #Début de l'apprentisage
    debut_apprendre = fields.Date(string="Début de l'apprentisage" ,required=True,tracking=True)
    #Fin de l'apprentisage
    fin_apprendre = fields.Date(string="Fin de l'apprentisage" ,required=True,tracking=True)
    #PV d'installation
    pv_installation = fields.Binary(string="PV d'installation",tracking=True)
    #Contrat
    contrat = fields.Binary(string="Contrat",tracking=True)

    semestre_ids = fields.One2many(comodel_name="semestre",inverse_name="apprenti_id",string="Semestres",readonly=True,tracking=True)
    semestre_display = fields.Char( string="Semestres",compute="_compute_semestre_display",store=False)

    #méthode pour calculer l'etat de l'apprenti
    @api.depends('debut_apprendre', 'fin_apprendre')
    def calcul_etat(self):
        today = date.today()
        for rec in self:
            if not rec.debut_apprendre or not rec.fin_apprendre:
                rec.state = 'pas_encore'
            elif today < rec.debut_apprendre : 
                rec.state = 'pas_encore'
            elif rec.debut_apprendre < today and  today < rec.fin_apprendre :
                rec.state = 'en_cours'
            elif today > rec.fin_apprendre  :
                rec.state = 'termine'


    @api.model
    def create(self,vals):
        if vals.get('matricule', _('Nouveau')) == _('Nouveau'):
            vals['matricule'] = self.env['ir.sequence'].next_by_code('apprenti') or _('Nouveau') 
        return super(Apprenti,self).create(vals)
    
    def action_open_semestre(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Créer Semestre',
            'res_model': 'semestre',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',  
            'context': {
                'default_apprenti_id': self.id,
                'form_view_initial_mode': 'edit',
                'apprenti_readonly': True, 
            }
        }
    
    def name_get(self):
        result = []
        for rec in self :
            matricule = rec.matricule or ''
            nom = rec.nom or ''
            prenom = rec.prenom or ''
            name = f"[{matricule}] {nom} {prenom}"
            result.append((rec.id,name))
        return result
    
    #méthode pour afficher les semestre en string (S1,S2,.....)
    def _compute_semestre_display(self):
        for rec in self:
            rec.semestre_display = ', '.join(rec.semestre_ids.mapped('semestre_type'))