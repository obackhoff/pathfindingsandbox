from tkinter import *
import random
import time
from node import *
from sebsheap import *

class SearchTools():

    def getObstacles(slef, canvas):
        arr = []
        for row in canvas.grid:
            for cell in row:
                if cell.fill and canvas.isNotStartGoal(cell):
                    arr.append(cell)
        return arr

    def isNotObstacle(self, obstacles, point):
        for o in obstacles:
            if(o.abs == point.abs and o.ord == point.ord):
                return False
        return True

class AStar():
    NAME = "A*"
    canvas = None

    def __init__(self, canvas):
        self.canvas = canvas

    def run(self):

        tic = time.clock()

        visited = []
        path = []

        openSet = []
        closedSet =[]

        grid = self.createGrid(self.canvas)

        startNode = Node(self.canvas.grid[self.canvas.START[0]][self.canvas.START[1]], True, self.canvas.START[0],self.canvas.START[1])
        goalNode = Node(self.canvas.grid[self.canvas.GOAL[0]][self.canvas.GOAL[1]], True, self.canvas.GOAL[0],self.canvas.GOAL[1])

        grid[startNode.x][startNode.y] = startNode
        grid[goalNode.x][goalNode.y] = goalNode

        openSet.append(grid[startNode.x][startNode.y])

        while(len(openSet) > 0):
            currentNode = openSet[0]
            for o in openSet:
                if o.fCost() < currentNode.fCost() or o.fCost() == currentNode.fCost() and o.hCost < currentNode.hCost:
                    currentNode = o

            openSet.remove(currentNode)
            closedSet.append(currentNode)

            if (currentNode == goalNode):
                print("DONE")
                break

            #print("current = " + str(currentNode.x) + ", " + str(currentNode.y) + "; goal = " + str(goalNode.x) + ", " + str(goalNode.y))
            for n in self.getNeighbours(grid, currentNode):
                if not n.walkable or n in closedSet:
                    continue

                newMovCostToNeighbour = currentNode.gCost + self.getDistance(currentNode, n)
                if newMovCostToNeighbour < n.gCost or n not in openSet:
                    visited.append(n)
                    n.gCost = newMovCostToNeighbour
                    n.hCost = self.getDistance(n, goalNode)
                    n.setParent(currentNode)

                    if n not in openSet:
                        openSet.append(n)

        path = self.getCellsPath(self.retracePath(startNode, goalNode))
        print("path lenght = " + str(len(path)))
        visited = self.getCellsPath(visited)

        toc = time.clock()
        print("time elapsed (run) = " + str(toc - tic))
        return visited, path


    def createGrid(self, canvas):
        grid = []
        # st = SearchTools()
        # obstacles = st.getObstacles(canvas)

        for i in range(len(canvas.grid)):
            temp = []
            for j in range(len(canvas.grid[0])):
                walkable = False
                # if st.isNotObstacle(obstacles, canvas.grid[i][j]):
                if not canvas.grid[i][j].fill:
                    walkable = True
                temp.append(Node(canvas.grid[i][j], walkable, i, j))
            grid.append(temp)
        return grid

    def retracePath(self, start, goal):
        path = []
        currentNode = goal
        while (currentNode != start):
            path.append(currentNode)
            currentNode = currentNode.getParent()

        path.reverse()
        return path

    def getCellsPath(self, path):
        cells = []
        for p in path:
            cells.append(p.cell)
        return cells

    def getNeighbours(self, grid, node):
        neighbours = []
        xmax = len(self.canvas.grid)
        ymax = len(self.canvas.grid[0])

        for x in range(-1,2):
            for y in range(-1,2):
                if x == 0 and y == 0:
                    continue

                checkX = node.x + x
                checkY = node.y + y

                if checkX >= 0 and checkX < xmax and checkY >=0 and checkY < ymax:
                    neighbours.append(grid[checkX][checkY])
        return neighbours

    def getDistance(self, nodeA, nodeB):
        distX = abs(nodeA.x - nodeB.x)
        distY = abs(nodeA.y - nodeB.y)

        if distX > distY:
            return 14 * distY + 10 * (distX - distY)
        return 14 * distX + 10 * (distY - distX)

