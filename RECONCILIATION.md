# Reconciliation notes (`python consistency.py` regenerates all of this)

Rebuilding the model from the paper showed several places where the published
numbers do not agree with each other. They are listed here so they can be
resolved against the original spreadsheet.

## 1. Equation constants (Section 1.2) vs. Table 3

The paper prints H = 50 km and K = 2.5×10⁻⁵ yr·kg/m². With those constants the
equation gives, at 600 km, 8.7 yr (drag sail), 183 yr (EDT), 705 yr (propulsion)
versus 2.2, 43.5 and 179.5 yr in Table 3.

Table 3 grows by about ×e per 100 km, i.e. H ≈ 100 km. It is reproduced to within
a few percent by **H = 100 km and K = 2.5×10⁻³**, which is what `model.CALIBRATED` uses.

## 2. Table 1 effective A/m

| System | A/m printed | area ÷ total mass |
|---|---|---|
| Drag sail | 0.468 | 0.465 |
| EDT | 0.024 | 0.0222 |
| Propulsion | 0.0058 | 0.0058 |

Table 3's drag-sail row matches 2.00/4.30 = 0.465. The EDT and propulsion rows imply
A/m ≈ 0.0232 and ≈ 0.00562, so those two rows are reproduced only to ~3–6%.

## 3. Table 2 "Predicted Lifetime" column

The predicted lifetimes cannot be reproduced by Equation (1) with either set of
constants (e.g. GRB Alpha, 535 km, A/m 0.010: equation gives ≈ 53 yr with the
Table-3 constants, the table says 2.2 yr). The error percentages and the 10.5 %
mean absolute error are internally consistent with the printed predicted/actual
values, but those predicted values do not come from the equation as written.
Source of the predicted column needs to be confirmed.

## 4. Sensitivity analysis (Section 1.3)

- ±50 % density → 3.0× spread between extremes for the drag sail (consistent with "factor of 2–3").
- ±10 % A/m → −9.1 % / +11.1 % (consistent with "8–12 %").
- ±15 % K at 600 km → ±0.33 yr (drag sail), ±6.5 yr (EDT), ±27 yr (propulsion).
  The text's "±0.3 to 2 years" only matches the drag sail.

## 5. Figure captions

On pages 23–24 the two images carry each other's captions: the residual histogram
sits under "Figure 1" and the altitude plot under "Figure 2", while the text refers
to the residuals as Figure 1 and the altitude plot as Figure 2. The residual sign
convention also differs between text (actual − predicted) and plot (predicted − actual).

## Status of the corrected draft (`corrected/`)

Items 1, 2 and 4 are corrected there. Item 3 (Table 2) is resolved by recomputing the predictions from
Equation (1): the model overestimates the two decayed satellites by a factor of ~7–13, so the
"10.5 % validation" claim is withdrawn and the model is presented as a relative-comparison tool. Item 5
(caption swap) is fixed. The revised manuscript includes a reconciled reference list.

## Validation data correction (second review)

An external check of the satellite records found the published Table 2 inputs wrong: GRBAlpha
re-entered June 2025 after ~4.2 yr (published: 2.0); DhabiSat re-entered January 2024 after ~2.6 yr
(published: 1.4; corrected from deployment-to-reentry dates); PERSEUS-M1 launched in 2014 into ~620 km and is still in
orbit (published: 475 km, decayed after 3.2 yr). `data.TABLE2_REVISED` holds the revised set used by
`corrected.py`. Mass and A/m of the validation satellites are carried over from the published table and have
not been independently checked. The units of K are year*m^2/kg.
