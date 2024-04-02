import numpy as np
import copy


import TSPClasses


class Node:

    def __init__(self, unreducedMatrix, level, pathVisited, cityForNewPath, cities, costFromParent, parentLB):
        """
        Creates a new node. Computes the reducedMatrix when is created.
        :param unreducedMatrix: unreduced matrix coming from parent with .copy()
        :param level: depth, used to know when we have found a route
        :param pathVisited: the path from the parent
        :param cityForNewPath: city that will be added to the pathVisited array
        :param cities: arrays of cities. Used for expanding the tree.
        :param costFromParent: the cost of (i,j) from the parent matrix, used to calculate new LB
        :param parentLB: the parent LB, used to calculate new LB
        """
        self.lowerBound: int = None
        self.length: int = len(unreducedMatrix)
        self.reducedMatrix = self.reduceMatrix(unreducedMatrix, costFromParent, parentLB)  # 2D Array
        self.level: int = level  # to know when to end
        self.pathVisited: list = pathVisited  # to know what path (new nodes to create) to follow
        self.addToPath(cityForNewPath)
        self.cities: list = cities

    def __lt__(self, other):
        return self.lowerBound < other.lowerBound

    def addToPath(self, city: TSPClasses.City):
        self.pathVisited.append(city)

    def reduceMatrix(self, unreducedMatrix, costFromParent, parentLB):
        lowerBound = 0
        #  Reduce row
        for row in range(self.length):
            rowContainsZero = 0 in unreducedMatrix[row]
            if rowContainsZero:
                continue

            minNumberInRow = min(unreducedMatrix[row])

            if minNumberInRow != np.inf:
                lowerBound += minNumberInRow
                for col in range(self.length):
                    unreducedMatrix[row][col] -= minNumberInRow

        # Reduce column
        for col in range(self.length):
            minNumberInCol = np.inf
            for row in range(self.length):
                if unreducedMatrix[row][col] < minNumberInCol:
                    minNumberInCol = unreducedMatrix[row][col]

            if minNumberInCol != 0 and minNumberInCol != np.inf:
                lowerBound += minNumberInCol
                for row in range(self.length):
                    if unreducedMatrix[row][col] != np.inf:
                        unreducedMatrix[row][col] -= minNumberInCol

        self.lowerBound = lowerBound + costFromParent + parentLB
        return unreducedMatrix

    def expandTree(self):
        children = []
        for city in self.cities:
            if city not in self.pathVisited:
                # Create a new node
                parentCity = self.pathVisited[-1]
                parentIndex = self.cities.index(parentCity)
                childIndex = self.cities.index(city)
                parentMatrixCopy = copy.deepcopy(self.reducedMatrix)
                matrixWithInfinities = self.makeRowAndColumnInfinite(parentMatrixCopy, parentIndex, childIndex)

                pathVisitedCopy = copy.deepcopy(self.pathVisited)
                tempNode = Node(matrixWithInfinities, self.level+1, pathVisitedCopy, city, self.cities,
                                self.reducedMatrix[parentIndex][childIndex], self.lowerBound)
                children.append(tempNode)


        return children

    def makeRowAndColumnInfinite(self, parentMatrix, row, column):
        """
        Sets the rows and columns and position (column, row) to infinity in the parentMatrix
        :param parentMatrix:
        :param row
        :param column
        :return:
        """
        for i in range(len(parentMatrix)):
            parentMatrix[row][i] = np.inf
            parentMatrix[i][column] = np.inf

        parentMatrix[column][row] = np.inf
        return parentMatrix

