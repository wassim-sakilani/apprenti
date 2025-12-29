{
    "name": "Apprenti",
    "version": "14.0.1.0.0",
    "sequence": -100,
    "summary": "Un module pour la gestion des apprentis en Algerian Desalination Company (ADC) ",
    "author": "Sakilani Mohamed Wassim",
    "maintainer": "Sakilani Mohamed Wassim",
    "website": "mailto:wassim.sakilani@gmail.com",
    "depends": ["mail","hr","report_xlsx"],                
    "data": [
        "security/ir.model.access.csv",
        "data/data_apprenti.xml",
        "wizard/Edit_Montant_mois_view.xml",
        "wizard/Apprenti_report_wizard_view.xml",
        "views/structure_view.xml",
        "views/semestre_view.xml",
        "views/apprenti_view.xml",
        "views/department_view.xml",
        "views/employe_view.xml",
        "views/etablissement_view.xml",
        "views/station_view.xml",
        "views/configuration_view.xml",
        'reports/apprenti_xlsx_report.xml'
        
        
    ],
    "installable": True,
    "application": True,
}
