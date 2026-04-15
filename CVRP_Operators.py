from random import randrange
from CVRP_Solution import CVRP_Solution


class CVRP_Operators:

    @classmethod
    def crossover(cls, crossoverType, P1: list, P2: list):
        if crossoverType == "OX":
            return CVRP_Operators._OX(P1, P2)
        elif crossoverType == "PMX":
            return CVRP_Operators._PMX(P1, P2)
        else:
            return CVRP_Operators._OX(P1, P2)

    @classmethod
    def _OX(cls, P1: list, P2: list):
        size = len(P1)
        c1, c2 = [-1] * size, [-1] * size

        left = randrange(size)
        right = randrange(size)
        if left > right:
            left, right = right, left

        c1[left:right + 1] = P1[left:right + 1]
        c2[left:right + 1] = P2[left:right + 1]

        fill1 = [x for x in P2 if x not in c1]
        fill2 = [x for x in P1 if x not in c2]

        idx1 = 0
        idx2 = 0
        for i in range(size):
            if c1[i] == -1:
                c1[i] = fill1[idx1]
                idx1 += 1
            if c2[i] == -1:
                c2[i] = fill2[idx2]
                idx2 += 1

        return c1, c2

    @classmethod
    def _PMX(cls, P1: list, P2: list):
        size = len(P1)
        c1, c2 = [-1] * size, [-1] * size

        left = randrange(size)
        right = randrange(size)
        if left > right:
            left, right = right, left

        c1[left:right + 1] = P2[left:right + 1]
        c2[left:right + 1] = P1[left:right + 1]

        def pmx_fill(child, parent, donor):
            for i in range(left, right + 1):
                if parent[i] not in child:
                    pos = i
                    value = parent[i]
                    while True:
                        mapped_value = donor[pos]
                        pos = parent.index(mapped_value)
                        if child[pos] == -1:
                            child[pos] = value
                            break
            for i in range(size):
                if child[i] == -1:
                    child[i] = parent[i]
            return child

        c1 = pmx_fill(c1, P1, P2)
        c2 = pmx_fill(c2, P2, P1)

        return c1, c2

    @classmethod
    def mutate(cls, mutationType, P: CVRP_Solution):
        if mutationType == "swap":
            CVRP_Operators._swap(P)
        elif mutationType == "insert":
            CVRP_Operators._insert(P)
        elif mutationType == "reverse":
            CVRP_Operators._reverse(P)

    @classmethod
    def _swap(cls, C: CVRP_Solution):
        n = C.getSize() // 10 + 1
        size = C.getSize()
        for _ in range(n):
            i, j = randrange(size), randrange(size)
            C.swap(i, j)

    @classmethod
    def _insert(cls, C: CVRP_Solution):
        n = C.getSize() // 10 + 1
        size = C.getSize()
        for _ in range(n):
            i, j = randrange(size), randrange(size)
            C.insert(i, j)

    @classmethod
    def _reverse(cls, C: CVRP_Solution):
        n = C.getSize() // 10 + 1
        size = C.getSize()
        for _ in range(n):
            i, j = randrange(size), randrange(size)
            C.reverse(i, j)