#!/usr/bin/env python3
"""
Figure 4: Long-term evolution of annual cumulative TDI distributions, 1940-2024.

Input: grid_annual_tdi_cumulative_1940_2024.csv
Strategy: uniform sample of ~100k grid cells for efficient KDE computation.

Panels:
  a,b,c: Ridgeline density by year (vertically stacked KDE, log10 scale)
  d,e,f: KDE overlay (all years on shared axis, transparency by year)
  g: Boxplot of log10(annual cumulative TDI) for land cells, 5-year intervals

Data groups: Global (all cells), Ocean (country == 'Ocean'), Land (countries)

Output: tdi_cumulative_7_panels.png (183 x 200 mm, 600 dpi)

Author: Yinyin Cai (ORCID: 0000-0002-7410-4510)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import sys
import warnings
warnings.filterwarnings('ignore')


def create_tdi_7_panels(csv_path, output_path='tdi_cumulative_7_panels.png'):
    print("Reading data (sampled)...")

    # Read country column + year columns, sampling every 10th row
    # First, read just the header to get column info
    with open(csv_path, 'r') as f:
        header = f.readline().strip().split(',')

    # Identify indices: country column and TDI_cum_XXXX columns
    country_idx = header.index('country')
    year_indices = []
    year_labels = []
    for i, col in enumerate(header):
        if col.startswith('TDI_cum_') and col.replace('TDI_cum_', '').isdigit():
            year_indices.append(i)
            year_labels.append(int(col.replace('TDI_cum_', '')))

    all_years = list(range(1940, 2025))
    display_years = [1940, 1944, 1949, 1954, 1959, 1964, 1969, 1974, 1979,
                     1984, 1989, 1994, 1999, 2004, 2009, 2014, 2019, 2024]

    # Read every 10th row to sample ~100k cells
    step = 10
    countries = []
    year_data = []
    row_count = 0
    with open(csv_path, 'r') as f:
        f.readline()  # skip header
        for line in f:
            if row_count % step == 0:
                parts = line.strip().split(',')
                countries.append(parts[country_idx])
                vals = [float(parts[i]) for i in year_indices]
                year_data.append(vals)
            row_count += 1

    countries = np.array(countries)
    year_data = np.array(year_data)  # shape: (n_samples, n_years)
    n_samples = len(countries)
    print(f"  Sampled {n_samples:,} cells from {row_count:,} total")

    # Split into groups
    is_ocean = (countries == 'Ocean')
    is_land = ~is_ocean & (countries != '') & (countries != 'NaN')

    all_log = {}
    ocean_log = {}
    land_log = {}

    for yi, yr in enumerate(year_labels):
        if yr not in all_years:
            continue

        # Global
        vals = year_data[:, yi]
        vals_g = vals[np.isfinite(vals)]
        if len(vals_g) > 0:
            mv = vals_g.min()
            if mv <= 0:
                vals_g = vals_g + abs(mv) + 0.001
            all_log[yr] = np.log10(vals_g)

        # Ocean
        vals_o = year_data[is_ocean, yi]
        vals_o = vals_o[np.isfinite(vals_o)]
        if len(vals_o) > 0:
            mv = vals_o.min()
            if mv <= 0:
                vals_o = vals_o + abs(mv) + 0.001
            ocean_log[yr] = np.log10(vals_o)

        # Land
        vals_l = year_data[is_land, yi]
        vals_l = vals_l[np.isfinite(vals_l)]
        if len(vals_l) > 0:
            mv = vals_l.min()
            if mv <= 0:
                vals_l = vals_l + abs(mv) + 0.001
            land_log[yr] = np.log10(vals_l)

        if yr % 20 == 0:
            print(f"  Extracted {yr} (global: {len(all_log[yr]):,}, "
                  f"ocean: {len(ocean_log.get(yr, [])):,}, "
                  f"land: {len(land_log.get(yr, [])):,})")

    # Global log range
    all_vals = np.concatenate(list(all_log.values()))
    log_min, log_max = all_vals.min(), all_vals.max()
    print(f"  Log10 range: {log_min:.2f} - {log_max:.2f}")

    # ---- Create figure ----
    width_mm, height_mm = 183, 200
    fig = plt.figure(figsize=(width_mm/25.4, height_mm/25.4))
    gs = plt.GridSpec(3, 3, height_ratios=[2, 1, 1], hspace=0.4, wspace=0.3)

    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])
    ax_d = fig.add_subplot(gs[1, 0])
    ax_e = fig.add_subplot(gs[1, 1])
    ax_f = fig.add_subplot(gs[1, 2])
    ax_g = fig.add_subplot(gs[2, :])

    plt.rcParams.update({'font.family': 'Arial', 'font.size': 8})

    titles = {
        'a': 'Global (1940-2024)',
        'b': 'Ocean (1940-2024)',
        'c': 'Land (1940-2024)',
        'd': 'Global (1940-2024)',
        'e': 'Ocean (1940-2024)',
        'f': 'Land (1940-2024)',
        'g': 'Land (1940-2024)',
    }
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_years)))
    y_ticks_pos = [all_years.index(y) * 1.0 for y in display_years if y in all_years]
    y_tick_labels_list = [str(y) for y in display_years if y in all_years]

    # ---- Panels a,b,c: Ridgeline ----
    print("Drawing ridgeline panels (a,b,c)...")
    for ax, data_dict, panel in zip(
        [ax_a, ax_b, ax_c], [all_log, ocean_log, land_log], ['a', 'b', 'c']
    ):
        for j, year in enumerate(all_years):
            arr = data_dict.get(year)
            if arr is None or len(arr) < 2:
                continue
            try:
                kde = gaussian_kde(arr)
                x_range = np.linspace(log_min, log_max, 600)
                y = kde(x_range)
                y_norm = y / y.max() * 0.8
                y_off = j * 1.0
                ax.fill_between(x_range, y_off, y_off + y_norm,
                                alpha=0.7, color=colors[j], linewidth=0)
                ax.plot(x_range, y_off + y_norm, color='black', linewidth=0.15)
            except Exception:
                continue

        ax.set_ylim(-0.8, len(all_years))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_yticks(y_ticks_pos)
        ax.set_yticklabels(y_tick_labels_list if panel == 'a' else [''] * len(y_ticks_pos),
                           fontsize=6)
        ax.set_xlim(log_min - 0.1, log_max + 0.1)
        ax.set_xlabel(r'$\log_{10}$(Annual cumulative TDI)', fontsize=6)
        ax.grid(True, alpha=0.25, linestyle='--', linewidth=0.2, axis='both')
        ax.set_title(titles[panel], fontsize=7, pad=4)
        ax.text(-0.1, 1.12, panel, transform=ax.transAxes, fontsize=9,
                fontweight='bold', verticalalignment='top')
        ax.tick_params(labelsize=6)

    # ---- Panels d,e,f: KDE overlay ----
    print("Drawing KDE overlay panels (d,e,f)...")
    for ax, data_dict, panel in zip(
        [ax_d, ax_e, ax_f], [all_log, ocean_log, land_log], ['d', 'e', 'f']
    ):
        for j, year in enumerate(all_years):
            arr = data_dict.get(year)
            if arr is None or len(arr) < 2:
                continue
            try:
                kde = gaussian_kde(arr)
                x_range = np.linspace(log_min, log_max, 400)
                y = kde(x_range)
                y_norm = y / y.max()
                alpha = 0.08 + 0.92 * (j / len(all_years))
                ax.plot(x_range, y_norm, color=colors[j], alpha=alpha, linewidth=0.25)
            except Exception:
                continue

        ax.set_xlabel(r'$\log_{10}$(Annual cumulative TDI)', fontsize=6)
        ax.set_ylabel('Density', fontsize=6)
        ax.set_xlim(log_min - 0.1, log_max + 0.1)
        ax.set_ylim(0, 1.1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.25, linestyle='--', linewidth=0.2, axis='both')
        ax.set_title(titles[panel], fontsize=7, pad=4)
        ax.text(-0.1, 1.12, panel, transform=ax.transAxes, fontsize=9,
                fontweight='bold', verticalalignment='top')
        ax.tick_params(labelsize=6)

    # ---- Panel g: Boxplot (Land) ----
    print("Drawing boxplot panel (g)...")
    box_data, box_labels = [], []
    for year in display_years:
        arr = land_log.get(year)
        if arr is not None and len(arr) > 0:
            box_data.append(arr)
            box_labels.append(str(year))

    if box_data:
        bp = ax_g.boxplot(box_data, labels=box_labels, patch_artist=True, widths=0.5)
        norm_p = plt.Normalize(vmin=1940, vmax=2024)
        for i, yr in enumerate(display_years):
            if i < len(bp['boxes']):
                bp['boxes'][i].set_facecolor(plt.cm.viridis(norm_p(yr)))
                bp['boxes'][i].set_alpha(0.7)
        for item in ['whiskers', 'caps']:
            for w in bp[item]:
                w.set_color('black')
                w.set_linewidth(0.6)
        for m in bp['medians']:
            m.set_color('black')
            m.set_linewidth(1.2)
        for fl in bp['fliers']:
            fl.set_marker('o')
            fl.set_markerfacecolor('gray')
            fl.set_markersize(1.5)
            fl.set_alpha(0.4)

    ax_g.set_ylabel(r'$\log_{10}$(Annual cumulative TDI)', fontsize=6)
    ax_g.tick_params(axis='both', labelsize=6)
    ax_g.tick_params(axis='x', rotation=45)
    ax_g.grid(True, alpha=0.25, linestyle='--', linewidth=0.2, axis='y')
    ax_g.spines['top'].set_visible(False)
    ax_g.spines['right'].set_visible(False)
    ax_g.set_title(titles['g'], fontsize=7, pad=4)
    ax_g.text(-0.05, 1.12, 'g', transform=ax_g.transAxes, fontsize=9,
              fontweight='bold', verticalalignment='top')

    # ---- Colorbar ----
    cbar_ax = fig.add_axes([0.15, 0.04, 0.7, 0.012])
    norm_c = plt.Normalize(vmin=1940, vmax=2024)
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm_c)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
    cbar.ax.tick_params(labelsize=6)
    cbar_ticks = list(range(1940, 2025, 15))
    if 2024 not in cbar_ticks:
        cbar_ticks.append(2024)
    cbar.set_ticks(cbar_ticks)

    # ---- Save ----
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.11)
    plt.savefig(output_path, dpi=600, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()


if __name__ == '__main__':
    DATA_PATH = r"D:\TDI论文\dataset\grid_annual_tdi_cumulative_1940_2024.csv"
    OUTPUT_PATH = 'tdi_cumulative_7_panels.png'
    if len(sys.argv) >= 2:
        DATA_PATH = sys.argv[1]
    if len(sys.argv) >= 3:
        OUTPUT_PATH = sys.argv[2]
    print("=" * 60)
    print("TDI Annual Cumulative 7-Panel Figure (sampled)")
    print("=" * 60)
    create_tdi_7_panels(DATA_PATH, OUTPUT_PATH)
    print("Done.")
