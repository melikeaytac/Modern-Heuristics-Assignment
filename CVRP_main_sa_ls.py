import time
import sys
from contextlib import redirect_stdout, redirect_stderr
from statistics import mean

from CVRP_Problem_Instance import CVRP_Problem_Instance
from CVRP_SimulatedAnnealing import CVRP_SimulatedAnnealing


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


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

    best_run_idx = min(range(len(results)), key=lambda i: results[i])

    print("\n===== SUMMARY =====")
    print("Best Result of 10 Runs:", min(results))
    print("Average Result of 10 Runs:", round(mean(results), 2))
    print("Best Result Found At Run:", best_run_idx + 1)
    print("Best Time of Finding Best Result:", round(times[best_run_idx], 4))
    print("Average Time of 10 Runs:", round(mean(times), 4))


if __name__ == "__main__":
    instanceName = "./problem_instances_CVRP/E-n51-k5.vrp"
    output_file = "sa_results.txt"

    with open(output_file, "a", encoding="utf-8") as f:
        tee = Tee(sys.stdout, f)
        with redirect_stdout(tee), redirect_stderr(tee):
            print("\n" + "=" * 60)
            print("INSTANCE:", instanceName)
            print("START TIME:", time.strftime("%Y-%m-%d %H:%M:%S"))
            print("=" * 60)
            print()

            # single_run(instanceName)
            ten_runs(instanceName)

            print()
            print("Results are also saved to:", output_file)