class DumbSearch(SearchTools):
    NAME = "Dumb Search"
    MODE = ""
    canvas = None

    def __init__(self, canvas):
        self.MODE = "NODIAG"
        self.canvas = canvas

    def run(self):
        tic = time.clock()

        start = self.canvas.grid[self.canvas.START[0]][self.canvas.START[1]]
        goal = self.canvas.grid[self.canvas.GOAL[0]][self.canvas.GOAL[1]]
        visited = set()
        notAgain = []
        path = [start]

        cnt = 0
        while True:
            dist = 99999999
            tempN = start
            neighbours = self.getNeighbours(path[-1])
            for n in neighbours:
                d = self.sqDistance(n, goal)
                visited.add(n)
                if d <= dist and n not in notAgain:
                    dist = d
                    tempN = n
                    # if d == dist:
                    #     if random.randint(0,1): tempN = n
                    # else:
                    #     tempN = n
            if tempN in path:
                notAgain.append(path[len(path) - 1])
                tempN = random.sample(neighbours, 1)[0]
            path.append(tempN)
            #print("path= "+str(tempN.abs)+","+str(tempN.ord))
            # if tempN.abs == goal.abs and tempN.ord == goal.ord:
            if tempN == goal:
                print("DONE")
                break
            cnt += 1
        # print(len(path))

        print("path before = " + str(len(path)))
        path = self.cleanPath(path)

        print("path clean = " + str(len(path)))
        # print(len(visited))
        # print(len(set(visited)))
        toc = time.clock()
        print("time elapsed (run) = " + str(toc - tic))
        return visited, path

    def cleanPath(self, path):
        arr = []
        tempIDX = 0
        i = 0
        length = len(path)
        while i < length:
            tempIDX = i
            for j in range(length - i - 1):
                if path[i] == path[i + j + 1]:
                    tempIDX = i + j + 1
            i = tempIDX
            arr.append(path[i])
            i += 1
        return arr

    def getObstacles(self):
        arr = []
        for row in self.canvas.grid:
            for cell in row:
                if cell.fill and self.canvas.isNotStartGoal(cell):
                    arr.append(cell)
        return arr

    def isNotObstacle(self, obstacles, point):
        for o in obstacles:
            if(o.abs == point.abs and o.ord == point.ord):
                return False
        return True

    def sqDistance(slef, pointA, pointB):
        xA = pointA.abs
        yA = pointA.ord
        xB = pointB.abs
        yB = pointB.ord
        return (xA - xB) * (xA - xB) + (yA - yB) * (yA - yB)

    def getNeighbours(self, point):
        arr = []
        x = point.abs
        y = point.ord
        xmax = len(self.canvas.grid)
        ymax = len(self.canvas.grid[0])
        cell1 = self.canvas.grid[y][x + 1]
        cell2 = self.canvas.grid[y][x - 1]
        cell3 = self.canvas.grid[y - 1][x]
        cell4 = self.canvas.grid[y + 1][x]

        # obstacles = self.getObstacles()

        if self.MODE == "NODIAG":
            if x + 1 < xmax and not cell1.fill or not self.canvas.isNotStartGoal(cell1) and cell1.fill:
                arr.append(cell1)
            if x - 1 >= 0 and not cell2.fill or not self.canvas.isNotStartGoal(cell2) and cell2.fill:
                arr.append(cell2)
            if y - 1 >= 0 and not cell3.fill or not self.canvas.isNotStartGoal(cell3) and cell3.fill:
                arr.append(cell3)
            if y + 1 < ymax and not cell4.fill or not self.canvas.isNotStartGoal(cell4) and cell4.fill:
                arr.append(cell4)
        return arr

class DumbSearch2(DumbSearch):
    NAME = "Dumb Search Experiments"
    MODE = ""
    canvas = None

    def __init__(self, canvas):
        self.MODE = "NODIAG"
        self.canvas = canvas

    def run(self):
        tic = time.clock()

        start = self.canvas.grid[self.canvas.START[0]][self.canvas.START[1]]
        goal = self.canvas.grid[self.canvas.GOAL[0]][self.canvas.GOAL[1]]
        visited = set()
        notAgain = []
        path = [start]

        cnt = 0
        while True:
            dist = 99999999
            tempN = start
            neighbours = self.getNeighbours(path[len(path) - 1])
            for n in neighbours:
                d = self.sqDistance(n, goal)
                visited.add(n)
                if d <= dist and n not in notAgain:
                    dist = d
                    tempN = n
                    # if d == dist:
                    #     if random.randint(0, 1):
                    #         tempN = n
                    # else:
                    #     tempN = n
            if tempN in path:
                notAgain.append(path[len(path) - 1])
                tempArr = random.sample(neighbours, int(len(neighbours)/2))
                for t in tempArr:
                    dist = 99999999
                    d = self.sqDistance(t, goal)
                    if d <= dist:
                        dist = d
                        tempN = t


            path.append(tempN)
            # print("path= " + str(tempN.abs) + "," + str(tempN.ord))
            if tempN.abs == goal.abs and tempN.ord == goal.ord:
                print("DONE")
                break
            cnt += 1
        # print(len(path))

        print("path before = " + str(len(path)))
        path = self.cleanPath(path)
        print("path clean = " + str(len(path)))
        # print(len(path))
        toc = time.clock()
        print("time elapsed (run) = " + str(toc - tic))
        return visited, path

