"""
Cross-check the model and the paper's published numbers against each other.

Run:  python consistency.py
"""
import numpy as np

from data import (TABLE1, TABLE2, TABLE3, ALTITUDES_KM, SYSTEMS, DRAG_SAIL, EDT,
                  PROPULSION, GUIDELINE_YEARS, REPORTED_MAE_PCT,
                  EDT_EXCEEDS_AT_600_PCT, PROP_EXCEEDS_AT_600_PCT, FIG4_MEAN_YEARS,
                  FIG4_COMPLIANCE_RATE_PCT, SENS_CLAIM_AM_PCT, SENS_CLAIM_K_YEARS_AT_600)
from model import (PRINTED, CALIBRATED, deorbit_time, table3, am_from_table1,
                   sensitivity)


def _line(char="-", n=86):
    print(char * n)


def check_table1():
    print("\n[1] Table 1: A/m as printed vs area / total mass")
    _line()
    print(f"{'System':<24}{'printed A/m':>14}{'area/mass':>14}{'diff %':>10}")
    for s, row in TABLE1.items():
        calc = row["area"] / row["total"]
        d = 100 * (row["am"] - calc) / calc
        flag = "" if abs(d) < 1.5 else "  <-- check"
        print(f"{s:<24}{row['am']:>14.4f}{calc:>14.4f}{d:>+10.1f}{flag}")


def check_equation_constants():
    print("\n[2] Table 3 reproduced by Equation (1)")
    _line()
    for params in (PRINTED, CALIBRATED):
        print(f"\n  {params.label}:  K = {params.K:g}, H = {params.H:g} km")
        worst = 0.0
        for s in SYSTEMS:
            for use_printed in (True, False):
                model = deorbit_time(ALTITUDES_KM, am_from_table1(s, use_printed), params)
                pub = np.array(TABLE3[s])
                dev = 100 * (model - pub) / pub
                worst_s = np.abs(dev).max()
                if params is CALIBRATED:
                    src = "Table-1 A/m   " if use_printed else "area/total mass"
                    print(f"    {s:<22}{src:<16} max |dev| = {worst_s:6.1f}%")
                worst = max(worst, worst_s)
        if params is PRINTED:
            m = table3(PRINTED)
            print(f"    e.g. drag sail @600 km: model {m[DRAG_SAIL][2]:.2f} yr vs Table 3 "
                  f"{TABLE3[DRAG_SAIL][2]} yr; EDT {m[EDT][2]:.1f} vs {TABLE3[EDT][2]}; "
                  f"propulsion {m[PROPULSION][2]:.1f} vs {TABLE3[PROPULSION][2]}")
            print(f"    worst deviation anywhere: {worst:,.0f}%  -> printed constants do NOT reproduce Table 3")


def check_implied_am():
    print("\n[3] A/m implied by each published Table 3 value (H=100, K=2.5e-3)")
    _line()
    for s in SYSTEMS:
        implied = CALIBRATED.K * np.exp(np.array(ALTITUDES_KM) / CALIBRATED.H) / np.array(TABLE3[s])
        print(f"  {s:<22}{np.round(implied, 5)}   (Table 1: {TABLE1[s]['am']}, "
              f"area/mass: {TABLE1[s]['area'] / TABLE1[s]['total']:.5f})")


def check_validation():
    print("\n[4] Table 2 validation: errors and predictions")
    _line()
    errs = []
    for r in TABLE2:
        if r["actual"] is not None:
            e = 100 * (r["predicted"] - r["actual"]) / r["actual"]
            errs.append(abs(e))
            print(f"  {r['name']:<12} error recomputed {e:+6.1f}%  (printed {r['error_pct']:+.1f}%)")
    print(f"  mean absolute error recomputed: {np.mean(errs):.2f}%  (reported {REPORTED_MAE_PCT}%)")
    print("\n  Can Equation (1) reproduce the 'Predicted Lifetime' column?")
    print(f"  {'CubeSat':<12}{'alt':>6}{'A/m':>8}{'paper':>9}{'calibrated':>12}{'printed':>14}")
    for r in TABLE2:
        cal = float(deorbit_time(r["alt"], r["am"], CALIBRATED))
        prn = float(deorbit_time(r["alt"], r["am"], PRINTED))
        print(f"  {r['name']:<12}{r['alt']:>6}{r['am']:>8.3f}{r['predicted']:>9.2f}{cal:>12.2f}{prn:>14.2f}")
    print("  -> the predicted column is NOT reproduced by Equation (1) with either set of constants.")


def check_text_claims():
    print("\n[5] Numbers quoted in the text")
    _line()
    ed = 100 * (TABLE3[EDT][2] / GUIDELINE_YEARS - 1)
    pr = 100 * (TABLE3[PROPULSION][2] / GUIDELINE_YEARS - 1)
    print(f"  EDT over guideline at 600 km        : {ed:.0f}%   (text: {EDT_EXCEEDS_AT_600_PCT}%)")
    print(f"  Propulsion over guideline at 600 km : {pr:.0f}%  (text: {PROP_EXCEEDS_AT_600_PCT}%)")
    vals = [TABLE3[s][2] for s in SYSTEMS]
    print(f"  Fig. 4 mean deorbit time            : {np.mean(vals):.1f} yr (figure: {FIG4_MEAN_YEARS})")
    comp = 100 * sum(v < GUIDELINE_YEARS for v in vals) / len(vals)
    print(f"  Fig. 4 compliance rate              : {comp:.0f}%  (figure: {FIG4_COMPLIANCE_RATE_PCT}%)")


def check_sensitivity():
    print("\n[6] Section 1.3 sensitivity analysis at 600 km (density/A-m rows: model, drag sail; K rows: Table 3)")
    _line()
    s = sensitivity(DRAG_SAIL)
    print(f"  +-50% density : drag sail {s['density_range'][0]:.2f} to {s['density_range'][1]:.2f} yr "
          f"(ratio {s['density_spread_factor']:.1f}x between extremes; text: 'factor of 2-3')")
    print(f"  +-10% A/m     : {s['am_change_pct'][0]:+.1f}% / {s['am_change_pct'][1]:+.1f}%  "
          f"(text: {SENS_CLAIM_AM_PCT[0]}-{SENS_CLAIM_AM_PCT[1]}%)")
    print(f"  +-15% K       : change in deorbit time at 600 km, text says "
          f"+-{SENS_CLAIM_K_YEARS_AT_600[0]} to {SENS_CLAIM_K_YEARS_AT_600[1]} years")
    for sysname in SYSTEMS:
        base = TABLE3[sysname][2]
        print(f"      {sysname:<22} +-{0.15 * base:.2f} yr")


def main():
    print("=" * 86)
    print("CONSISTENCY CHECK: Shermatova (2026), Axiom Young Research vol. 2")
    print("=" * 86)
    check_table1()
    check_equation_constants()
    check_implied_am()
    check_validation()
    check_text_claims()
    check_sensitivity()


if __name__ == "__main__":
    main()
