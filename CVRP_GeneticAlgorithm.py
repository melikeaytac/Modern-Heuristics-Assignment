from random import random
from copy import copy
from CVRP_Population import CVRP_Population
from CVRP_Operators import CVRP_Operators
from CVRP_Solution import CVRP_Solution
from CVRP_LocalSearch import CVRP_LocalSearch


class CVRP_GeneticAlgorithm:

    def __init__(self, popSize=100, crossoverType="OX", crossoverRate=0.8,
                 mutationType="swap", mutationRate=0.2, nbOfGenerations=100,
                 applyLocalSearch=True):
        self.__popSize = popSize
        self.__crossoverType = crossoverType
        self.__crossoverRate = crossoverRate
        self.__mutationType = mutationType
        self.__mutationRate = mutationRate
        self.__nbOfGenerations = nbOfGenerations
        self.__applyLocalSearch = applyLocalSearch

    def run(self):
        population = CVRP_Population(self.__popSize)
        self.__best = population.findBestSolution()

        for _ in range(self.__nbOfGenerations):
            offspring = CVRP_Population(0)

            for _ in range(self.__popSize // 2):
                p1 = population.tournamentSelection(2)
                p2 = population.tournamentSelection(2)

                c1, c2 = copy(p1), copy(p2)

                if random() < self.__crossoverRate:
                    c1perm, c2perm = CVRP_Operators.crossover(
                        self.__crossoverType,
                        c1.getPermutation(),
                        c2.getPermutation()
                    )
                    c1 = CVRP_Solution(c1perm)
                    c2 = CVRP_Solution(c2perm)

                if random() < self.__mutationRate:
                    CVRP_Operators.mutate(self.__mutationType, c1)
                    CVRP_Operators.mutate(self.__mutationType, c2)

                # probabilistic local search (çok kritik)
                if self.__applyLocalSearch and random() < 0.2:
                 c1 = CVRP_LocalSearch.two_opt_first(c1, max_iter=30)

                self.__updateBest(c1)
                self.__updateBest(c2)

                offspring.addSolution(c1)
                offspring.addSolution(c2)

            population.extendPopulation(offspring)
            population.survivalSelection()

    def getBestSolution(self):
        return self.__best

    def __updateBest(self, solution: CVRP_Solution):
        if (solution is not None) and (solution.getFitness() < self.__best.getFitness()):
            self.__best = copy(solution)