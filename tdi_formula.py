#!/usr/bin/env python3
"""
TDI (Thermal Deviation Index) Formula — Core Module
=====================================================

This module provides the canonical implementation of the Thermal Deviation
Index, a dimensionless metric quantifying how far ambient temperature deviates
from optimal conditions for human economic activity.

The TDI is a four-parameter weakly asymmetric exponential function anchored to:
  - 0 °C   (freezing point of water)       → TDI = 1
  - 22.5 °C (centre of human comfort zone)  → TDI = 0 (minimum)
  - 36.5 °C (mean human body temperature)   → TDI = 1

Reference:
  Cai, Y. (2026). A global gridded dataset of the Thermal Deviation Index
  derived from ERA5 hourly temperature (1940-2024). Scientific Data.

Author: Yinyin Cai (ORCID: 0000-0002-7410-4510)
"""

import numpy as np
from typing import Union, Tuple
from numpy.typing import ArrayLike

# ============================================================================
# Canonical TDI Parameters (analytically solved from boundary conditions)
# ============================================================================
A = 8.4199        # Growth scale, upward deviation
B = -32.4940      # Growth scale, downward deviation
U = 31.5307       # Location parameter (°C)
C = -1.6625       # Vertical shift

T_OPT = 22.5      # Optimal temperature (°C)
T_FREEZE = 0.0    # Freezing point of water (°C)
T_BODY = 36.5     # Mean human body temperature (°C)


def tdi(temperature: Union[float, ArrayLike]) -> Union[float, np.ndarray]:
    """
    Compute the Thermal Deviation Index.

        TDI(T) = exp((T - U) / A) + exp((T - U) / B) + C

    Parameters
    ----------
    temperature : float or array-like
        2-m air temperature in degrees Celsius.

    Returns
    -------
    float or ndarray
        TDI value(s). TDI >= 0; TDI = 0 at T = 22.5 °C;
        0 < TDI < 1 for T in (0, 36.5); TDI > 1 for extreme temperatures.

    Examples
    --------
    >>> tdi(22.5)   # optimal
    0.0
    >>> tdi(0.0)    # freezing
    1.0
    >>> tdi(36.5)   # body temperature
    1.0
    >>> tdi(50.0)   # extreme heat
    7.8707...
    """
    return np.exp((temperature - U) / A) + np.exp((temperature - U) / B) + C


def verify(tol: float = 3e-5) -> dict:
    """
    Verify all four boundary conditions to numerical precision.

    Returns
    -------
    dict : {condition_name: {'target': value, 'computed': value, 'pass': bool}}
    """
    h = 1e-6
    results = {
        'f(22.5) = 0': {
            'target': 0.0,
            'computed': float(tdi(T_OPT)),
            'pass': abs(float(tdi(T_OPT))) < tol
        },
        "f'(22.5) = 0": {
            'target': 0.0,
            'computed': float((tdi(T_OPT + h) - tdi(T_OPT - h)) / (2 * h)),
            'pass': abs(float((tdi(T_OPT + h) - tdi(T_OPT - h)) / (2 * h))) < tol
        },
        'f(0) = 1': {
            'target': 1.0,
            'computed': float(tdi(T_FREEZE)),
            'pass': abs(float(tdi(T_FREEZE)) - 1.0) < tol
        },
        'f(36.5) = 1': {
            'target': 1.0,
            'computed': float(tdi(T_BODY)),
            'pass': abs(float(tdi(T_BODY)) - 1.0) < tol
        },
        'weak_asymmetry': {
            'target': '|a| != |b|',
            'computed': f'|{A}| vs |{abs(B)}|',
            'pass': abs(A) != abs(B)
        },
    }
    return results


def reference_table() -> dict:
    """TDI values at standard reference temperatures."""
    return {T: float(tdi(T)) for T in [0, 10, 18, 22.5, 27, 30, 36.5, 40, 50]}


def grid_id_to_lonlat(grid_id: int) -> Tuple[float, float]:
    """Convert grid_id (1–1,038,240) to (longitude, latitude) in degrees."""
    if not (1 <= grid_id <= 1038240):
        raise ValueError(f"grid_id out of range: {grid_id}")
    i = (grid_id - 1) % 1440
    j = (grid_id - 1) // 1440
    return (i * 0.25, -90 + j * 0.25)


def lonlat_to_grid_id(lon: float, lat: float) -> int:
    """Convert (longitude, latitude) to grid_id."""
    i = int(round(lon / 0.25)) + 1
    j = int(round((lat + 90) / 0.25)) + 1
    return i + (j - 1) * 1440


# ============================================================================
# Self-test
# ============================================================================
if __name__ == '__main__':
    print("TDI Formula Verification\n" + "=" * 45)
    results = verify()
    all_ok = True
    for name, r in results.items():
        ok = "PASS" if r['pass'] else "FAIL"
        if not r['pass']:
            all_ok = False
        if isinstance(r['computed'], float):
            print(f"  [{ok}] {name}: {r['computed']:.6e}")
        else:
            print(f"  [{ok}] {name}: {r['computed']}")
    print(f"\nAll conditions: {'PASS' if all_ok else 'FAIL'}")

    print("\nReference values:")
    for T, val in reference_table().items():
        print(f"  TDI({T:5.1f} °C) = {val:.4f}")
