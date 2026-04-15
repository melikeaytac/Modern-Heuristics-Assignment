import math


class CVRP_Problem_Instance:
    __n = 0                      # customer count (without depot)
    __capacity = 0
    __coords = {}
    __demands = {}
    __depot = 1                  # TSPLIB usually uses 1-based depot id
    __DM = []

    def __init__(self, instanceName):
        self.instanceName = instanceName
        self.__readFromFile()
        self.__calculateDM()

    def __readFromFile(self):
        section = None

        with open(self.instanceName, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        coords = {}
        demands = {}
        depot = 1
        capacity = 0
        dimension = 0

        for line in lines:
            if line.startswith("DIMENSION"):
                dimension = int(line.split(":")[-1].strip())
            elif line.startswith("CAPACITY"):
                capacity = int(line.split(":")[-1].strip())
            elif line.startswith("NODE_COORD_SECTION"):
                section = "NODE_COORD_SECTION"
                continue
            elif line.startswith("DEMAND_SECTION"):
                section = "DEMAND_SECTION"
                continue
            elif line.startswith("DEPOT_SECTION"):
                section = "DEPOT_SECTION"
                continue
            elif line.startswith("EOF"):
                break
            else:
                if section == "NODE_COORD_SECTION":
                    parts = line.split()
                    node_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    coords[node_id] = (x, y)
                elif section == "DEMAND_SECTION":
                    parts = line.split()
                    node_id = int(parts[0])
                    demand = int(parts[1])
                    demands[node_id] = demand
                elif section == "DEPOT_SECTION":
                    if line != "-1":
                        depot = int(line)

        CVRP_Problem_Instance.__capacity = capacity
        CVRP_Problem_Instance.__coords = coords
        CVRP_Problem_Instance.__demands = demands
        CVRP_Problem_Instance.__depot = depot
        CVRP_Problem_Instance.__n = dimension - 1  # excluding depot

    def __calculateDM(self):
        all_nodes = sorted(CVRP_Problem_Instance.__coords.keys())
        max_id = max(all_nodes)

        CVRP_Problem_Instance.__DM = [[0 for _ in range(max_id + 1)] for _ in range(max_id + 1)]

        for i in all_nodes:
            xi, yi = CVRP_Problem_Instance.__coords[i]
            for j in all_nodes:
                if i == j:
                    dist = 0
                else:
                    xj, yj = CVRP_Problem_Instance.__coords[j]
                    dist = int(round(math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)))
                CVRP_Problem_Instance.__DM[i][j] = dist

    @classmethod
    def getNbOfCustomers(cls):
        return cls.__n

    @classmethod
    def getCapacity(cls):
        return cls.__capacity

    @classmethod
    def getDepot(cls):
        return cls.__depot

    @classmethod
    def getDemand(cls, node):
        return cls.__demands[node]

    @classmethod
    def getDistance(cls, node1, node2):
        return cls.__DM[node1][node2]

    @classmethod
    def getCustomerList(cls):
        return [node for node in sorted(cls.__coords.keys()) if node != cls.__depot]