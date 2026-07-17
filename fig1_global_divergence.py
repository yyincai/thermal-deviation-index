#!/usr/bin/env python3
"""
Figure 1: Global divergence between annual mean temperature and TDI (1940–2024).

Panel (a): 5-year moving average anomalies of global annual mean temperature
            and annual mean TDI, relative to the 1940–1944 baseline.
Panel (b): 5-year moving average anomalies of global daily mean and daily
            maximum TDI.

Input data requirements (intermediate analysis products):
  - five_year_moving_average_results.csv  (columns: year, Tmean_*_diff_from_base,
    TDImean_*_diff_from_base)
  - daily_statistics_with_differences.csv (columns: Date, Period, Mean_diff,
    Max_diff)

Output: combined_charts.png (140 × 75 mm, 600 dpi)

Author: Yinyin Cai (ORCID: 0000-0002-7410-4510)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


def plot_combined_charts(data_dir: str = ".", output: str = "combined_charts.png"):
    """
    Generate the combined divergence plot.

    Parameters
    ----------
    data_dir : str
        Directory containing the intermediate data files.
    output : str
        Path for the output PNG file.
    """
    # ---- Load data ----
    f1 = f"{data_dir}/five_year_moving_average_results.csv"
    f2 = f"{data_dir}/daily_statistics_with_differences.csv"

    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)

    # Filter: panel (a) from row index 1 (year 1945); panel (b) 5-year rolling
    df1_f = df1.iloc[1:]
    df2_f = df2.iloc[7:]
    df2_f = df2_f[df2_f['Period'] == '5_year_rolling_average']
    df2_f['Date'] = pd.to_datetime(df2_f['Date'])

    plt.rcParams['font.family'] = 'Arial'

    # ---- Figure layout (140 × 75 mm) ----
    mm2in = 1 / 25.4
    fig = plt.figure(figsize=(140 * mm2in, 75 * mm2in))

    # Panel (a): upper subplot
    ax1 = fig.add_axes([0, 0.55, 90/140, 35/75])
    ax1_tdi = ax1.twinx()

    # Panel (b): lower subplot
    ax2 = fig.add_axes([0.015, 0, 1, 40/75])
    ax2_max = ax2.twinx()

    # ---- Panel (a): annual mean T & TDI anomalies ----
    years = pd.to_numeric(df1_f['year'], errors='coerce')
    tmean_cols = ['Tmean_global_mean_diff_from_base', 'Tmean_country_mean_diff_from_base']
    tdimean_cols = ['TDImean_global_mean_diff_from_base', 'TDImean_country_mean_diff_from_base']
    tmean_c = ['#1f77b4', '#ff7f0e']
    tdimean_c = ['#d62728', '#9467bd']

    for i, col in enumerate(tmean_cols):
        if col in df1_f.columns:
            data = pd.to_numeric(df1_f[col], errors='coerce')
            if not data.isnull().all():
                ax1.plot(years, data, color=tmean_c[i], linewidth=0.75,
                         label=r'$\Delta T$ (global)' if 'global' in col else r'$\Delta T$ (countries)')
    for i, col in enumerate(tdimean_cols):
        if col in df1_f.columns:
            data = pd.to_numeric(df1_f[col], errors='coerce')
            if not data.isnull().all():
                ax1_tdi.plot(years, data, color=tdimean_c[i], linewidth=0.75, linestyle='--',
                             label=r'$\Delta TDI$ (global)' if 'global' in col else r'$\Delta TDI$ (countries)')

    ax1.set_xlim(1945, 2024)
    ax1.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax1.set_ylabel(r'$\Delta T_{\mathrm{yearly}}^{\mathrm{mean}}$ (°C)', fontsize=8, color=tmean_c[0])
    ax1_tdi.set_ylabel(r'$\Delta TDI_{\mathrm{yearly}}^{\mathrm{mean}}$', fontsize=8, color=tdimean_c[0])
    ax1.axhline(y=0, color='#1f77b4', linewidth=0.8, alpha=0.7)
    ax1_tdi.axhline(y=0, color='#d62728', linewidth=0.8, alpha=0.7)
    ax1.grid(True, which='major', alpha=0.3, linewidth=0.5)
    ax1.tick_params(labelsize=8)
    ax1_tdi.tick_params(labelsize=8)
    for sp in ['top', 'right']:
        ax1.spines[sp].set_visible(False)
        ax1_tdi.spines[sp].set_visible(False)

    lines = ax1.get_legend_handles_labels()
    lines_tdi = ax1_tdi.get_legend_handles_labels()
    ax1.legend(lines[0] + lines_tdi[0], lines[1] + lines_tdi[1],
               fontsize=6, frameon=False, loc='upper right')

    ax1.text(-0.08, 1.05, 'a', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', verticalalignment='top')

    # ---- Panel (b): daily mean & max TDI anomalies ----
    dates = df2_f['Date']
    mean_diff = pd.to_numeric(df2_f['Mean_diff'], errors='coerce')
    max_diff = pd.to_numeric(df2_f['Max_diff'], errors='coerce')

    ax2.plot(dates, mean_diff, color='#1f77b4', linewidth=0.5,
             label=r'$\Delta TDI_{\mathrm{daily}}^{\mathrm{mean}}$ (Mean)(global)')
    ax2_max.plot(dates, max_diff, color='#d62728', linewidth=0.5,
                 label=r'$\Delta TDI_{\mathrm{daily}}^{\mathrm{mean}}$ (Max)(global)')

    ax2.xaxis.set_major_locator(mdates.YearLocator(10))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.set_ylabel(r'$\Delta TDI_{\mathrm{daily}}^{\mathrm{mean}}$ (Mean)', fontsize=8, color='#1f77b4')
    ax2_max.set_ylabel(r'$\Delta TDI_{\mathrm{daily}}^{\mathrm{mean}}$ (Max)', fontsize=8, color='#d62728')
    ax2.axhline(y=0, color='#1f77b4', linewidth=0.8, alpha=0.7)
    ax2_max.axhline(y=0, color='#d62728', linewidth=0.8, alpha=0.7)
    ax2.grid(True, which='major', alpha=0.3, linewidth=0.5)
    ax2.tick_params(labelsize=8)
    ax2_max.tick_params(labelsize=8)
    for sp in ['top', 'right']:
        ax2.spines[sp].set_visible(False)
        ax2_max.spines[sp].set_visible(False)

    lines2 = ax2.get_legend_handles_labels()
    lines2_max = ax2_max.get_legend_handles_labels()
    ax2.legend(lines2[0] + lines2_max[0], lines2[1] + lines2_max[1],
               fontsize=6, frameon=False, loc='upper right')

    ax2.text(-0.08, 1.05, 'b', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', verticalalignment='top')

    plt.savefig(output, dpi=600, bbox_inches='tight')
    print(f"Figure 1 saved to: {output}")


if __name__ == '__main__':
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    out_path = sys.argv[2] if len(sys.argv) > 2 else "combined_charts.png"
    plot_combined_charts(data_dir, out_path)
