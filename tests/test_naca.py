import unittest
import foillib as fl


class test_naca_4(unittest.TestCase):

    def setUp(self):
        self.x, self.y = fl.naca("0012")

    # ensure that the maxium thickness of the NACA0012 is in fact 12% of chord.
    def test_max_thickness(self):
        max_thickness = abs(min(self.y)) + max(self.y)
        self.assertAlmostEqual(max_thickness, 0.12, 4)

    # ensure that the default airfoil has a non-zero trailing edge thickness
    def test_trailing_edge_thickness(self):
        self.assertGreater(self.y[0], 0)
        self.assertLess(self.y[-1], 0)


class test_naca_5(unittest.TestCase):

    def setUp(self):
        self.x, self.y = fl.naca("24012")

    # ensure that the default airfoil has a non-zero trailing edge thickness
    def test_trailing_edge_thickness(self):
        self.assertGreater(self.y[0], 0)
        self.assertLess(self.y[-1], 0)


if __name__ == "__main__":
    unittest.main()
