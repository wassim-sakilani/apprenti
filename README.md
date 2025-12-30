
# Apprenti
Apprentices Module
=======
# 🎓 Apprenticeship Management Module for Odoo

![Odoo Version](https://img.shields.io/badge/Odoo-14.0%2B-purple?style=flat-square)
![License](https://img.shields.io/badge/license-LGPL--3-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-Stable-green?style=flat-square)

## 📋 Description

The **Apprenticeship Management** module is a custom Odoo solution designed to streamline the administrative process of managing apprentices within an organization. It handles the entire lifecycle of an apprentice contract, from registration and semester tracking to remuneration calculation and reporting.

This module is essential for HR departments dealing with vocational training contracts, ensuring compliance with legal durations and simplifying payroll calculations based on semester progression.

## ✨ Key Features

### 👤 Apprentice Management
- **Comprehensive Profile:** Manage detailed information (Personal info, Contract ID, Structure, Department, Supervisor/Maitre).
- **Automated Sequencing:** Auto-generation of apprentice matricule numbers.
- **Status Tracking:** Automatic status updates (Open, In Progress, Finished) based on contract dates.
- **Document Attachment:** Upload fields for Contracts and Installation PVs.

### 📅 Semester & Education Tracking
- **Semester Logic:** Pre-defined semester types (S1 to S6) with validation checks.
- **Validation:** strict constraints to prevent overlapping dates or incorrect academic years (e.g., ensuring format YYYY/YYYY).
- **Remuneration Calculation:** Automatic calculation of monthly allowances based on the semester type (percentage of SMIG).
- **Monthly Breakdown:** Automatically generates a monthly payment breakdown for the duration of the semester.

### 📊 Reporting
- **Excel Export:** Built-in engine to export the "State of Apprentices" report in XLSX format using `report_xlsx`.
- **Dashboards:** Kanban and Tree views with useful filters and grouping (by State, Department, etc.).

## 🛠 Technical Details

- **Models:** `apprenti`, `semestre`, `semestre.mois`
- **Dependencies:** `base`, `mail`, `hr`, `report_xlsx`
- **Computed Logic:** - State calculation based on `today()` vs start/end dates.
  - Salary percentage logic (S1=20%, S2=30%, etc.).

## 🚀 Installation

1. Clone this repository into your Odoo addons path:
   ```bash
   git clone [https://github.com/wassim-sakilani/Apprentis.git](https://github.com/wassim-sakilani/Apprentis.git)

2. Update your Odoo configuration file (odoo.conf) to include the module path.

3. Restart the Odoo service.

4. Go to Apps, search for Apprenti, and click Install.

5. Note: Ensure report_xlsx library is installed.

## ⚙️ Configuration
  To adjust the SMIG (Guaranteed Minimum Interprofessional Wage) used for calculation:

1. Go to Settings > Technical > System Parameters.

2. Edit or Create a parameter named apprenti.smig.

3. Set the value (Default is 20,000 DZD).

### 🤝 Contribution
Contributions are welcome! Please fork the repository and submit a pull request.

