import time
from statistics import mean

from CVRP_Problem_Instance import CVRP_Problem_Instance
from CVRP_SimulatedAnnealing import CVRP_SimulatedAnnealing


def single_run(instanceName):
    CVRP_Problem_Instance(instanceName)

    sa = CVRP_SimulatedAnnealing()

    start = time.time()
    sa.run()
    end = time.time()

    best = sa.getBestSolution()
    print("Best fitness:", best.getFitness())
    print("Routes:", best.getRoutes())
    print("Elapsed time:", round(end - start, 4), "seconds")


def ten_runs(instanceName):
    results = []
    times = []

    for run_no in range(10):
        CVRP_Problem_Instance(instanceName)

        sa = CVRP_SimulatedAnnealing()

        start = time.time()
        sa.run()
        elapsed = time.time() - start

        best = sa.getBestSolution()
        results.append(best.getFitness())
        times.append(elapsed)

        print(f"Run {run_no + 1}: fitness={best.getFitness():.2f}, time={elapsed:.4f}s")

    print("\n===== SUMMARY =====")
    print("Best Result of 10 Runs:", min(results))
    print("Average Result of 10 Runs:", round(mean(results), 2))
    print("Best Time of Finding Best Result:", round(min(times), 4))
    print("Average Time of 10 Runs:", round(mean(times), 4))


if __name__ == "__main__":
    instanceName = "./problem_instances_CVRP/A-n32-k5.vrp"

    # single_run(instanceName)
    ten_runs(instanceName)
