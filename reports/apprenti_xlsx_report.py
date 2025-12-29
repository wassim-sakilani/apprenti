from odoo import models

class ApprentiXlsx(models.AbstractModel):
    _name = 'report.apprenti.apprenti_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, apprentis):
        

        sheet = workbook.add_worksheet("Etat des apprentis")
        sheet.set_zoom(90) 
        sheet.set_paper(9)
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#D9D9D9', 
            'border': 1,
            'text_wrap': True 
        })

       
        text_format = workbook.add_format({
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })

        
        date_format = workbook.add_format({
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'num_format': 'dd/mm/yyyy'
        })

        
        currency_format = workbook.add_format({
            'font_size': 10,
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '#,##0.00 "DZD"'
        })

        
        sheet.set_column('A:A', 12) # N° Contrat
        sheet.set_column('B:B', 15) # Matricule
        sheet.set_column('C:C', 25) # Nom Prenom
        sheet.set_column('D:D', 35) # Spécialités
        sheet.set_column('E:F', 15) # Dates
        sheet.set_column('G:I', 25) # Structures/Dep/Station/Etab
        sheet.set_column('J:J', 35) # Etabblisment
        sheet.set_column('K:K', 15) # Semestre
        sheet.set_column('L:L', 15) # Presalaire
        sheet.set_column('M:M', 25) # Maitre
        sheet.set_column('N:N', 15) # Remuneration Maitre

        
        headers = [
            "N° Contrat", 
            "Matricule", 
            "Apprentis mis en place", 
            "Spécialités", 
            "Date début", 
            "Date fin", 
            "Structure", 
            "Departement", 
            "Station", 
            "Etablissement de formation", 
            "Semestre Actuel", 
            "Presalaire", 
            "Nom maitre d'apprentissage", 
            "Rémunération maitre d'apprentissage"
        ]

        
        for col_num, header_title in enumerate(headers):
            sheet.write(0, col_num, header_title, header_format)

        
        sheet.freeze_panes(1, 0)

        row = 1
        for obj in apprentis:
            
            full_name = f"{obj.nom} {obj.prenom}"
            
            sheet.write(row, 0, obj.num_contrat, text_format)          # A
            sheet.write(row, 1, obj.matricule, text_format)            # B
            sheet.write(row, 2, full_name, text_format)                # C
            sheet.write(row, 3, obj.speciality, text_format)           # D
            sheet.write(row, 4, obj.debut_apprendre, date_format)      # E
            sheet.write(row, 5, obj.fin_apprendre, date_format)        # F
            
            
            sheet.write(row, 6, obj.structure_id.name if obj.structure_id else "", text_format)    # G
            sheet.write(row, 7, obj.department_id.name if obj.department_id else "", text_format)  # H
            sheet.write(row, 8, obj.station_id.name if obj.station_id else "", text_format)        # I
            sheet.write(row, 9, obj.etablissement_id.name if obj.etablissement_id else "", text_format) # J
            
            
            sheet.write(row, 10, obj.semestre_display or "", text_format) # K
            
            
            sheet.write(row, 11, 0.0, currency_format)                 # L
            
            
            sheet.write(row, 12, obj.maitre_id.name if obj.maitre_id else "", text_format) # M
            
            
            sheet.write(row, 13, "", currency_format)                  # N

            row += 1