class DumbSearch8N(DumbSearch):
    NAME = "Dumb Search with 8 Neighbours"
    MODE = ""
    canvas = None

    def __init__(self, canvas):
        self.MODE = "NODIAG"
        self.canvas = canvas

    def getNeighbours(self, point):
        neighbours = []
        xmax = len(self.canvas.grid)
        ymax = len(self.canvas.grid[0])
        # obstacles = self.getObstacles()

        for x in range(-1,2):
            for y in range(-1,2):
                if x == 0 and y == 0:
                    continue

                checkX = point.ord + x
                checkY = point.abs + y
                cell = self.canvas.grid[checkX][checkY]

                if checkX >= 0 and checkX < xmax and checkY >=0 and checkY < ymax:
                    if not cell.fill or not self.canvas.isNotStartGoal(cell) and cell.fill:
                        neighbours.append(cell)
        return neighbours

class AStarHeap(AStar):
    NAME = "A*Heap"

    def run(self):

        tic = time.clock()

        visited = []
        path = []

        openSet = ListObjectHeap()
        nodeObjectToHeapObject = {}

        grid = self.createGrid(self.canvas)

        startNode = Node(self.canvas.grid[self.canvas.START[0]][self.canvas.START[1]], True, self.canvas.START[0],self.canvas.START[1])
        goalNode = Node(self.canvas.grid[self.canvas.GOAL[0]][self.canvas.GOAL[1]], True, self.canvas.GOAL[0],self.canvas.GOAL[1])

        grid[startNode.x][startNode.y] = startNode
        grid[goalNode.x][goalNode.y] = goalNode

        startNodeHeapObject = NodeObjectWrapper(startNode)
        startNode.isInOpenSet = True
        openSet.push(startNodeHeapObject)
        nodeObjectToHeapObject[startNode] = startNodeHeapObject

        while not openSet.checkIfEmpty():
            currentNode = openSet.pop().getNodeObject()
            currentNode.isInOpenSet = False
            del nodeObjectToHeapObject[currentNode]
            currentNode.isInClosedSet = True

            if (currentNode == goalNode):
                print("DONE")
                break

            #print("current = " + str(currentNode.x) + ", " + str(currentNode.y) + "; goal = " + str(goalNode.x) + ", " + str(goalNode.y))
            for n in self.getNeighbours(grid, currentNode):
                if not n.walkable or n.isInClosedSet:
                    continue

                newMovCostToNeighbour = currentNode.gCost + self.getDistance(currentNode, n)
                if newMovCostToNeighbour < n.gCost or not n.isInOpenSet:
                    visited.append(n)
                    n.gCost = newMovCostToNeighbour
                    n.hCost = self.getDistance(n, goalNode)
                    n.setParent(currentNode)


                    if n.isInOpenSet:
                        openSet.updateHeap(nodeObjectToHeapObject[n].index)
                    else:
                        n.isInOpenSet = True
                        addNodeHeapObject = NodeObjectWrapper(n)
                        openSet.push(addNodeHeapObject)
                        nodeObjectToHeapObject[n] = addNodeHeapObject


        visited = self.getCellsPath(visited)

        path = self.getCellsPath(self.retracePath(startNode, goalNode))
        print("path lenght = " + str(len(path)))
        toc = time.clock()
        print("time elapsed (run) = " + str(toc - tic))

        return visited, path

class AStarNoLists(AStar):
    NAME = "A*NoLists"

    def run(self):


        visited = []
        path = []

        openSet = []

        grid = self.createGrid(self.canvas)

        startNode = Node(self.canvas.grid[self.canvas.START[0]][self.canvas.START[1]], True, self.canvas.START[0],self.canvas.START[1])
        goalNode = Node(self.canvas.grid[self.canvas.GOAL[0]][self.canvas.GOAL[1]], True, self.canvas.GOAL[0],self.canvas.GOAL[1])

        grid[startNode.x][startNode.y] = startNode
        grid[goalNode.x][goalNode.y] = goalNode

        openSet.append(startNode)


        tic = time.clock()

        while(len(openSet) > 0):
            currentNode = openSet[0]
            for o in openSet:
                if o.fCost() < currentNode.fCost() or o.fCost() == currentNode.fCost() and o.hCost < currentNode.hCost:
                    currentNode = o

            openSet.remove(currentNode)
            currentNode.isInOpenSet = False
            currentNode.isInClosedSet = True

            if (currentNode == goalNode):
                print("DONE")
                break

            #print("current = " + str(currentNode.x) + ", " + str(currentNode.y) + "; goal = " + str(goalNode.x) + ", " + str(goalNode.y))
            for n in self.getNeighbours(grid, currentNode):
                if not n.walkable or n.isInClosedSet:
                    continue

                newMovCostToNeighbour = currentNode.gCost + self.getDistance(currentNode, n)
                if newMovCostToNeighbour < n.gCost or not n.isInOpenSet:
                    visited.append(n)
                    n.gCost = newMovCostToNeighbour
                    n.hCost = self.getDistance(n, goalNode)
                    n.setParent(currentNode)

                    if not n.isInOpenSet:
                        openSet.append(n)
                        n.isInOpenSet = True

        toc = time.clock()
        print("time elapsed (run) = " + str(toc - tic))
        path = self.getCellsPath(self.retracePath(startNode, goalNode))
        print("path lenght = " + str(len(path)))
        visited = self.getCellsPath(visited)


        return visited, path
