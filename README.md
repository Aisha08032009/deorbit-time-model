# CubeSat Deorbit-Time Model

**Aisha Shermatova** — Python implementation accompanying the corrected version of *Quantifying the Deorbit Time of CubeSats: A Comparative Analysis of Drag Sails, Propulsion, and Tethers* (original article: *Axiom Young Research*, Volume 2, 2026).

This repository regenerates the corrected paper’s numerical tables and four figures from a first-order **passive orbital decay comparison**. The original publication used spreadsheet calculations; this Python implementation documents the corrected equation, parameters, validation comparison, and results.

## Model and interpretation

For initial altitude `h` (km) and effective area-to-mass ratio `A/m` (m²/kg), the model is:

```text
T (years) = K × exp(h/H) / (A/m)
H = 100 km
K = 2.5e-3 year·m²/kg
```

The model compares drag sails, an electrodynamic tether **without active Lorentz braking**, and a propulsion system **without an active burn**. It does not predict real operational failure probabilities, deployment reliability, costs, or regulatory approval. It produces a consistent *relative ranking under the stated assumptions*. Because the simple model substantially overpredicts observed decay times, its absolute lifetimes are not suitable for mission compliance verification.

## Reproduce the corrected paper

Requires Python 3.10+ and LaTeX only if rebuilding the PDFs.

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m unittest discover -s tests -v
```

`run_all.py` recalculates `deorbit_times.csv`, `corrected/numbers.tex`, `corrected/table_*.tex` and the PDF/PNG figures in `corrected/figures/`. The consistency report explicitly compares the **original printed** tables and equation with the revised model; warnings about the original publication are expected.

To rebuild the manuscript PDF:

```bash
cd corrected
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

`corrected/main.tex` is the modular LaTeX version. `single/paper.tex` is a self-contained version. Both identify this repository at <https://github.com/Aisha08032009/deorbit-time-model>.

## Numerical results at 600 km (years)

| Drag sail | EDT (passive only) | Propulsion (no burn) |
|---:|---:|---:|
| 2.2 | 45.4 | 174.8 |

All 15 deorbit-time values from the revised Table 3 are recomputed by the model. The revised validation Table 2 uses observed decay lifetimes for GRBAlpha (~4.2 years) and DhabiSat (~2.6 years since spacecraft deployment), plus lower-bound lifetime comparisons for ESTCube-1, AAUSat-3, and PERSEUS-M1.

Validation status sources: [GRBAlpha (NASA)](https://heasarc.gsfc.nasa.gov/docs/heasarc/missions/grbalpha.html), [DhabiSat deployment and reentry](https://www.nanosats.eu/sat/mysat-2), [PERSEUS-M1 orbital status](https://celestrak.org/NORAD/elements/table.php?FORMAT=json&GROUP=active). The validation satellites' masses and assumed area-to-mass ratios were retained from the original paper rather than independently measured.

## Repository contents

- `model.py`, `data.py`: equation, inputs and sensitivity calculations
- `corrected.py`, `figures.py`, `run_all.py`: compute corrected tables and regenerate plots
- `consistency.py`, `RECONCILIATION.md`: differences from the originally published article
- `corrected/`: corrected manuscript source, compiled PDF, tables, figures, corrigendum draft
- `single/`: self-contained manuscript source and compiled PDF
- `tests/`: regression checks for the corrected model and output tables

For an editorial correction, use the **corrected manuscript** rather than the original publication's tables. The original paper remains the historical version of record until the journal accepts the correction.
