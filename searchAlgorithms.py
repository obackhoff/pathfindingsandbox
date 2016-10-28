from tkinter import *
import random
import time
from node import *

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

        st = SearchTools()
        obstacles = st.getObstacles(self.canvas)

        for i in range(len(canvas.grid)):
            temp = []
            for j in range(len(canvas.grid[0])):
                walkable = False
                if st.isNotObstacle(obstacles, canvas.grid[i][j]):
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
        done = False
        start = self.canvas.grid[self.canvas.START[0]][self.canvas.START[1]]
        goal = self.canvas.grid[self.canvas.GOAL[0]][self.canvas.GOAL[1]]
        visited = []
        notAgain = []
        path = [start]

        cnt = 0
        tic = time.clock()
        while(not done):
            dist = 99999999
            tempN = start
            for n in self.getNeighbours(path[len(path) - 1]):
                d = self.sqDistance(n, goal)
                visited.append(n)
                if d <= dist and n not in notAgain:
                    dist = d
                    tempN = n
                    # if d == dist:
                    #     if random.randint(0,1): tempN = n
                    # else:
                    #     tempN = n
            if tempN in path:
                notAgain.append(path[len(path) - 1])
                tempN = random.sample(
                    self.getNeighbours(path[len(path) - 1]), 1)[0]
            path.append(tempN)
            #print("path= "+str(tempN.abs)+","+str(tempN.ord))
            if tempN.abs == goal.abs and tempN.ord == goal.ord:
                done = True
                print("DONE")
            cnt += 1
        # print(len(path))
        toc = time.clock()
        print("time elapsed (run) = " + str(toc - tic))

        print("path before = " + str(len(path)))
        tic = time.clock()
        path = self.cleanPath(path)
        toc = time.clock()
        print("time elapsed (clean) = " + str(toc - tic))
        print("path clean = " + str(len(path)))
        # print(len(path))
        return visited, path

    def cleanPath(self, path):
        arr = []
        tempIDX = 0
        i = 0
        while i < len(path):
            tempIDX = i
            for j in range(len(path[i + 1:])):
                if path[i] == path[i + 1:][j]:
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

        obstacles = self.getObstacles()

        if self.MODE == "NODIAG":
            if x + 1 < xmax and self.isNotObstacle(obstacles, self.canvas.grid[y][x + 1]):
                arr.append(self.canvas.grid[y][x + 1])
            if x - 1 >= 0 and self.isNotObstacle(obstacles, self.canvas.grid[y][x - 1]):
                arr.append(self.canvas.grid[y][x - 1])
            if y - 1 >= 0 and self.isNotObstacle(obstacles, self.canvas.grid[y - 1][x]):
                arr.append(self.canvas.grid[y - 1][x])
            if y + 1 < ymax and self.isNotObstacle(obstacles, self.canvas.grid[y + 1][x]):
                arr.append(self.canvas.grid[y + 1][x])
        return arr


class DumbSearch2(DumbSearch):
    NAME = "Dumb Search Experiments"
    MODE = ""
    canvas = None

    def __init__(self, canvas):
        self.MODE = "NODIAG"
        self.canvas = canvas

    def run(self):
        done = False
        start = self.canvas.grid[self.canvas.START[0]][self.canvas.START[1]]
        goal = self.canvas.grid[self.canvas.GOAL[0]][self.canvas.GOAL[1]]
        visited = []
        notAgain = []
        path = [start]

        cnt = 0
        tic = time.clock()
        while(not done):
            dist = 99999999
            tempN = start
            for n in self.getNeighbours(path[len(path) - 1]):
                d = self.sqDistance(n, goal)
                visited.append(n)
                if d <= dist and n not in notAgain:
                    dist = d
                    # tempN = n
                    if d == dist:
                        if random.randint(0, 1):
                            tempN = n
                    else:
                        tempN = n
            if tempN in path:
                notAgain.append(path[len(path) - 1])
                tempN = random.sample(
                    self.getNeighbours(path[len(path) - 1]), 1)[0]
            path.append(tempN)
            # print("path= " + str(tempN.abs) + "," + str(tempN.ord))
            if tempN.abs == goal.abs and tempN.ord == goal.ord:
                done = True
                print("DONE")
            cnt += 1
        # print(len(path))
        toc = time.clock()
        print("time elapsed (run) = " + str(toc - tic))

        print("path before = " + str(len(path)))
        tic = time.clock()
        path = self.cleanPath(path)
        toc = time.clock()
        print("time elapsed (clean) = " + str(toc - tic))
        print("path clean = " + str(len(path)))
        # print(len(path))
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
        obstacles = self.getObstacles()

        for x in range(-1,2):
            for y in range(-1,2):
                if x == 0 and y == 0:
                    continue

                checkX = point.ord + x
                checkY = point.abs + y

                if checkX >= 0 and checkX < xmax and checkY >=0 and checkY < ymax:
                    if self.canvas.grid[checkX][checkY] not in obstacles:
                        neighbours.append(self.canvas.grid[checkX][checkY])
        return neighbours


