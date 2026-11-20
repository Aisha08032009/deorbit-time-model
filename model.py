"""
First-order orbital decay model (Section 1.2 of the paper):

        T  ~=  K * exp(h / H) / (A / m)

    T    deorbit time (years)
    h    initial altitude (km)
    H    atmospheric scale height (km)
    A/m  effective area-to-mass ratio (m^2/kg)
    K    empirical scaling constant

Two parameter sets are provided because the constants *printed* in the paper
(H = 50 km, K = 2.5e-5) do not reproduce the paper's own Table 3. Table 3 is
reproduced (drag sail essentially exactly, the other two within a few percent)
by H = 100 km and K = 2.5e-3. See RECONCILIATION.md and consistency.py.
"""
from dataclasses import dataclass

import numpy as np

from data import TABLE1, DRAG_SAIL, EDT, PROPULSION, SYSTEMS


@dataclass(frozen=True)
class ModelParams:
    K: float          # year * kg / m^2
    H: float          # km
    label: str


PRINTED = ModelParams(K=2.5e-5, H=50.0, label="constants as printed in the paper")
CALIBRATED = ModelParams(K=2.5e-3, H=100.0, label="constants that reproduce Table 3")


def effective_am(area_m2: float, total_mass_kg: float) -> float:
    """Effective area-to-mass ratio (m^2/kg)."""
    return area_m2 / total_mass_kg


def am_from_table1(system: str, use_printed_am: bool = False) -> float:
    """A/m for a system: either as printed in Table 1, or area / total mass."""
    row = TABLE1[system]
    return row["am"] if use_printed_am else effective_am(row["area"], row["total"])


def deorbit_time(h_km, am, params: ModelParams = CALIBRATED,
                 density_factor: float = 1.0, k_factor: float = 1.0):
    """
    Deorbit time in years.

    density_factor : multiplies atmospheric density (T is inversely proportional)
    k_factor       : multiplies the calibration constant K
    """
    h = np.asarray(h_km, dtype=float)
    return k_factor * params.K * np.exp(h / params.H) / (am * density_factor)


def table3(params: ModelParams = CALIBRATED, altitudes=(400, 500, 600, 700, 800),
           use_printed_am: bool = False) -> dict:
    return {s: deorbit_time(altitudes, am_from_table1(s, use_printed_am), params)
            for s in SYSTEMS}


def sensitivity(system: str = DRAG_SAIL, h_km: float = 600.0,
                params: ModelParams = CALIBRATED, use_printed_am: bool = False) -> dict:
    """The three perturbations described in Section 1.3."""
    am = am_from_table1(system, use_printed_am)
    base = float(deorbit_time(h_km, am, params))
    dens_hi = float(deorbit_time(h_km, am, params, density_factor=1.5))
    dens_lo = float(deorbit_time(h_km, am, params, density_factor=0.5))
    am_hi = float(deorbit_time(h_km, am * 1.1, params))
    am_lo = float(deorbit_time(h_km, am * 0.9, params))
    k_hi = float(deorbit_time(h_km, am, params, k_factor=1.15))
    k_lo = float(deorbit_time(h_km, am, params, k_factor=0.85))
    return dict(
        base=base,
        density_range=(dens_hi, dens_lo),
        density_spread_factor=dens_lo / dens_hi,          # low-density / high-density
        am_change_pct=(100 * (am_hi / base - 1), 100 * (am_lo / base - 1)),
        k_change_years=(k_lo - base, k_hi - base),
    )
