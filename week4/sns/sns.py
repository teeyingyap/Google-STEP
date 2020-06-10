# run: python sns.py start_name end_name

from sys import argv

graph = {}
nicknameDict = {}

class Node():
    def __init__(self, num, parent):
        self.num = num
        self.parent = parent


def main():
    load_nicknames("nicknames.txt")
    load_links("links.txt")

    if len(argv) != 3:
        print("Usage: python sns.py start_name end_name")
        return 1
    
    # check whether name exists  
    if argv[1] not in nicknameDict.keys() or argv[2] not in nicknameDict.keys():
        print("Invalid name.")
        return 1
    # get() return value of the item
    start = nicknameDict.get(argv[1])
    end = nicknameDict.get(argv[2])
    if dfs(start, end):
        print("%s can reach %s" % (argv[1], argv[2]))
    else:
        print("%s cannot reach %s" % (argv[1], argv[2]))

    print("The shortest path is", bfs(start, end))
    test(bfs(start, end))



def load_nicknames(textfile):
    # load nicknames into a python dictionary
    with open(textfile, "r") as file:
        for line in file.readlines():
            lineList = line.strip().split("\t")
            nicknameDict[lineList[1]] = int(lineList[0])            


def load_links(textfile):
    # load txt file into a python dictionary
    with open(textfile, "r") as file:
        for line in file.readlines():
            lineList = line.strip().split("\t")
            key = int(lineList[0])
            if key in graph:
                graph[key].append(int(lineList[1]))
            else:
                graph[key] = [int(lineList[1])]



# check whether a node can be reached with recursive dfs
def dfs(start, end, visited=[]):
    visited.append(start)

    if start == end:
        return True

    for node in graph[start]:
        if node not in visited:
            result = dfs(node, end, visited)
            if result:
                return True

    return False

# find the shortest path with bfs 
def bfs(start, end):
    queue = []
    queue.append(Node(start, None))
    # keep track of visited nodes
    visited = []

    while queue:
        # remove from front of queue
        node = queue[0]
        queue = queue[1:]
                    
        if node.num == end:
            path = []
            while node is not None:
                path.append(node.num)
                node = node.parent
            return path[::-1]

        visited.append(node.num)

        # Add the user which the node is following to queue
        for follow in graph[node.num]:
            if follow not in visited:
                adjNode = Node(follow, node)
                queue.append(adjNode)



def test(path_list):
    for i in range(1, len(path_list)):
        if path_list[i] not in graph[path_list[i - 1]]:
            print(path_list[i - 1], "does not follow ", path_list[i])
    print("OK, valid path")





main()


