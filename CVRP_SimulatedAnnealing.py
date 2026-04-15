import math
from random import choice, random, randrange, seed

from CVRP_LocalSearch import CVRP_LocalSearch
from CVRP_Solution import CVRP_Solution


class CVRP_SimulatedAnnealing:

    def __init__(
        self,
        initialTemperature=100.0,
        coolingRate=0.99,
        minTemperature=1.0,
        iterationsPerTemp=80,
        applyLocalSearch=True,
        localSearchRate=0.15,
        localSearchMaxIter=30,
        maxNoImprove=40,
        randomSeed=None,
    ):
        self.__initialTemperature = initialTemperature
        self.__coolingRate = coolingRate
        self.__minTemperature = minTemperature
        self.__iterationsPerTemp = iterationsPerTemp
        self.__applyLocalSearch = applyLocalSearch
        self.__localSearchRate = localSearchRate
        self.__localSearchMaxIter = localSearchMaxIter
        self.__maxNoImprove = maxNoImprove

        if randomSeed is not None:
            seed(randomSeed)

        self.__best = None

    def run(self):
        current = CVRP_Solution()

        if self.__applyLocalSearch:
            current = CVRP_LocalSearch.two_opt_first(current, max_iter=self.__localSearchMaxIter)

        best = self.__cloneSolution(current)
        temperature = self.__initialTemperature
        noImproveCounter = 0

        while temperature > self.__minTemperature and noImproveCounter < self.__maxNoImprove:
            improved = False

            for _ in range(self.__iterationsPerTemp):
                candidate = self.__generateNeighbor(current)

                if self.__applyLocalSearch and random() < self.__localSearchRate:
                    candidate = CVRP_LocalSearch.two_opt_first(candidate, max_iter=self.__localSearchMaxIter)

                delta = candidate.getFitness() - current.getFitness()

                # Accept worse moves with temperature-based probability to escape local minima.
                if delta < 0 or random() < math.exp(-delta / max(temperature, 1e-12)):
                    current = candidate

                    if current.getFitness() < best.getFitness():
                        best = self.__cloneSolution(current)
                        improved = True

            if improved:
                noImproveCounter = 0
            else:
                noImproveCounter += 1

            temperature *= self.__coolingRate

        self.__best = best

    def getBestSolution(self):
        return self.__best

    def __cloneSolution(self, solution):
        return CVRP_Solution(solution.getPermutation().copy())

    def __generateNeighbor(self, solution):
        neighbor = self.__cloneSolution(solution)
        size = neighbor.getSize()

        if size < 2:
            return neighbor

        i = randrange(size)
        j = randrange(size)
        while j == i:
            j = randrange(size)

        move = choice(("swap", "insert", "reverse"))

        if move == "swap":
            neighbor.swap(i, j)
        elif move == "insert":
            neighbor.insert(i, j)
        else:
            neighbor.reverse(i, j)

        return neighbor
