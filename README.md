# Breast Cancer Patient Data System

A structured clinical data storage and management system developed as a Bachelor's Thesis at **Hospital Clínico San Carlos** (Madrid), in collaboration with the oncology research unit.

The system enables clinicians and researchers to import, organise, and query multi-source patient data from a breast cancer cohort study, replacing fragmented spreadsheet workflows with a unified, standardised data pipeline.

> **Note:** All data files included in this repository are anonymised synthetic samples. No real patient data is stored or distributed.

---

## Motivation

Clinical research teams frequently collect patient data across multiple instruments and time points — anthropometrics, blood analytics, physical function tests, dietary assessments, ultrasound measurements — each exported in different formats. This project provides a unified Python-based pipeline to import, validate, and structure all data sources into a single queryable system, with a graphical user interface designed for non-technical clinical staff.

---

## Features

- **Multi-source data import** — structured importers for 9 data types: general patient data, visit records, analytics, anthropometrics, ultrasound (eco), impedance, IPAQ (physical activity), MEDAS (Mediterranean diet), and SPPB (physical performance)
- **Baseline + follow-up support** — each data type handles both initial (`baseline`) and follow-up (`_seg`) visits
- **Data merging** — automated fusion of baseline and follow-up records into a unified dataset
- **Export automation** — scripts for generating standardised exports in researcher-preferred formats
- **REDCap integration** — data models aligned with REDCap clinical data standards
- **GUI application** — Python-based interface packaged as a standalone `.exe` for hospital deployment

---

## Repository Structure

```
breast-cancer-data-system/
├── importacion_*.py          # Per-datatype import scripts (baseline)
├── importacion_*_seg.py      # Per-datatype import scripts (follow-up)
├── automatizacion_exportacion/  # Export automation scripts
├── docs/                     # Project documentation and thesis materials
├── data/                     # Anonymised sample CSV files
│   ├── datos_generales.csv
│   ├── datos_analitica.csv
│   ├── datos_antropometricos.csv
│   ├── datos_eco.csv
│   ├── datos_impedancia.csv
│   ├── datos_ipaq.csv
│   ├── datos_medas.csv
│   ├── datos_sppb.csv
│   ├── datos_visita.csv
│   └── ...
└── generacion_exe_aplicacion.txt  # Instructions for packaging the GUI as .exe
```

---

## Data Types Handled

| Module | Description |
|--------|-------------|
| `datos_generales` | General patient demographics and diagnosis info |
| `datos_analitica` | Blood analytics results |
| `datos_antropometricos` | Anthropometric measurements (weight, BMI, etc.) |
| `datos_eco` | Ultrasound (ecography) measurements |
| `datos_impedancia` | Bioelectrical impedance analysis |
| `datos_ipaq` | IPAQ physical activity questionnaire |
| `datos_medas` | MEDAS Mediterranean diet adherence score |
| `datos_sppb` | SPPB physical performance battery |
| `datos_visita` | Visit metadata and scheduling |

Each module has a `baseline` and `_seg` (follow-up) variant.

---

## Tech Stack

- **Python** — core data processing and GUI
- **REDCap** — clinical data standard alignment
- **pandas / openpyxl** — data manipulation and Excel export
- **tkinter** — graphical user interface
- **PyInstaller** — packaging as standalone `.exe` for hospital deployment

---

## Context

This project was developed as the Bachelor's Thesis for a BSc in Biomedical Engineering at **Universidad Politécnica de Madrid**, in partnership with the oncology unit at **Hospital Clínico San Carlos**. It was subsequently presented at the **Spanish Biomedical Engineering Society Congress (CASEIB 2024)**.

📄 [Published paper — CASEIB 2024](https://example.com) <!-- replace with actual link if available -->

---

## Author

**Ana Pascual López** — Biomedical Engineer, MSc ML for Health  
[LinkedIn](https://www.linkedin.com/in/anapascual-biomedicalengineer) · [GitHub](https://github.com/anapascual)