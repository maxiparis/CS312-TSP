import numpy as np
import copy


import TSPClasses


class Node:
    nodesCreated = 0

    def __init__(self, unreducedMatrix, level, pathVisited, cityForNewPath, cities, costFromParent, parentLB):
        """
        Creates a new node. Computes the reducedMatrix and lowerBound when is created.

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
        self.incrementCount()

    @classmethod
    def incrementCount(cls):
        """
        Increments the nodesCreated everytime a new node is created.
        """
        cls.nodesCreated += 1

    @classmethod
    def resetCount(cls):
        """
        Resets the count for created nodes.
        """
        cls.nodesCreated = 0

    def __lt__(self, other):
        # it needs to consider the lower bound and the depth (level)
        return self.lowerBound / self.level < other.lowerBound / other.level

    def addToPath(self, city: TSPClasses.City):
        """
        Adds a new city to the path visited.
        :param city: to be added to the path
        """
        self.pathVisited.append(city)

    def reduceMatrix(self, unreducedMatrix, costFromParent, parentLB):
        """
        Reduces a matrix. Updates the node lower bound.
        :param unreducedMatrix: matrix to be reduced
        :param costFromParent: cost of going from the previous city (node) to this city.
        :param parentLB: parent's lowerBound
        """
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
        """
        Creates a new child node for every city that has not been visited by this state yet.
        :return: The children of the current node.
        """
        children = []
        for city in self.cities:
            if city not in self.pathVisited:
                parentCity = self.pathVisited[-1]
                parentIndex = self.cities.index(parentCity)
                childIndex = self.cities.index(city)
                parentMatrixCopy = copy.deepcopy(self.reducedMatrix)
                matrixWithInfinities = self.makeRowAndColumnInfinite(parentMatrixCopy, parentIndex, childIndex)

                pathVisitedCopy = copy.copy(self.pathVisited)
                # Create a new node
                tempNode = Node(matrixWithInfinities, self.level+1, pathVisitedCopy, city, self.cities,
                                self.reducedMatrix[parentIndex][childIndex], self.lowerBound)
                children.append(tempNode)


        return children

    def makeRowAndColumnInfinite(self, parentMatrix, row, column):
        """
        Sets the rows and columns and position (column, row) to infinity in the parentMatrix
        :param parentMatrix matrix where cells will be updated
        :param row to be set to infinity
        :param column to be set to infinity
        :return: the matrix with updated rows and columns
        """
        for i in range(len(parentMatrix)):
            parentMatrix[row][i] = np.inf
            parentMatrix[i][column] = np.inf

        parentMatrix[column][row] = np.inf
        return parentMatrix

    def test(self) -> int:
        """
        Tests if the pathVisited is complete (go from the first element to the end)
        :return: LB if the path is complete, infinity otherwise
        """
        if self.level == self.length - 1 and self.thereIsPathToOrigin():
            return self.lowerBound
        else:
            return np.inf

    def thereIsPathToOrigin(self):
        indexOrigin = 0
        lastCity = self.pathVisited[-1]
        lastCityIndex = self.cities.index(lastCity)
        return self.reducedMatrix[lastCityIndex][indexOrigin] != np.inf