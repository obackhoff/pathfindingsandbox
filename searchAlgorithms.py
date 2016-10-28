from tkinter import *
import random
import time


class DumbSearch():
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
            for n in self.getNeighbors(path[len(path) - 1]):
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
                    self.getNeighbors(path[len(path) - 1]), 1)[0]
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

    def getNeighbors(self, point):
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
            for n in self.getNeighbors(path[len(path) - 1]):
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
                    self.getNeighbors(path[len(path) - 1]), 1)[0]
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
