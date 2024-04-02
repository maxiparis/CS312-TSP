from unittest import TestCase

from Node import Node
from TSPClasses import City
from TSPSolver import *


class TestNode(TestCase):
    def setUp(self):
        self.solver = TSPSolver(None)
    def test_add_to_path(self):
        city1 = City(0.2523423, 0.323234)
        city2 = City(0.7776675, 0.4434)
        city3 = City(0.2523423, 0.131545)
        city4 = City(0.123123, 0.65656)
        city5 = City(0.3344432, 0.434233)

        cities = [city1, city2, city3, city4, city5]

        startMatrix = self.solver.convertCitiesIntoStartMatrix(cities, len(cities))
        startNode = Node(startMatrix, 0, [], cities[0], cities)

        self.assertTrue(len(startNode.pathVisited) == 1)


