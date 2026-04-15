from copy import copy, deepcopy
from random import randrange
from CVRP_Solution import CVRP_Solution


class CVRP_Population:
    def __init__(self, size):
        self.__size = size
        self.__population = []
        for _ in range(size):
            self.__population.append(CVRP_Solution())

    def getPopulationSize(self):
        return len(self.__population)

    def getPopulation(self):
        return self.__population

    def getSolution(self, index):
        return self.__population[index]

    def findBestSolution(self):
        best = copy(self.__population[0])
        for i in range(1, len(self.__population)):
            if self.__population[i].getFitness() < best.getFitness():
                best = copy(self.__population[i])
        return copy(best)

    def addSolution(self, solution: CVRP_Solution):
        self.__population.append(solution)

    def extendPopulation(self, population):
        if population is not None:
            for solution in population.getPopulation():
                self.addSolution(copy(solution))

    def tournamentSelection(self, tournamentSize):
        winner = self.getSolution(randrange(self.getPopulationSize()))
        for _ in range(tournamentSize - 1):
            rival = self.getSolution(randrange(self.getPopulationSize()))
            if rival.getFitness() < winner.getFitness():
                winner = rival
        return copy(winner)

    def survivalSelection(self):
        self.__population = sorted(self.__population, key=lambda x: x.getFitness())

        elitism_count = self.getPopulationSize() // 10
        if elitism_count == 0:
            elitism_count = 1

        pop = deepcopy(self.__population[:elitism_count])
        self.__population = deepcopy(self.__population[elitism_count:])

        while len(pop) < self.__size:
            winner = self.tournamentSelection(2)
            pop.append(deepcopy(winner))

        self.__population = deepcopy(pop)

    def __str__(self):
        s = ""
        for i in range(self.getPopulationSize()):
            s += f"{i}) {self.getSolution(i).getFitness()}, Valid: {self.getSolution(i).isValid()}\n"
        return s