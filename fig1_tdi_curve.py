#!/usr/bin/env python3
"""
Figure 1: Thermal Deviation Index (TDI) function curve.

TDI(T) = exp((T - 31.5307) / 8.4199) + exp((T - 31.5307) / -32.4940) - 1.6625

X-axis: Temperature (degree C)
Y-axis: TDI (dimensionless)

Multi-zone fills: cold side (blue), warm side (orange), comfort zone (green),
cold stress T < 0 degree C (dark blue), heat stress T > 36.5 degree C (dark red).
Vertical reference line at T = 22.5 degree C.
Three anchor points: 0 degree C, 22.5 degree C, 36.5 degree C.

Output: tdi_function_curve.png (140 x 90 mm, 600 dpi)

Author: Yinyin Cai (ORCID: 0000-0002-7410-4510)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys


def tdi(T):
    """Compute TDI from temperature in degree Celsius."""
    return (np.exp((T - 31.5307) / 8.4199)
            + np.exp((T - 31.5307) / -32.4940)
            - 1.6625)


def plot_tdi_curve(output: str = "tdi_function_curve.png"):
    """Generate the TDI function curve figure."""

    # ---- Nature-inspired colour palette ----
    CURVE_COLOR   = '#2a5a8c'   # deep blue: main curve line
    COLD_FILL     = '#d0dff0'   # soft blue: cold-side under-curve
    WARM_FILL     = '#f5d5c8'   # soft orange: warm-side under-curve
    COLD_STRESS   = '#9ab5d4'   # muted blue: cold TDI > 1 zone
    WARM_STRESS   = '#e8a090'   # muted red: warm TDI > 1 zone
    COMFORT_FILL  = '#c5e0c5'   # pale green: comfort zone 18-27
    ANCHOR_RED    = '#b8423f'   # muted red: anchor point dots
    ANCHOR_GREEN  = '#4a8c4a'   # muted green: comfort optimum dot
    REF_GREY      = '#999999'   # reference lines
    TEXT_DARK     = '#333333'   # annotation text colour

    # ---- Style ----
    rcParams.update({
        'font.family': 'Arial',
        'font.size': 8,
        'axes.labelsize': 9,
        'axes.titlesize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'text.color': TEXT_DARK,
        'axes.edgecolor': '#cccccc',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 0.5,
        'xtick.major.width': 0.3,
        'ytick.major.width': 0.3,
    })

    # ---- Data ----
    T = np.linspace(-20, 52, 3000)
    Y = tdi(T)
    T_opt = 22.5

    # ---- Create figure ----
    fig, ax = plt.subplots(1, 1, figsize=(140/25.4, 90/25.4))

    # ==== ZONE FILLS (bottom to top) ====

    # -- Zone 1: Cold side (T < 22.5), below curve --
    T_cold = T[T <= T_opt]
    Y_cold = Y[T <= T_opt]
    ax.fill_between(T_cold, 0, Y_cold,
                    color=COLD_FILL, alpha=0.45, linewidth=0)

    # -- Zone 2: Warm side (T > 22.5), below curve --
    T_warm = T[T >= T_opt]
    Y_warm = Y[T >= T_opt]
    ax.fill_between(T_warm, 0, Y_warm,
                    color=WARM_FILL, alpha=0.45, linewidth=0)

    # -- Zone 3: Comfort zone (18-27 degree C) overlay --
    T_comf = np.linspace(18, 27, 500)
    ax.fill_between(T_comf, 0, tdi(T_comf),
                    color=COMFORT_FILL, alpha=0.5, linewidth=0)

    # -- Zone 4: Cold stress (T < 0, TDI > 1) --
    T_cs = T[T <= 0]
    Y_cs = tdi(T_cs)
    ax.fill_between(T_cs, 1, Y_cs,
                    color=COLD_STRESS, alpha=0.5, linewidth=0)

    # -- Zone 5: Warm stress (T > 36.5, TDI > 1) --
    T_ws = T[T >= 36.5]
    Y_ws = tdi(T_ws)
    ax.fill_between(T_ws, 1, Y_ws,
                    color=WARM_STRESS, alpha=0.5, linewidth=0)

    # ==== REFERENCE LINES ====

    # Vertical at T = 22.5 degree C
    ax.axvline(x=T_opt, color=ANCHOR_GREEN, linewidth=0.7,
               linestyle='--', alpha=0.5, zorder=2)

    # Horizontal at TDI = 0
    ax.axhline(y=0, color=REF_GREY, linewidth=0.4, linestyle='-', alpha=0.35, zorder=1)
    # Horizontal at TDI = 1
    ax.axhline(y=1, color=REF_GREY, linewidth=0.4, linestyle=':', alpha=0.35, zorder=1)

    # ==== MAIN CURVE ====
    ax.plot(T, Y, color=CURVE_COLOR, linewidth=1.5, zorder=5)

    # ==== ANCHOR POINTS ====
    anchors = [
        (0,     1.0, '0 °C\nFreezing point\nof water',     ANCHOR_RED,   'right'),
        (T_opt, 0.0, '22.5 °C\nComfort optimum\n(TDI = 0)', ANCHOR_GREEN, 'right'),
        (36.5,  1.0, '36.5 °C\nBody temperature',           ANCHOR_RED,   'left'),
    ]
    for Tx, Ty, label, color, side in anchors:
        # Dot
        ax.plot(Tx, Ty, 'o', color=color, markersize=7, zorder=7,
                markeredgecolor='white', markeredgewidth=1.2)
        # Annotation position
        if Tx == T_opt:
            # Move left of the vertical line to avoid overlap
            xytext = (T_opt - 6, 0.8)
            ha = 'center'
        elif Tx == 0:
            xytext = (5, 1.9)
            ha = 'left'
        else:
            xytext = (32, 1.9)
            ha = 'left'
        ax.annotate(label, (Tx, Ty), xytext=xytext,
                    fontsize=6.5, color=color, ha=ha, va='bottom',
                    linespacing=1.3,
                    arrowprops=dict(arrowstyle='->', color=color,
                                    lw=0.5, connectionstyle='arc3,rad=0.15'),
                    zorder=8)

    # ==== LABELS ====
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Thermal Deviation Index (TDI)')

    # ==== AXIS ====
    ax.set_xlim(-20, 52)
    ax.set_ylim(-0.3, 7.0)
    ax.set_xticks(np.arange(-20, 55, 10))
    ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])

    # ==== GRID (major + minor for density) ====
    ax.set_xticks(np.arange(-20, 55, 5), minor=True)
    ax.set_yticks(np.arange(0, 7.5, 0.5), minor=True)
    ax.grid(True, which='major', linestyle=':', linewidth=0.15, alpha=0.25)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.08, alpha=0.12)

    # ==== TITLE ====
    ax.set_title('Thermal Deviation Index (TDI)', pad=10, fontsize=10,
                 fontweight='normal', color=TEXT_DARK)

    # ==== LEGEND (no frame) ====
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLD_FILL,     alpha=0.6, label='Cold side (T < 22.5 °C)'),
        Patch(facecolor=WARM_FILL,     alpha=0.6, label='Warm side (T > 22.5 °C)'),
        Patch(facecolor=COMFORT_FILL,  alpha=0.6, label='Comfort zone (18–27 °C)'),
        Patch(facecolor=COLD_STRESS,   alpha=0.6, label='Cold stress (T < 0 °C)'),
        Patch(facecolor=WARM_STRESS,   alpha=0.6, label='Heat stress (T > 36.5 °C)'),
    ]
    ax.legend(handles=legend_elements, fontsize=5.5, loc='upper left',
              frameon=False, borderpad=0.3, labelspacing=0.3,
              handlelength=1.2, handleheight=0.8)

    # ==== SAVE ====
    plt.tight_layout()
    plt.savefig(output, dpi=600, bbox_inches='tight', facecolor='white',
                edgecolor='none')
    print(f'Saved: {output}')
    plt.close()


if __name__ == '__main__':
    output_path = sys.argv[1] if len(sys.argv) > 1 else 'tdi_function_curve.png'
    plot_tdi_curve(output_path)
