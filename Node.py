import numpy as np

import TSPClasses


class Node:

    def __init__(self, unreducedMatrix, level, city, cities):
        """
        Creates a new node. Computes the reducedMatrix when is created.
        :param unreducedMatrix: unreduced matrix coming from parent with .copy()
        :param level: depth, used to know when we have found a route
        :param city: city that will be added to the pathVisited array
        :param cities: arrays of cities. Used for expanding the tree.
        """
        self.reducedMatrix = self.reduceMatrix(unreducedMatrix)  # 2D Array
        self.length: int = len(self.reducedMatrix)
        self.lowerBound: int = None
        self.level: int = level  # to know when to end
        self.pathVisited: list = []  # to know what path (new nodes to create) to follow

        # FIXME: fix the way that pathVisited is created. Needs to get a list from the parent, and then add the city


        self.addToPath(city)
        self.cities: list = cities

    def __lt__(self, other):
        return self.lowerBound < other.lowerBound

    def addToPath(self, city: TSPClasses.City):
        self.pathVisited.append(city)

    def reduceMatrix(self, unreducedMatrix):
        lowerBound = 0
        #  Reduce row
        for row in range(self.length):
            rowContainsZero = 0 in unreducedMatrix[row]
            if rowContainsZero:
                continue

            minNumberInRow = min(unreducedMatrix[row])
            lowerBound += minNumberInRow
            for col in range(self.length):
                unreducedMatrix[row][col] -= minNumberInRow

        # Reduce column
        for col in range(self.length):
            minNumberInCol = np.inf
            for row in range(self.length):
                if unreducedMatrix[row][col] < minNumberInCol:
                    minNumberInCol = unreducedMatrix[row][col]

            if minNumberInCol != 0:
                lowerBound += minNumberInCol
                for row in range(self.length):
                    unreducedMatrix[row][col] -= minNumberInCol

        self.lowerBound = lowerBound

    def expandTree(self):
        # TODO
        pass
