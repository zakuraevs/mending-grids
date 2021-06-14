from itertools import combinations 

# Class representing a 2-D grid
class Graph:
    def __init__(self, rows, cols):
        # row and column counts
        self.rows = rows
        self.cols = cols
        # matrix of nodes, each nodes is an integet 0 ... rows x cols
        self.nodes = []
        # matrix of colors for each node
        self.coloring = []
        # mapping from node number to its [row, col] address
        self.nameToLocation = {}

        # populating the graph
        nodeNum = 1
        for row in range(cols):
            self.nodes.append([])
            self.coloring.append([])
            for col in range(rows):
                self.nodes[row].append(nodeNum)
                self.coloring[row].append(0)  
                self.nameToLocation[nodeNum] = [row, col]
                nodeNum += 1

    # get addresses of neighbors of a node given its address
    def getNeighbors(self, row, col):
        neighbors = []

        if row == 0:
            if col == 0:
                neighbors.append([0,1])
                neighbors.append([1,0])
            elif col == self.rows - 1:
                neighbors.append([0, self.rows - 2])
                neighbors.append([1, self.rows - 1])
            else:
                neighbors.append([0, col - 1])
                neighbors.append([0, col + 1])
                neighbors.append([1, col])
        elif row == self.rows - 1:
            if col == 0:
                neighbors.append([self.rows - 1, 1])
                neighbors.append([self.rows - 2, 0])
            elif col == self.rows - 1:
                neighbors.append([self.rows - 1, self.cols - 2])
                neighbors.append([self.rows - 2, self.cols - 1])
            else:
                neighbors.append([self.rows - 1, col - 1])
                neighbors.append([self.rows - 1, col + 1])
                neighbors.append([self.rows - 2, col])
        else:
            if col == 0:
                neighbors.append([row - 1, 0])
                neighbors.append([row, 1])
                neighbors.append([row + 1, 0])
            elif col == self.rows - 1:
                neighbors.append([row - 1, self.cols - 1])
                neighbors.append([row, self.cols - 2])
                neighbors.append([row + 1, self.cols - 1])
            else:
                neighbors.append([row, col - 1])
                neighbors.append([row, col + 1])
                neighbors.append([row - 1, col])
                neighbors.append([row + 1, col])

        return neighbors

    # check if current coloring is valid
    def isValidWeak2Coloring(self):
        for row in range(self.rows):
            for col in range(self.cols):
                currentNeighbs = self.getNeighbors(row,col)
                currentColor = self.coloring[row][col]
                nodeOk = False
                for neighb in currentNeighbs:
                    neighbColor = self.coloring[neighb[0]][neighb[1]]
                    if neighbColor != currentColor:
                        nodeOk = True
                        break
                if not nodeOk:
                    return False
        return True

    # check if a node at row, col is happy - has at leas 1 neighbor of a different color
    def isHappyNode(self, row, col):
        node = self.nodes[row][col]
        color = self.coloring[row][col]
        neighbs = self.getNeighbors(row, col)
        for n in neighbs:
            nColor = self.coloring[n[0]][n[1]]
            if nColor != color:
                return True
        return False

# get the difference of 2 lists
def listDifferece(l1, l2):
    return list(set(l1) - set(l2)) + list(set(l2) - set(l1))

# computationally check if any partial solution with 1 uncolored node can be mended with a window of at most 3 nodes
def main():

    # dimensions of the graphs
    rows = 5
    cols = 5

    # creating the graph
    graph = Graph(rows, cols)

    # printing names of all nodes
    print("Names of all nodes")
    for row in range(rows):
        for col in range(cols):
            print(graph.nodes[row][col], end =" ")
        print()
    print()
    

    # coloring corner nodes - we assume a partial solution is correct,
    # no need to change corners 
    graph.coloring[0][0] = 3
    graph.coloring[0][1] = 4
    graph.coloring[1][0] = 5

    graph.coloring[0][cols - 1] = 3
    graph.coloring[0][cols - 2] = 4
    graph.coloring[1][cols - 1] = 5

    graph.coloring[rows - 1][0] = 3
    graph.coloring[rows - 1][1] = 4
    graph.coloring[rows - 2][0] = 5
    
    graph.coloring[rows - 1][cols - 1] = 3
    graph.coloring[rows - 1][cols - 2] = 4
    graph.coloring[rows - 2][cols - 1] = 5

    # printing initial coloring
    print("Initial coloring")
    for row in range(rows):
        for col in range(cols):
            print(graph.coloring[row][col], end =" ")
        print()
    print()

    # all nodes that could be affected by mending under the assumption of window of size 3 nodes within radius 1 of center
    allInterestingNodes = [3, 7, 8, 9, 11, 12 ,14, 15, 17, 18, 19, 23]

    # counting iterations, should be 2^12 = 4,096
    iterations = 0

    # going over all possible colorings of the 12 interesting nodes
    for redCount in range(13):
        # all possible combinations of interesting nodes with redCount red nodes, starting at 0, 1, 2, ..., 12
        redCombinations = combinations(allInterestingNodes, redCount)

        # going over all combinations of red nodes of length redCount
        for redNodes in redCombinations:
            iterations += 1

            # blue nodes
            blueNodes = listDifferece(allInterestingNodes, redNodes)

            # coloring red nodes
            for n in redNodes:
                address = graph.nameToLocation[n]
                graph.coloring[address[0]][address[1]] = 1
            
            # coloring blue nodes
            for n in blueNodes:
                address = graph.nameToLocation[n]
                graph.coloring[address[0]][address[1]] = 2

            # trying to patch the hole with red
            graph.coloring[2][2] = 1
            currentlyValid = graph.isValidWeak2Coloring()
            if currentlyValid:
                continue

            # trying to patch the hole with blue
            graph.coloring[2][2] = 2
            currentlyValid = graph.isValidWeak2Coloring()
            if currentlyValid:
                continue

            # trying to swap top and bottom
            if (not graph.isHappyNode(1, 2)) or (not graph.isHappyNode(3, 2)):
                topColor = graph.coloring[1][2]
                graph.coloring[1][2] = graph.coloring[3][2]
                graph.coloring[3][2] = topColor
            
            currentlyValid = graph.isValidWeak2Coloring()
            if currentlyValid:
                continue

            # trying to swap left and right
            if (not graph.isHappyNode(2, 1)) or (not graph.isHappyNode(2, 3)):
                leftColor = graph.coloring[2][1]
                graph.coloring[2][1] = graph.coloring[2][3]
                graph.coloring[2][3] = leftColor

            currentlyValid = graph.isValidWeak2Coloring()
            if currentlyValid:
                continue
            # if we got this far, the hypothesis was false :(
            else:
                print("Failed to mend!")
                print("\n")
                for row in range(rows):
                    for col in range(cols):
                        print(graph.coloring[row][col], end =" ")
                    print()

    print("Iterations: ")
    print(iterations)
    print()

    # printing last valid coloring visited
    
    print("Last checked coloring")
    for row in range(rows):
        for col in range(cols):
            print(graph.coloring[row][col], end =" ")
        print()

main()