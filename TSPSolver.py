#!/usr/bin/python3
import heapq
from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
from TSPClasses import *
from Node import *
import heapq
import itertools


class TSPSolver:
    def __init__(self, gui_view):
        self.scenario = None

    def setupWithScenario(self, scenario):
        self.scenario = scenario

    ''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self.scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''
    def greedy(self, time_allowance = 60.0):
        results = {}
        cities = self.scenario.getCities()
        numberCities = len(cities)
        foundTour = False  # There is a path from a start city to that same start city (tour)
        bssf = None
        start_time = time.time()

        startCityIndex = 0
        allCitiesHaveBeenAStart = startCityIndex == numberCities  # Used to check if I should keep traversing cities

        while not foundTour and time.time() - start_time < time_allowance:
            if not allCitiesHaveBeenAStart:
                bssf, foundTour = self.findTourGreedy(cities[startCityIndex], cities, numberCities)
                self.setCitiesToUnvisited(cities)
                if foundTour:
                    break
                else:
                    startCityIndex += 1
                    allCitiesHaveBeenAStart = startCityIndex == numberCities

            else:  # Every city was a start point and no route was found
                break  # ... out of the loop and finish

        end_time = time.time()

        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = 1 if foundTour else 0
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None

        return results

    def findTourGreedy(self, startCity, cities, numberCities):
        """
        Used by greedy algorithm.
        Tries to traverse through all the cities, starting and ending in the startCity.
        :param startCity: the city that will be origin and the end
        :param cities: all the cities to visit
        :param numberCities: total number of cities, 1 based.
        :return:    bssf -> TSPSolution, includes the route and the cost using ._costOfRoute()
                    thereIsTour: bool, true if there is a route, false otherwise
        """
        thereIsTour = False
        route = [startCity]
        currentCity = startCity
        currentCity.setVisited(True)

        for i in range(numberCities-1):
            nextCity = self.findShortestPathFrom(currentCity, cities, numberCities)
            if nextCity is None:
                return None, thereIsTour
            currentCity = nextCity
            currentCity.setVisited(True)
            route.append(currentCity)

        # After going through every city, and getting to the last one, check if that last one can go back to start city
        if currentCity.costTo(startCity) != np.inf:
            thereIsTour = True
        else:  # the last city in route[] does not go connect to startCity, therefore there is no route
            return None, thereIsTour

        bssf = TSPSolution(route)

        return bssf, thereIsTour

    def setCitiesToUnvisited(self, cities):
        """
        Set all the cities in an array to unvisited.
        """
        for city in cities:
            city.setVisited(False)



    def findShortestPathFrom(self, originCity, cities, numberCities):
        """
        Goes through each edge coming from originCity and returns the city with the minimum cost edge.
        :param numberCities: cities length
        :param cities: array of cities
        :param originCity: city where the edge will be going to another city.
        :return: the city with the lowest edge cost
        """
        lowestCity = None  # Update as I go through each city
        lowestCost = np.inf

        for i in range(numberCities):
            destinationCity = cities[i]
            if destinationCity.hasBeenVisited():
                continue
            costToDestinationCity = originCity.costTo(destinationCity)
            if costToDestinationCity < lowestCost:
                lowestCost = costToDestinationCity
                lowestCity = destinationCity

        return lowestCity

    ''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''
    def branchAndBound(self, time_allowance = 60.0):
        Node.resetCount()
        results = {}
        cities = self.scenario.getCities()
        numberCities = len(cities)
        bssf = None
        start_time = time.time()
        maxPriorityQueueSize = 0
        # childrenCount = 0
        prunedCount = 0
        solutionsCount = 0
        bssfToTestPathToOrigin = None

        #  Creating the first matrix
        rootMatrix = self.convertCitiesIntoStartMatrix(cities, numberCities)

        #  Creating first node and pushing it into the PQ
        root = Node(rootMatrix.copy(), 0, [], cities[0], cities, 0, 0)
        priorityQueue = []
        heapq.heappush(priorityQueue, root)

        #  Initializing bssf from greedy algorithm
        greedyResults = self.greedy()
        bssf = greedyResults['soln']

        while priorityQueue and time.time() - start_time < time_allowance:
            # print("{:.1f}".format(time.time() - start_time))
            maxPriorityQueueSize = max(len(priorityQueue), maxPriorityQueueSize)
            poppedNode = heapq.heappop(priorityQueue)
            if poppedNode.lowerBound < bssf.cost:
                children = poppedNode.expandTree()
                for node in children:
                    print(bssf.cost)
                    test = node.test()
                    if test != np.inf:
                        bssfToTestPathToOrigin = TSPSolution(node.pathVisited)
                        if bssfToTestPathToOrigin.cost < bssf.cost:
                            solutionsCount += 1
                            bssf = bssfToTestPathToOrigin
                    elif node.lowerBound < bssf.cost:
                        heapq.heappush(priorityQueue, node)
                    else:
                        prunedCount += 1
            else:
                prunedCount += 1

        end_time = time.time()
        print(bssf.cost)
        results['cost'] = bssf.cost
        results['time'] = end_time - start_time
        results['count'] = solutionsCount
        results['soln'] = bssf
        results['max'] = maxPriorityQueueSize
        results['total'] = Node.nodesCreated
        results['pruned'] = prunedCount
        return results


    def convertCitiesIntoStartMatrix(self, cities, length):
        """
        Creates a 2d array or matrix from the data of a list cities
        :param cities: source data
        :param length: number of rows or columns the matrix will have
        :return: the created matrix (it has not been reduced yet)
        """
        # Initialize matrix with inf
        matrix = [[np.inf for _ in range(length)] for _ in range(length)]

        # Populate, go through each cell in the matrix
        for row in range(length):
            originCity = cities[row]
            for col in range(length):
                destinationCity = cities[col]
                # Distance from row to col
                matrix[row][col] = originCity.costTo(destinationCity)

        return matrix

