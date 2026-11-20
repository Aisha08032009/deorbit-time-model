"""Regenerate the consistency report, CSV, and all corrected tables/figures (corrected/)."""
import csv

from consistency import main as consistency_report
from data import ALTITUDES_KM, TABLE3, SYSTEMS
from model import CALIBRATED, table3


def export_csv(path="deorbit_times.csv"):
    model = table3(CALIBRATED)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system", "altitude_km", "published_years (Table 3)",
                    f"model_years (K={CALIBRATED.K:g}, H={CALIBRATED.H:g})"])
        for s in SYSTEMS:
            for i, h in enumerate(ALTITUDES_KM):
                w.writerow([s, h, TABLE3[s][i], round(float(model[s][i]), 3)])
    print(f"saved {path}")


if __name__ == "__main__":
    consistency_report()
    print()
    export_csv()
    import corrected
    corrected.main()
