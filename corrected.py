"""
Corrected numbers, figures and LaTeX fragments, all derived from the model.

Corrections applied (see corrected/CORRIGENDUM.tex):
  * Equation (1) constants:  H = 100 km, K = 2.5e-3  (printed: 50 km, 2.5e-5)
  * A/m = effective area / total mass  (Table 1 printed 0.468 and 0.024)
  * Table 3, every derived percentage, thresholds and sensitivity numbers are
    recomputed from the model rather than copied.

The corrected validation table is generated from TABLE2_REVISED, and
the original residual plot is replaced by predicted-versus-observed values.
Validation satellite areas and masses remain source assumptions.

Run:  python corrected.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import figures
from data import (ALTITUDES_KM, SYSTEMS, DRAG_SAIL, EDT, PROPULSION, TABLE1, TABLE2_REVISED,
                  GUIDELINE_YEARS)
from model import CALIBRATED, am_from_table1, deorbit_time, sensitivity

OUT = Path("corrected")
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

P = CALIBRATED
am = {s: am_from_table1(s) for s in SYSTEMS}
t3 = {s: [round(float(x), 1) for x in deorbit_time(ALTITUDES_KM, am[s], P)] for s in SYSTEMS}


def threshold_altitude(system):
    """Altitude (km) at which deorbit time equals the 25-year guideline."""
    return P.H * np.log(GUIDELINE_YEARS * am[system] / P.K)


def validation_rows():
    """Equation (1) evaluated for the five validation CubeSats (inputs as published)."""
    rows = []
    for r in TABLE2_REVISED:
        pred = float(deorbit_time(r["alt"], r["am"], P))
        ratio = pred / r["actual"] if r["actual"] else None
        rows.append(dict(r, model=pred, ratio=ratio))
    return rows


def write_val_table(rows):
    lines = [r"\begin{table}[H]", r"\centering",
             r"\caption{Validation set: observed lifetimes versus Equation~(\ref{eq:decay}). "
             r"GRBAlpha: launched March 2021, re-entered June 2025. DhabiSat: re-entered January 2024. "
             r"PERSEUS-M1: launched June 2014, still in orbit. Predictions are computed from the equation.}",
             r"\label{tab:val}", r"\small",
             r"\begin{tabular}{lccccrr}", r"\toprule",
             r"CubeSat & Altitude & Mass & $A/m$ & Observed & Eq.~(\ref{eq:decay}) & Ratio \\",
             r" & (km) & (kg) & (m$^2$/kg) & lifetime (yr) & (yr) & (model/obs.) \\", r"\midrule"]
    for r in rows:
        obs = f"{r['actual']:.1f}" if r["actual"] else "12+ (in orbit)"
        ratio = f"{r['ratio']:.0f}$\\times$" if r["ratio"] else "consistent"
        lines.append(f"{r['name']} & $\\sim${r['alt']} & {r['mass']:g} & {r['am']:.3f} & "
                     f"{obs} & {r['model']:.1f} & {ratio} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (OUT / "table_val.tex").write_text("\n".join(lines) + "\n")


def fig_validation(rows):
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    lim = np.array([0.8, 400])
    ax.plot(lim, lim, "k-", lw=1.2, label="Perfect agreement")
    ax.plot(lim, lim * 10, ls=":", lw=1, color="gray")
    ax.plot(lim, lim / 10, ls=":", lw=1, color="gray", label=r"$\pm$10$\times$")
    for r in rows:
        if r["actual"]:
            ax.scatter(r["actual"], r["model"], s=55, color="#1f2fb0", zorder=3)
            ax.annotate(r["name"], (r["actual"], r["model"]), xytext=(6, 5),
                        textcoords="offset points", fontsize=8)
    ops = [r for r in rows if not r["actual"]]
    for r in ops:
        ax.annotate("", xy=(40, r["model"]), xytext=(12, r["model"]),
                    arrowprops=dict(arrowstyle="-|>", color="#f0a30a", lw=1.8))
        ax.scatter(12, r["model"], s=55, color="#f0a30a", marker="D", zorder=3)
        ax.annotate(r["name"], (12, r["model"]), xytext={"PERSEUS-M1": (-6, -13)}.get(r["name"], (-6, 7)), textcoords="offset points",
                    fontsize=8, ha="right")
    ax.scatter([], [], s=55, color="#1f2fb0", label="Decommissioned (observed decay)")
    ax.scatter([], [], s=55, color="#f0a30a", marker="D", label="Still in orbit (observed $\\geq$12 yr)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.8, 400); ax.set_ylim(0.8, 400)
    ax.set_xlabel("Observed lifetime (years)")
    ax.set_ylabel("Equation (1) prediction (years)")
    ax.grid(True, which="both", color="#e5e5e5", lw=0.6)
    ax.legend(loc="lower right", fontsize=7.5)
    fig.tight_layout()
    return fig


def derived():
    mean600 = np.mean([t3[s][2] for s in SYSTEMS])
    rows = validation_rows()
    by = {r['name']: r['model'] for r in rows}
    ratios = [r["ratio"] for r in rows if r["ratio"]]
    mape = np.mean([abs(r["model"] - r["actual"]) / r["actual"] * 100 for r in rows if r["actual"]])
    sens = sensitivity(DRAG_SAIL, 600.0, P)
    return dict(
        SailFour=t3[DRAG_SAIL][0], SailSix=t3[DRAG_SAIL][2], SailEight=t3[DRAG_SAIL][4],
        EDTSix=t3[EDT][2], PropSix=t3[PROPULSION][2],
        EDTover=round(100 * (t3[EDT][2] / GUIDELINE_YEARS - 1)),
        PROPover=round(100 * (t3[PROPULSION][2] / GUIDELINE_YEARS - 1)),
        MeanSix=round(mean600, 1),
        EDTcross=int(5 * round(threshold_altitude(EDT) / 5)),
        PROPcross=int(5 * round(threshold_altitude(PROPULSION) / 5)),
        KsensSail=round(0.15 * t3[DRAG_SAIL][2], 1),
        KsensEDT=round(0.15 * t3[EDT][2], 1),
        KsensProp=round(0.15 * t3[PROPULSION][2]),
        ValLo=int(round(min(ratios))), ValHi=int(round(max(ratios))),
        ValMAPE=int(round(mape, -2)),
        ValEstFour=round(by["ESTCube-1"]), ValAauThree=round(by["AAUSat-3"]), ValPerseus=round(by["PERSEUS-M1"]),
        ValModelGRB=round(by["GRBAlpha"], 1), ValModelDhabi=round(by["DhabiSat"], 1),
        ValModelEst=round(by["ESTCube-1"], 1), ValModelAau=round(by["AAUSat-3"], 1), ValModelPerseus=round(by["PERSEUS-M1"], 1),
        DensLo=round(sens["density_range"][0], 1),
        DensHi=round(sens["density_range"][1], 1),
    )


def write_numbers(d):
    lines = ["% Auto-generated by corrected.py - do not edit by hand."]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in d.items()]
    (OUT / "numbers.tex").write_text("\n".join(lines) + "\n")


def write_tables():
    rows1 = [("Base Satellite", None)] + [(s, s) for s in SYSTEMS]
    t1 = [r"\begin{table}[H]", r"\centering",
          r"\caption{Summary of parameters used for deorbit calculations (corrected: A/m = effective area / total mass).}",
          r"\label{tab:params}", r"\small",
          r"\begin{tabular}{lccccc}", r"\toprule",
          r"System & Dry mass & Propellant & Effective area & Total mass & Effective A/m \\",
          r" & (kg) & (kg) & (m$^2$) & (kg) & (m$^2$/kg) \\", r"\midrule"]
    for name, key in rows1:
        row = TABLE1[name]
        dry = "--" if row["dry"] is None else f"{row['dry']:.2f}"
        prop = "--" if row["prop"] is None else f"{row['prop']:.2f}"
        a = row["area"] / row["total"]
        t1.append(f"{name} & {dry} & {prop} & {row['area']:.2f} & {row['total']:.2f} & {a:.3g} \\\\")
    t1 += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]

    t3_lines = [r"\begin{table}[H]", r"\centering",
                r"\caption{Calculated deorbit times (years) from various initial altitudes.}",
                r"\label{tab:times}",
                r"\begin{tabular}{rrrr}", r"\toprule",
                r"Altitude (km) & Drag Sail & E.D.\ Tether & Propulsion \\", r"\midrule"]
    for i, h in enumerate(ALTITUDES_KM):
        t3_lines.append(f"{h} & {t3[DRAG_SAIL][i]:.1f} & {t3[EDT][i]:.1f} & {t3[PROPULSION][i]:.1f} \\\\")
    t3_lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (OUT / "table_params.tex").write_text("\n".join(t1) + "\n")
    (OUT / "table_times.tex").write_text("\n".join(t3_lines) + "\n")


def save(fig, name):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {FIG / name}.pdf/.png")


def main():
    d = derived()
    write_numbers(d)
    write_tables()
    rows = validation_rows()
    write_val_table(rows)
    save(fig_validation(rows), "fig_validation")
    save(figures.fig_deorbit_vs_altitude(t3), "fig_deorbit_vs_altitude")
    save(figures.fig_am_vs_time(t3, am), "fig_am_vs_time")
    save(figures.fig_performance_600km(t3), "fig_performance_600km")
    print("\nCorrected Table 3:")
    for i, h in enumerate(ALTITUDES_KM):
        print(f"  {h}: " + "  ".join(f"{t3[s][i]:>8.1f}" for s in SYSTEMS))
    print("\nDerived values:", d)


if __name__ == "__main__":
    main()
