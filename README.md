# TDI Thermal Deviation Index — Code Repository

Code accompanying the Scientific Data Data Descriptor: *"Thermal Deviation Index dataset derived from ERA5 hourly temperature, 1940–2024"*.

**Dataset DOI**: https://doi.org/10.6084/m9.figshare.33012002 (figshare)  
**Code DOI**: https://doi.org/10.6084/m9.figshare.33012194 (figshare)  
**License**: CC BY 4.0

## Contents

| File | Purpose |
|------|---------|
| `tdi_formula.py` | Core TDI function, parameter derivation, boundary-condition verification |
| `fig1_tdi_curve.py` | Figure 1: TDI function curve with anchor points and thermal zones |
| `fig2_case_study_cities.py` | Figure 2: hourly temperature–TDI distributions for two case-study cities (2024) |
| `fig3_global_divergence.py` | Figure 3: global temperature–TDI divergence trends (1940–2024) |
| `fig4_tdi_7panels.py` | Figure 4: long-term evolution of annual cumulative TDI distributions (7 panels) |
| `requirements.txt` | Python dependencies |

## Quick Start

```bash
pip install -r requirements.txt
```

### Verify the TDI formula

```bash
python tdi_formula.py
```

Expected output verifies all boundary conditions: TDI(22.5) = 0, TDI'(22.5) = 0, TDI(0) = 1, TDI(36.5) = 1.

### Figure 1 — TDI function curve

No external data required. Output: `tdi_function_curve.png` (140 × 90 mm, 600 dpi).

```bash
python fig1_tdi_curve.py [output_path]
```

### Figure 2 — Case-study cities

Requires `case_points.xlsx` source file.

```bash
python fig2_case_study_cities.py case_points.xlsx fig2_output.png
```

### Figure 3 — Global divergence trends

Requires intermediate analysis data files (`five_year_moving_average_results.csv`, `daily_statistics_with_differences.csv`).

```bash
python fig3_global_divergence.py /path/to/data/ fig3_output.png
```

### Figure 4 — Annual cumulative TDI distributions (7 panels)

Requires `grid_annual_tdi_cumulative_1940_2024.csv` from the TDI dataset (figshare DOI: 10.6084/m9.figshare.33012002). The script uniformly samples ~100,000 grid cells for efficient kernel density estimation.

```bash
python fig4_tdi_7panels.py /path/to/grid_annual_tdi_cumulative_1940_2024.csv [output_path]
```

## Dependencies

Python 3.11+ with:

```
numpy, scipy, pandas, matplotlib, openpyxl
```

See `requirements.txt` for minimum version constraints.

## Citation

If you use this code, please cite:

> Cai, Y. (2026). TDI thermal deviation index — code v1.0.0. *figshare*. https://doi.org/10.6084/m9.figshare.33012194

If you use the TDI dataset, please cite:

> Cai, Y. (2026). Global Thermal Deviation Index (TDI) Dataset 1940–2024. *figshare*. https://doi.org/10.6084/m9.figshare.33012002

## License

CC BY 4.0

## Contact

Yinyin Cai  
Center for Weather Management Engineering  
Nanjing University of Information Science and Technology  
Email: yyincai@nuist.edu.cn  
ORCID: 0000-0002-7410-4510
