from unittest import TestCase

from dtw import dtw

_d = lambda x, y: abs(x - y)


class DtwTest(TestCase):
    def test_null(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        self.assertEqual(dtw(x, y, _d), 0)

    def test_bias(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 4, 5, 6]
        self.assertEqual(dtw(x, y, _d), 2)

    def test_distance(self):
        x = [0, 0, 1, 1, 2, 4, 2, 1, 2, 0]
        y = [1, 1, 1, 2, 2, 2, 2, 3, 2, 0]
        self.assertEqual(dtw(x, y, _d), 4)

    def test_symmetry(self):
        x = [0, 0, 1, 1, 2, 4, 2, 1, 2, 0]
        y = [1, 1, 1, 2, 2, 2, 2, 3, 2, 0]
        self.assertEqual(dtw(x, y, _d), dtw(y, x, _d))
