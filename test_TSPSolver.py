from unittest import TestCase
import numpy as np
from TSPSolver import *


class TestTSPSolver(TestCase):
    def setUp(self):
        self.solver = TSPSolver(None)

    def test_reduce_matrix(self):
        self.fail()

    def testReduceMatrix(self):
        matrix = [[np.inf, 7, 3, 12],
                  [3, np.inf, 6, 14],
                  [5, 8, np.inf, 6],
                  [9, 3, 5, np.inf]]

        result = self.solver.reduceMatrix(matrix, 4)
        self.assertEqual(15, result, "the LB are not the same.")

        matrix = [[np.inf, 385, 1801, 371],
                  [np.inf, np.inf, 1693, 639],
                  [2080, 1533, np.inf, 2131],
                  [373, np.inf, 1855, np.inf]]

        result = self.solver.reduceMatrix(matrix, 4)
        self.assertEqual(3970, result, "the LB are not the same.")