#!/usr/bin/env python3
"""
Figure 2: Hourly temperature–TDI distributions for two case-study cities (2024).

Both cities (Namegata, Japan and Fulton, USA) have nearly identical annual mean
temperatures (~290.6 K / ~17.5 °C) yet different annual mean TDI values
(~0.21 vs ~0.23). This demonstrates that TDI captures distributional information
lost in the annual mean temperature.

Each panel combines a temperature density distribution (upper, blue) with TDI
scatter points (lower, green), annotated with quantile reference lines.

Input data: case_points.xlsx (source data file, 4 rows × 8,791 columns)

Output: case_points_analysis.png (90 × 45 mm, 600 dpi)

Author: Yinyin Cai (ORCID: 0000-0002-7410-4510)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sys
import os


def plot_case_study(data_path: str = "case_points.xlsx",
                    output: str = "case_points_analysis.png"):
    """
    Generate the case-study hourly distribution plot.

    Parameters
    ----------
    data_path : str
        Path to case_points.xlsx.
    output : str
        Path for the output PNG file.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_excel(data_path)
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 8

    nature = {
        'blue': '#1f77b4', 'red': '#d62728', 'green': '#2ca02c',
        'orange': '#ff7f0e', 'purple': '#9467bd', 'brown': '#8c564b',
    }

    # ---- Figure layout (90 × 45 mm) ----
    mm2in = 1 / 25.4
    fig = plt.figure(figsize=(90 * mm2in, 45 * mm2in))
    ax_a = fig.add_axes([0.08, 0.1, 0.35, 0.8])
    ax_b = fig.add_axes([0.58, 0.1, 0.35, 0.8])

    def process_group(df, group_idx):
        """Extract T (Kelvin -> Celsius) and TDI hourly data for a city-pair."""
        r0 = group_idx * 2
        t_raw = df.iloc[r0, 7:].values.astype(float) - 273.15
        tdi_raw = df.iloc[r0 + 1, 7:].values.astype(float)
        t = t_raw[~np.isnan(t_raw)]
        tdi = tdi_raw[~np.isnan(tdi_raw)]
        info = {
            'name': df.iloc[r0, 5],
            'country': df.iloc[r0, 3],
            'lon': float(df.iloc[r0, 1]),
            'lat': float(df.iloc[r0, 2]),
        }
        return t, tdi, info

    def format_lon(lon):
        return f"{360 - lon:.1f}°W" if lon > 180 else f"{lon:.1f}°E"

    def draw_panel(ax, t, tdi, info, label, nature):
        """Draw combined density (T) + scatter (TDI) for one city."""
        t_mean = np.mean(t)
        tdi_mean = np.mean(tdi)
        q25, q50, q75 = np.percentile(t, [25, 50, 75])

        # T density (upper half)
        kde = stats.gaussian_kde(t)
        x_t = np.linspace(t.min(), t.max(), 1000)
        y_dens = kde(x_t)
        dens_max = y_dens.max()

        # TDI scatter (lower half, inverted)
        tdi_range = tdi.max() - tdi.min()
        scale = dens_max / tdi_range if tdi_range > 0 else 1
        y_tdi = -(tdi - tdi.min()) * scale
        y_tdi_mean = -(tdi_mean - tdi.min()) * scale

        y_upper = dens_max * 1.1
        y_lower = -(tdi_range * scale) * 1.1

        ax.plot(x_t, y_dens, color=nature['blue'], linewidth=1)
        ax.hist(t, bins=50, density=True, alpha=0.5, color=nature['blue'],
                edgecolor='white', linewidth=0.2)
        ax.scatter(t[:len(tdi)], y_tdi, color=nature['green'], s=1,
                   alpha=0.6, edgecolors='none')

        ax.set_xlim(t.min(), t.max())
        ax.set_ylim(y_lower, y_upper)
        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_color('black')
        ax.spines['bottom'].set_linewidth(0.5)

        # Reference lines
        ax.axhline(y=y_tdi_mean, color=nature['red'], linestyle='--', linewidth=1, alpha=0.8)
        ax.text(t.max(), y_tdi_mean, f'TDI mean={tdi_mean:.2f}', fontsize=6,
                color=nature['red'], va='bottom', ha='right')
        for val, clr, lbl in [(q25, nature['orange'], '25%'),
                               (q50, nature['purple'], '50%'),
                               (q75, nature['brown'], '75%')]:
            ax.axvline(x=val, color=clr, linestyle=':', linewidth=1, alpha=0.7)
            ax.text(val, y_upper * 1.02, lbl, fontsize=6, color=clr, ha='center', va='bottom')

        # Location annotation
        lon_str = format_lon(info['lon'])
        ax.text(0.5, 1.18,
                f"{info['name']} ({info['country']}, {lon_str}, {info['lat']:.1f}°N)\n"
                f"T mean={t_mean:.2f}°C, 2024",
                transform=ax.transAxes, fontsize=6, ha='center', va='bottom')

        ax.text(-0.17, 1.15, label, transform=ax.transAxes, fontsize=10,
                fontweight='bold', va='bottom', ha='left')
        ax.grid(True, alpha=0.3)
        for sp in ['top', 'right']:
            ax.spines[sp].set_visible(False)

        return ax

    # Draw both panels
    for ax, gid, lbl in [(ax_a, 0, 'a'), (ax_b, 1, 'b')]:
        t, tdi, info = process_group(df, gid)
        draw_panel(ax, t, tdi, info, lbl, nature)
        print(f"  {info['name']} ({info['country']}): T mean={np.mean(t):.2f}°C, TDI mean={np.mean(tdi):.4f}")

    plt.savefig(output, dpi=600, bbox_inches='tight')
    print(f"Figure 2 saved to: {output}")


if __name__ == '__main__':
    data_path = sys.argv[1] if len(sys.argv) > 1 else "case_points.xlsx"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "case_points_analysis.png"
    plot_case_study(data_path, out_path)
