"""
Published values from:

Shermatova, A. (2026). Quantifying the Deorbit Time of CubeSats: A Comparative
Analysis of Drag Sails, Propulsion, and Tethers. Axiom Young Research, vol. 2.

All numbers here are transcribed exactly as printed in the paper
(Tables 1-3 and the figure/text claims), so the figures can be redrawn from them
and so model.py / consistency.py can be checked against them.
"""

ALTITUDES_KM = [400, 500, 600, 700, 800]
GUIDELINE_YEARS = 25.0

DRAG_SAIL = "Drag Sail"
EDT = "Electrodynamic Tether"
PROPULSION = "Propulsion System"
SYSTEMS = [DRAG_SAIL, EDT, PROPULSION]

# ---- Table 1: parameters (3U CubeSat, 4.0 kg, 10 x 10 x 30 cm) ---------------
BASE_MASS_KG = 4.00
BASE_AREA_M2 = 0.03            # 10 cm x 30 cm face

TABLE1 = {
    # system: dry mass, propellant mass, total system mass, area, total mass, A/m as printed
    "Base Satellite": dict(dry=None, prop=None, system=None, area=0.03, total=4.00, am=0.0075),
    DRAG_SAIL:        dict(dry=0.30, prop=0.00, system=0.30, area=2.00, total=4.30, am=0.468),
    EDT:              dict(dry=0.50, prop=0.00, system=0.50, area=0.10, total=4.50, am=0.024),
    PROPULSION:       dict(dry=0.80, prop=0.40, system=1.20, area=0.03, total=5.20, am=0.0058),
}

# ---- Table 2: validation set ("actual" is None for the two 12+ yr satellites) --
TABLE2 = [
    dict(name="GRB Alpha",  alt=535, mass=3.0,   am=0.010, actual=2.0,  predicted=2.2,   error_pct=+10.0),
    dict(name="DhabiSat",   alt=405, mass=4.0,   am=0.008, actual=1.4,  predicted=1.25,  error_pct=-10.7),
    dict(name="PERSEUS-M1", alt=475, mass=4.5,   am=0.007, actual=3.2,  predicted=3.55,  error_pct=+10.9),
    dict(name="ESTCube-1",  alt=665, mass=1.048, am=0.029, actual=None, predicted=45.2,  error_pct=None),
    dict(name="AAUSat-3",   alt=800, mass=0.8,   am=0.038, actual=None, predicted=112.3, error_pct=None),
]
REPORTED_MAE_PCT = 10.5

# ---- Table 3: calculated deorbit times (years) -------------------------------
TABLE3 = {
    DRAG_SAIL:  [0.3, 0.8, 2.2, 5.9, 16.0],
    EDT:        [5.8, 16.0, 43.5, 118.0, 320.0],
    PROPULSION: [24.0, 66.1, 179.5, 487.1, 1320.0],
}

# ---- Claims made in the text -------------------------------------------------
EDT_EXCEEDS_AT_600_PCT = 74
PROP_EXCEEDS_AT_600_PCT = 618
FIG4_MEAN_YEARS = 75.1
FIG4_COMPLIANCE_RATE_PCT = 33

# Residuals used in the residual histogram (predicted - actual, years)
RESIDUALS_YEARS = [+0.20, -0.15, +0.35]

# Sensitivity claims (Section 1.3)
SENS_CLAIM_DENSITY_FACTOR = (2, 3)           # "+-50% density changed times by a factor of 2-3"
SENS_CLAIM_AM_PCT = (8, 12)                  # "10% A/m uncertainty -> ~8-12% change"
SENS_CLAIM_K_YEARS_AT_600 = (0.3, 2.0)       # "15% K variation -> +-0.3 to 2 years at 600 km"


# ---- Revised validation set (used by corrected.py) ---------------------------
# Observed lifetimes re-checked against public orbital records after the
# published Table 2 was found to be inconsistent with them:
#   GRBAlpha   launched March 2021, re-entered ~9 June 2025          -> ~4.2 yr
#   DhabiSat   re-entered ~17 January 2024 (~2.6 yr after deployment June 2021)
#   PERSEUS-M1 launched June 2014 into a ~620 km orbit and still in orbit
#              (the published 475 km / 3.2 yr "decayed" entry was wrong)
# Mass and A/m are carried over unchanged from the published table.
TABLE2_REVISED = [
    dict(name="GRBAlpha",   alt=535, mass=3.0,   am=0.010, actual=4.2),
    dict(name="DhabiSat",   alt=405, mass=4.0,   am=0.008, actual=2.6),
    dict(name="ESTCube-1",  alt=665, mass=1.048, am=0.029, actual=None),
    dict(name="AAUSat-3",   alt=800, mass=0.8,   am=0.038, actual=None),
    dict(name="PERSEUS-M1", alt=620, mass=4.5,   am=0.007, actual=None),
]
