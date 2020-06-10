# run: python route.py start_station end_station

from sys import argv
from math import inf

matrix = []
stationDict = {}

# number of stations
N = 250


class PriorityQueue():
    def __init__(self):
        self.pq = []

    def get_key(self, elem):
        return elem[0]

    def pq_push(self, distance, node):
        if self.pq:
            self.pq.append((distance, node))
            self.pq.sort(key=self.get_key)
        else:
            self.pq.append((distance, node))


    def pq_pop(self):
        return self.pq.pop(0)


def main():
    # initialization
    load_stations("stations.txt")
    load_edges("edges.txt")

    if len(argv) != 3:
        print("Usage: python route.py start_station end_station")
        return 1

    if argv[1] not in stationDict.keys() or argv[2] not in stationDict.keys():
        print("Invalid station.")
        return 1
    start = stationDict.get(argv[1])
    end = stationDict.get(argv[2])
    # print(start, end)
    print("Shortest time between %s and %s is %i mins" % (argv[1], argv[2], dijkstra(start,end)))




def load_stations(textfile):
    # load stations into a python dictionary
    with open(textfile, "r", encoding="utf-8") as file:
        for line in file.readlines():
            lineList = line.strip().split("\t")
            stationDict[lineList[1]] = int(lineList[0])          



def load_edges(textfile):
    # load txt file into a matrix
    # initialize matrix[N][N] with infinity
    for i in range(N):
        matrix.append([inf for i in range(N)])
    with open(textfile, "r") as file:
        for line in file.readlines():
            lineList = line.strip().split("\t")
            from_id = int(lineList[0])
            to_id = int(lineList[1])
            weight = int(lineList[-1])
            matrix[from_id][to_id] = weight


def dijkstra(start, end):
    # set all distances from source as infinity
    d = [inf] * N
    visited = [False] * N
    priorityqueue = PriorityQueue()
    priorityqueue.pq_push(0, start)

    # set source node to zero
    d[start] = 0
    
    while True:
        # print(priorityqueue.pq)
        current_distance, current_node = priorityqueue.pq_pop()
        # print(current_node)
        if visited[end]:
            return d[end]

        for i in range(N):
            # find neighbours of current node
            if matrix[current_node][i] < inf and not visited[i]:
                distance = d[current_node] + matrix[current_node][i]
                # only update if calculated value is smaller 
                if distance < d[i]:
                    d[i] = distance
                    priorityqueue.pq_push(d[i], i)

        # mark node as visited
        visited[current_node] = True



main()
