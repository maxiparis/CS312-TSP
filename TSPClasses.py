#!/usr/bin/python3


import math
import numpy as np
import random
import time


class TSPSolution:
    def __init__(self, listOfCities):
        self.route = listOfCities
        self.cost = self.costOfRoute()

    def costOfRoute(self):
        """
        Calculates the cost of the route this class holds.
        :return: the cost of the route
        """
        cost = 0
        last = self.route[0]
        for city in self.route[1:]:
            cost += last.costTo(city)
            last = city
        cost += self.route[-1].costTo(self.route[0])
        return cost

    def enumerateEdges(self):
        elist = []
        c1 = self.route[0]
        for c2 in self.route[1:]:
            dist = c1.costTo(c2)
            if dist == np.inf:
                return None
            elist.append((c1, c2, int(math.ceil(dist))))
            c1 = c2
        dist = self.route[-1].costTo(self.route[0])
        if dist == np.inf:
            return None
        elist.append((self.route[-1], self.route[0], int(math.ceil(dist))))
        return elist


def nameForInt(num):
    if num == 0:
        return ''
    elif num <= 26:
        return chr(ord('A') + num - 1)
    else:
        return nameForInt((num - 1) // 26) + nameForInt((num - 1) % 26 + 1)


class Scenario:
    HARD_MODE_FRACTION_TO_REMOVE = 0.20  # Remove 20% of the edges

    def __init__(self, city_locations, difficulty, rand_seed):
        self.difficulty = difficulty

        if difficulty == "Normal" or difficulty == "Hard":
            self.cities = [City(pt.x(), pt.y(), \
                                 random.uniform(0.0, 1.0) \
                                 ) for pt in city_locations]
        elif difficulty == "Hard (Deterministic)":
            random.seed(rand_seed)
            self.cities = [City(pt.x(), pt.y(), \
                                 random.uniform(0.0, 1.0) \
                                 ) for pt in city_locations]
        else:
            self.cities = [City(pt.x(), pt.y()) for pt in city_locations]

        num = 0
        for city in self.cities:
            city.setScenario(self)
            city.setIndexAndName(num, nameForInt(num + 1))
            num += 1

        # Assume all edges exists except self-edges
        ncities = len(self.cities)
        self.edge_exists = (np.ones((ncities, ncities)) - np.diag(np.ones(ncities))) > 0

        if difficulty == "Hard":
            self.thinEdges()
        elif difficulty == "Hard (Deterministic)":
            self.thinEdges(deterministic=True)

    def getCities(self):
        return self.cities

    def randperm(self, n):
        perm = np.arange(n)
        for i in range(n):
            randind = random.randint(i, n - 1)
            save = perm[i]
            perm[i] = perm[randind]
            perm[randind] = save
        return perm

    def thinEdges(self, deterministic=False):
        ncities = len(self.cities)
        edge_count = ncities * (ncities - 1)  # can't have self-edge
        num_to_remove = np.floor(self.HARD_MODE_FRACTION_TO_REMOVE * edge_count)

        can_delete = self.edge_exists.copy()

        # Set aside a route to ensure at least one tour exists
        route_keep = np.random.permutation(ncities)
        if deterministic:
            route_keep = self.randperm(ncities)
        for i in range(ncities):
            can_delete[route_keep[i], route_keep[(i + 1) % ncities]] = False

        # Now remove edges until
        while num_to_remove > 0:
            if deterministic:
                src = random.randint(0, ncities - 1)
                dst = random.randint(0, ncities - 1)
            else:
                src = np.random.randint(ncities)
                dst = np.random.randint(ncities)
            if self.edge_exists[src, dst] and can_delete[src, dst]:
                self.edge_exists[src, dst] = False
                num_to_remove -= 1


class City:
    def __init__(self, x, y, elevation=0.0):
        self.x = x
        self.y = y
        self.elevation = elevation
        self.scenario = None
        self.index = -1
        self.name = None
        self.visited = False

    def setVisited(self, visited: bool):
        self.visited = visited

    def hasBeenVisited(self):
        return self.visited

    def setIndexAndName(self, index, name):
        self.index = index
        self.name = name

    def setScenario(self, scenario):
        self.scenario = scenario

    ''' <summary>
		How much does it cost to get from this city to the destination?
		Note that this is an asymmetric cost function.
		 
		In advanced mode, it returns infinity when there is no connection.
		</summary> '''
    MAP_SCALE = 1000.0

    def costTo(self, other_city):

        assert (type(other_city) == City)

        # In hard mode, remove edges; this slows down the calculation...
        # Use this in all difficulties, it ensures INF for self-edge

        # If there is no edge between cities with index self._index to other_city._index
        if not self.scenario.edge_exists[self.index, other_city.index]:
            return np.inf

        # Euclidean Distance
        cost = math.sqrt((other_city.x - self.x) ** 2 +
                         (other_city.y - self.y) ** 2)

        # For Medium and Hard modes, add in an asymmetric cost (in easy mode it is zero).
        if not self.scenario.difficulty == 'Easy':
            cost += (other_city.elevation - self.elevation)
            if cost < 0.0:
                cost = 0.0

        return int(math.ceil(cost * self.MAP_SCALE))

    def __str__(self):
        return f"City({self.name}): Elevation: {self.elevation}, Index: {self.index}, Coordinates: ({self.x}, {self.y}), Visited: {self.visited}"

    def __repr__(self):
        return f"City({self.name}): Elevation: {self.elevation}, Index: {self.index}, Coordinates: ({self.x}, {self.y}), Visited: {self.visited}"


    def __eq__(self, other):
        if isinstance(other, City):
            return self.name == other.name
        return False


