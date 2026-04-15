from random import shuffle, randrange
from copy import copy, deepcopy
from CVRP_Problem_Instance import CVRP_Problem_Instance


class CVRP_Solution:
    def __init__(self, initType="random"):
        self.__reset()

        if isinstance(initType, list):
            self.__constructByPermutation(initType)
        elif initType == "ordered":
            self.__constructOrdered()
        else:
            self.__constructRandom()

        self._evaluate()

    def __reset(self):
        self.__perm = []
        self.__routes = []
        self.__fitness = float("inf")

    def __constructByPermutation(self, perm):
        self.__perm = copy(perm)

    def __constructOrdered(self):
        self.__perm = CVRP_Problem_Instance.getCustomerList()

    def __constructRandom(self):
        self.__perm = CVRP_Problem_Instance.getCustomerList()
        shuffle(self.__perm)

    def _decodeRoutes(self):
        depot = CVRP_Problem_Instance.getDepot()
        capacity = CVRP_Problem_Instance.getCapacity()

        routes = []
        current_route = [depot]
        current_load = 0

        for customer in self.__perm:
            demand = CVRP_Problem_Instance.getDemand(customer)

            if current_load + demand <= capacity:
                current_route.append(customer)
                current_load += demand
            else:
                current_route.append(depot)
                routes.append(current_route)

                current_route = [depot, customer]
                current_load = demand

        current_route.append(depot)
        routes.append(current_route)

        return routes

    def _evaluate(self):
        self.__routes = self._decodeRoutes()
        total_distance = 0

        for route in self.__routes:
            for i in range(len(route) - 1):
                total_distance += CVRP_Problem_Instance.getDistance(route[i], route[i + 1])

        self.__fitness = total_distance

    def getPermutation(self):
        return self.__perm

    def getRoutes(self):
        return self.__routes

    def getFitness(self):
        return self.__fitness

    def getSize(self):
        return len(self.__perm)

    def getCustomer(self, index):
        return self.__perm[index]

    def setPermutation(self, perm):
        self.__perm = copy(perm)
        self._evaluate()

    def swap(self, i, j):
        if i == j:
            return
        self.__perm[i], self.__perm[j] = self.__perm[j], self.__perm[i]
        self._evaluate()

    def insert(self, i, j):
        if i == j:
            return
        customer = self.__perm.pop(i)
        self.__perm.insert(j, customer)
        self._evaluate()

    def reverse(self, i, j):
        if i == j:
            return
        if i > j:
            i, j = j, i
        self.__perm[i:j + 1] = self.__perm[i:j + 1][::-1]
        self._evaluate()

    def isValid(self):
        customers = CVRP_Problem_Instance.getCustomerList()

        if len(self.__perm) != len(customers):
            return "Permutation Size Mismatch"

        if sorted(self.__perm) != sorted(customers):
            return "Missing or Repeating Customers"

        capacity = CVRP_Problem_Instance.getCapacity()
        for route in self.__routes:
            load = sum(CVRP_Problem_Instance.getDemand(node) for node in route if node != CVRP_Problem_Instance.getDepot())
            if load > capacity:
                return "Capacity Violation"

        if self.__fitness < 0:
            return "Problem with Fitness Value"

        return "Everything is Fine"

    def __str__(self):
        return f"{self.__fitness:.2f}; routes={self.__routes}; Valid:{self.isValid()}"