from unittest import TestCase
import heapq
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

    def testPQ(self):
        node1 = Node(None, 10, None, None)
        node2 = Node(None, 20, None, None)
        node3 = Node(None, 30, None, None)

        priorityQueue = []
        heapq.heappush(priorityQueue, node1)
        heapq.heappush(priorityQueue, node2)
        heapq.heappush(priorityQueue, node3)

        poppedNode = heapq.heappop(priorityQueue)
        self.assertEqual(node1, poppedNode, "Node 1 was not popped first.")

        poppedNode = heapq.heappop(priorityQueue)
        self.assertEqual(node2, poppedNode, "Node 2 was not popped second.")

        poppedNode = heapq.heappop(priorityQueue)
        self.assertEqual(node3, poppedNode, "Node 1 was not popped third.")



