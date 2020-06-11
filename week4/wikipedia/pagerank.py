import numpy as np

# graph = {0: [3,5,1], 1: [0, 6, 7], 2: [4, 6, 0]}

# use random surfer model

# first map all links inside an adjacency list

# loop through the adjacency list to check what the node points to 
# then construct the transition matrix where each column represents one page
# construct row by row then transpose it


# let initial page vector to be 1/N, where N = number of pages


# test
# d = 0.85
# A = np.array([[0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0], [1/3, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
# 			  [1/3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [1/3, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0],
# 			  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5], [0.0, 0.0, 0.0, 0.5, 1.0, 0.0, 0.0, 0.5], [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0]])


# x = np.array([[1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8]]).T
# I = np.ones((8, 8))

# for k in range(8):
# 	M = d*(A) + ((1.0-d)/8)*I
# 	x = M.dot(x)
# 	# print(x)





def main():

	graph = {}
	pageDict = {}
	A = []
	load_pages("pages.txt", pageDict)
	load_links("links.txt", graph)

	N = len(pageDict)
	A = transition_matrix(A, graph, N)
	for i in range(N):
		print(A[i][0])

	# intial page column vector
	x = np.tile(np.array([1/N]), (N, 1))

	I = np.ones((N, N))

	# damping factor
	# the probability that the user will continue clicking
	d = 0.85
	num_iteration = 13 # just a random number for now
	for k in range(num_iteration):
		M = d*(A) + ((1.0-d)/N)*I
		x = M.dot(x)






def transition_matrix(A, graph, N):
	# try to find who is pointing to the current node
	A = np.zeros((N, N))
	for key, value in graph.items():
		cell_value = 1 / len(value)
		for link in value:
			A[key][link] = cell_value
	return A.T




def load_pages(textfile, pageDict):
    # load pages into a python dictionary
    with open(textfile, "r", encoding="utf-8") as file:
        for line in file.readlines():
            lineList = line.strip().split("\t")
            pageDict[lineList[1]] = int(lineList[0])          



def load_links(textfile, graph):
    # load txt file into a adjacency list
    with open(textfile, "r") as file:
        for line in file.readlines():
            lineList = line.strip().split("\t")
            key = int(lineList[0])
            if key in graph:
                graph[key].append(int(lineList[1]))
            else:
                graph[key] = [int(lineList[1])]



if  __name__ == '__main__':
	main()