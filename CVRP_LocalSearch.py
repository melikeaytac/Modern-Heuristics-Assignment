from copy import copy
from CVRP_Solution import CVRP_Solution


class CVRP_LocalSearch:

    @staticmethod
    def two_opt_first(s: CVRP_Solution, max_iter=30):
        sn = copy(s)
        n = sn.getSize()

        iteration = 0
        modified = True

        while modified and iteration < max_iter:
            modified = False
            iteration += 1

            for i in range(n - 1):
                for j in range(i + 1, n):
                    # deepcopy yerine hızlı kopya
                    perm = sn.getPermutation().copy()
                    perm[i:j + 1] = perm[i:j + 1][::-1]

                    neighbor = CVRP_Solution(perm)

                    if neighbor.getFitness() < sn.getFitness():
                        sn = neighbor
                        modified = True
                        break

                if modified:
                    break

        return sn