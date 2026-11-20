"""
Figures from the paper, redrawn from the published values in data.py.

Note on numbering: in the PDF the two images on pages 23-24 sit under captions
that are swapped relative to their content (the residual histogram carries the
caption "Figure 1" and the altitude plot "Figure 2"). Files here are named by
content to avoid ambiguity.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

from data import (ALTITUDES_KM, TABLE1, TABLE3, SYSTEMS, DRAG_SAIL, EDT, PROPULSION,
                  GUIDELINE_YEARS, RESIDUALS_YEARS)
from model import CALIBRATED

OUT = Path("figures")
BLUE, ORANGE, GREEN, RED = "#1f2fb0", "#f0a30a", "#1a7a1a", "#c0392b"
STYLE = {
    DRAG_SAIL:  dict(color=BLUE,   ls="-",  marker="o", label="Drag Sail"),
    EDT:        dict(color=ORANGE, ls="--", marker="s", label="Electrodynamic Tether"),
    PROPULSION: dict(color=GREEN,  ls=":",  marker="^", label="Propulsion System"),
}


# ------------------------------------------------------------------ altitude plot
def fig_deorbit_vs_altitude(t3=TABLE3):
    fig, ax = plt.subplots(figsize=(9, 6.2))
    ax.set_facecolor("#eef0f8")
    for s in SYSTEMS:
        ax.semilogy(ALTITUDES_KM, t3[s], lw=1.8, ms=6, **STYLE[s])
    ax.axhline(GUIDELINE_YEARS, color="#b22222", ls="--", lw=1.5)
    ax.text(402, GUIDELINE_YEARS * 1.12, "25-Year Guideline", color="#b22222", fontsize=8)

    for s, c in [(DRAG_SAIL, BLUE), (EDT, ORANGE), (PROPULSION, GREEN)]:
        y = t3[s][2]
        ax.annotate(f"{y:g} years", (600, y), xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=8, color=c)
    ax.annotate("Approaches 25-Year Limit", (800, t3[DRAG_SAIL][4]),
                xytext=(745, 40), fontsize=8, color=BLUE, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))

    ax.set_xlabel("Initial Altitude (km)")
    ax.set_ylabel("Deorbit Time (years)")
    ax.set_title("Calculated Deorbit Time vs. Initial Altitude\nfor Different CubeSat Deorbit Technologies",
                 fontsize=11)
    ax.grid(True, which="major", color="white", lw=1)
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlim(390, 810)
    ax.set_ylim(0.2, 3000)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ residual histogram
def fig_residuals():
    r = np.array(RESIDUALS_YEARS)
    mu, sd = r.mean(), r.std()                    # population SD, matches the printed curve
    fig, ax = plt.subplots(figsize=(7.5, 6))
    ax.hist(r, bins=[-0.15, 0.175, 0.5], color="#5a7bef", edgecolor="black", lw=1.2)
    x = np.linspace(-0.5, 0.5, 400)
    pdf = np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
    ax.plot(x, pdf, color="#d62728", lw=2, label="Normal Distribution")
    ax.axvline(0, color="gray", ls="--", lw=1)
    for v in r:
        ax.text(v, 0.08, f"{v:+.2f}", ha="center", fontsize=8,
                bbox=dict(fc="white", ec="none", pad=1.5))
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(0, 2.1)
    ax.set_xlabel("Prediction Error (years)")
    ax.set_ylabel("Frequency")
    ax.set_title("Residual Distribution of Model Predictions", fontsize=11)
    ax.text(0.02, 0.98, "Mean Absolute Error = 10.5%\nValidation against 3 CubeSats",
            transform=ax.transAxes, ha="left", va="top", fontsize=8)
    ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(0.0, 0.90))
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ A/m vs deorbit time
def fig_am_vs_time(t3=TABLE3, am_map=None):
    am_map = am_map or {s: TABLE1[s]["am"] for s in SYSTEMS}
    fig, ax = plt.subplots(figsize=(9, 6))
    pts = [(DRAG_SAIL, "#1111dd"), (EDT, "#f0a30a"), (PROPULSION, "#d62728")]
    k = CALIBRATED.K * np.exp(600 / CALIBRATED.H)         # y = k / x trend
    xs = np.linspace(0.004, 0.5, 400)
    ax.semilogy(xs, k / xs, "k--", lw=1.4, label="Inverse Trend: y = k/x")
    for s, c in pts:
        am, t = am_map[s], t3[s][2]
        ax.scatter([am], [t], s=60, color=c, zorder=3,
                   label=f"{s} ({am:.3g} m²/kg, {t:g} yrs)")
    ax.set_xlim(0, 0.5)
    ax.set_ylim(1, 1000)
    ax.set_xlabel("Effective Area-to-Mass Ratio (m²/kg)")
    ax.set_ylabel("Deorbit Time at 600 km (years)")
    ax.set_title("Area-to-Mass Ratio vs Deorbit Time", fontsize=11)
    ax.grid(True, which="both", color="#dddddd", lw=0.6)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ 600 km bar chart
def fig_performance_600km(t3=TABLE3):
    vals = [t3[s][2] for s in SYSTEMS]
    names = ["Drag Sail", "Electrodynamic Tether", "Propulsion System"]
    colors = ["#4a86c0", "#ff8210", "#e3123b"]
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(names, vals, color=colors, edgecolor=["#2d5a7a", "#b35c0a", "#a00d29"], lw=1.5,
                  width=0.6)
    bars[0].set_linestyle((0, (2, 1)))
    bars[0].set_edgecolor("#2e7d32")
    ax.set_yscale("log")
    ticks = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    ax.yaxis.set_major_locator(FixedLocator(ticks))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}" if v < 1000 else "1k"))
    ax.set_ylim(1, 1000)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.12, f"{v:g}", ha="center",
                fontsize=11, fontweight="bold")
    ax.axhline(GUIDELINE_YEARS, color="#c2185b", ls="--", lw=1.6)
    ax.text(2.45, GUIDELINE_YEARS * 1.1, "25-year guideline", ha="right", fontsize=8,
            color="#c2185b", bbox=dict(boxstyle="round", fc="white", ec="#c2185b"))
    comp = sum(v < GUIDELINE_YEARS for v in vals)
    ax.text(0.02, 0.97,
            "Compliance Status\n● Compliant (< 25 years)\n● Non-compliant (≥ 25 years)\n"
            f"Compliance rate: {100 * comp / len(vals):.0f}% ({comp}/{len(vals)})\n"
            f"Mean deorbit time: {np.mean(vals):.1f} years",
            transform=ax.transAxes, va="top", fontsize=8,
            bbox=dict(boxstyle="round", fc="white", ec="#bbbbbb"))
    ax.set_xlabel("Deorbit Technology", fontweight="bold")
    ax.set_ylabel("Deorbit Time at 600 km (years)", fontweight="bold")
    ax.set_title("Performance Comparison at Standard Altitude (600 km)", fontweight="bold", fontsize=11)
    ax.grid(axis="y", color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    return fig


def save_all(dpi: int = 250):
    OUT.mkdir(exist_ok=True)
    for name, fn in [("fig_deorbit_vs_altitude", fig_deorbit_vs_altitude),
                     ("fig_residuals", fig_residuals),
                     ("fig_am_vs_time", fig_am_vs_time),
                     ("fig_performance_600km", fig_performance_600km)]:
        fig = fn()
        fig.savefig(OUT / f"{name}.png", dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        print(f"saved {OUT / name}.png")


if __name__ == "__main__":
    save_all()
