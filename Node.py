class Node:
    def __init__(self, matrix, lowerBound, level, pathVisited):
        self.reducedMatrix = matrix
        self.lowerBound = lowerBound
        #  self.currentCityNumber = None
        self.level = level
        self.pathVisited = pathVisited


    def __lt__(self, other):
        return self.lowerBound < other.lowerBound

