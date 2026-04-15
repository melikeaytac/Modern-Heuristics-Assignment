import time
from statistics import mean

from CVRP_Problem_Instance import CVRP_Problem_Instance
from CVRP_GeneticAlgorithm import CVRP_GeneticAlgorithm


def single_run(instanceName):
    CVRP_Problem_Instance(instanceName)

    ga = CVRP_GeneticAlgorithm(
        popSize=50,
        nbOfGenerations=100,
    )

    start = time.time()
    ga.run()
    end = time.time()

    best = ga.getBestSolution()
    print("Best fitness:", best.getFitness())
    print("Routes:", best.getRoutes())
    print("Elapsed time:", round(end - start, 4), "seconds")


def ten_runs(instanceName):
    results = []
    times = []

    for run_no in range(10):
        CVRP_Problem_Instance(instanceName)

        ga = CVRP_GeneticAlgorithm()

        start = time.time()
        ga.run()
        elapsed = time.time() - start

        best = ga.getBestSolution()
        results.append(best.getFitness())
        times.append(elapsed)

        print(f"Run {run_no + 1}: fitness={best.getFitness():.2f}, time={elapsed:.4f}s")

    print("\n===== SUMMARY =====")
    print("Best Result of 10 Runs:", min(results))
    print("Average Result of 10 Runs:", round(mean(results), 2))
    print("Best Time of Finding Best Result:", round(min(times), 4))
    print("Average Time of 10 Runs:", round(mean(times), 4))


if __name__ == "__main__":
    # Example TSPLIB CVRP instance path:
    # ./problem_instances_CVRP/A-n32-k5.vrp
    instanceName = "./problem_instances_CVRP/A-n32-k5.vrp"

    # single_run(instanceName)
    ten_runs(instanceName)