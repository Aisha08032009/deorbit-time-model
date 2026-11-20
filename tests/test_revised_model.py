import math
import unittest

from data import SYSTEMS, ALTITUDES_KM, DRAG_SAIL, EDT, PROPULSION, TABLE2_REVISED
from model import CALIBRATED, am_from_table1, deorbit_time
from corrected import derived, validation_rows

class ReproducibilityTests(unittest.TestCase):
    def test_model_at_600km(self):
        target = {DRAG_SAIL: 2.2, EDT: 45.4, PROPULSION: 174.8}
        for s, expected in target.items():
            self.assertAlmostEqual(round(float(deorbit_time(600, am_from_table1(s), CALIBRATED)), 1), expected, places=1)

    def test_full_table3(self):
        expected = {
            DRAG_SAIL: [0.3, 0.8, 2.2, 5.9, 16.0],
            EDT: [6.1, 16.7, 45.4, 123.4, 335.4],
            PROPULSION: [23.7, 64.3, 174.8, 475.2, 1291.7],
        }
        for s in SYSTEMS:
            self.assertEqual([round(float(deorbit_time(h, am_from_table1(s), CALIBRATED)), 1) for h in ALTITUDES_KM], expected[s])

    def test_validation_recomputed(self):
        rows = {r['name']: r for r in validation_rows()}
        for n, model, observed in [('GRBAlpha',52.7,4.2), ('DhabiSat',17.9,2.6), ('PERSEUS-M1',176.0,None)]:
            self.assertAlmostEqual(rows[n]['model'], model, delta=.1)
            self.assertEqual(rows[n]['actual'], observed)

    def test_derived_values(self):
        d=derived()
        self.assertEqual((d['EDTover'],d['PROPover'],d['ValLo'],d['ValHi']), (82,599,7,13))

    def test_valid_model_units(self):
        self.assertAlmostEqual(CALIBRATED.H,100.0)
        self.assertAlmostEqual(CALIBRATED.K,0.0025)
        self.assertTrue(math.isfinite(float(deorbit_time(600,am_from_table1(DRAG_SAIL),CALIBRATED))))
