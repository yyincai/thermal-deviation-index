# TDI Thermal Deviation Index — Code Repository

Code accompanying the Scientific Data Data Descriptor: *"A global gridded dataset of the Thermal Deviation Index derived from ERA5 hourly temperature (1940–2024)"*.

**Dataset DOI**: https://doi.org/XXXXX (figshare / Zenodo)  
**Code DOI**: https://doi.org/XXXXX (Zenodo)  
**License**: CC BY 4.0

## Contents

| File | Purpose |
|------|---------|
| `tdi_formula.py` | Core TDI function, parameter derivation, boundary-condition verification |
| `fig1_global_divergence.py` | Generates Figure 1: global temperature–TDI divergence (1940–2024) |
| `fig2_case_study_cities.py` | Generates Figure 2: hourly temperature–TDI distributions for case-study cities |
| `requirements.txt` | Python dependencies |

## Quick Start

```bash
pip install -r requirements.txt
```

### Verify the TDI formula

```bash
python tdi_formula.py
```

Expected output verifies all four boundary conditions: TDI(22.5) = 0, TDI'(22.5) = 0, TDI(0) = 1, TDI(36.5) = 1.

### Regenerate Figure 1 (global divergence)

Requires intermediate analysis data files (`five_year_moving_average_results.csv`, `daily_statistics_with_differences.csv`).

```bash
python fig1_global_divergence.py /path/to/data/ fig1_output.png
```

### Regenerate Figure 2 (case-study cities)

Requires `case_points.xlsx` source file.

```bash
python fig2_case_study_cities.py case_points.xlsx fig2_output.png
```

## Dependencies

```
numpy, scipy, pandas, matplotlib, openpyxl
```

## Citation

If you use this code, please cite:

> Cai, Y. (2026). TDI-thermal-deviation-index: code accompanying the TDI dataset (v1.0.0). *Zenodo*. https://doi.org/XXXXX

If you use the TDI dataset, please cite:

> Cai, Y. (2026). Global Thermal Deviation Index (TDI) Dataset 1940–2024. *figshare*. https://doi.org/XXXXX

## License

CC BY 4.0

## Contact

Yinyin Cai  
Center for Weather Management Engineering  
Nanjing University of Information Science and Technology  
Email: yyincai@nuist.edu.cn  
ORCID: 0000-0002-7410-4510
