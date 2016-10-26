from tkinter import *
import random

class ImageImport():
    def __init__(self):
        pass
    def __new__(self, file):
        file = open(file)
        lines = file.readlines()
        sizeX, sizeY, maxcolor = lines[1].split(" ", 3)
        return lines[2].split(" "), int(sizeX), int(sizeY)

class Cell():
    EMPTY_COLOR_BG = "white"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False

    def _switch(self):
        """ Switch if the cell is OBSTACLE or not. """
        self.fill= not self.fill

    def draw(self, color):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = color
            outline = color

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    START = [0,0]
    GOAL = [0,0]
    SEARCH = None
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):

        self.START[0] = int(0.2*columnNumber)
        self.START[1] = int(0.2*columnNumber)
        self.GOAL[0] = int(rowNumber - 0.2*rowNumber)
        self.GOAL[1] = int(rowNumber - 0.2*rowNumber)

        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        #bind enter key to start
        self.bind("<Return>",self.handleEnter)

        self.draw()
        self.focus_set()

        cell = self.grid[self.START[0]][self.START[1]]
        cell._switch()
        cell.draw("blue")

        cell = self.grid[self.GOAL[0]][self.GOAL[1]]
        cell._switch()
        cell.draw("red")



    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw("black")

    def isNotStartGoal(self, currentCell):
        if(currentCell.abs == self.START[1] and currentCell.ord == self.START[0]):
            return False
        else:
            if(currentCell.abs == self.GOAL[1] and currentCell.ord == self.GOAL[0]):
                return False
            else: 
                return True

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        if self.isNotStartGoal(cell):
            cell._switch()
            cell.draw("black")
        #add the cell to the list of cell switched during the click
            self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched and self.isNotStartGoal(cell):
            cell._switch()
            cell.draw("black")
            self.switched.append(cell)

    def handleEnter(self, event):
        print(self.SEARCH.NAME)
        visited, path = self.SEARCH.run()
        for v in visited:
            if not v.fill:
                v._switch()
            v.draw("pink")
        for p in path:
            if not p.fill:
                p._switch()
            p.draw("green")

        cell = self.grid[self.START[0]][self.START[1]]
        cell.draw("blue")

        cell = self.grid[self.GOAL[0]][self.GOAL[1]]
        cell.draw("red")  

    def setSearch(self, search):
        self.SEARCH = search(self)


class ImageGrid(CellGrid):
    SEARCH = ""
    START = [0,0]
    GOAL = [0,0]
    def __init__(self, master, cellSize, image, *args, **kwargs):
        img, imgx, imgy = ImageImport(image)

        rowNumber = imgx
        columnNumber = imgy

        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        #bind enter key to start
        self.bind("<Return>",self.handleEnter)

        self.draw(img)
        self.focus_set()

    def draw(self, img):
        i = 0
        for row in self.grid:
            for cell in row:
                if img[i] == "0" and img[i+1] == "0" and img[i+2] == "0":
                    cell._switch()
                    cell.draw("black")
                else:
                    if img[i] == "255" and img[i+1] == "0" and img[i+2] == "0":
                        cell._switch()
                        cell.draw("red")
                        self.GOAL = [cell.ord, cell.abs]
                    else:
                        if img[i] == "0" and img[i+1] == "0" and img[i+2] == "255":
                            cell._switch()
                            cell.draw("blue")
                            self.START = [cell.ord, cell.abs]
                        else:
                            cell.draw("black")
                i += 3
                

class DumbSearch():
    NAME = "Dumb Search"
    MODE = ""
    def __init__(self, grid):
        self.MODE = "NODIAG"

    def run(self):
        done = False
        start = grid.grid[grid.START[0]][grid.START[1]]
        goal = grid.grid[grid.GOAL[0]][grid.GOAL[1]]
        visited = []
        notAgain = []
        path = [start]

        cnt = 0

        while(not done):
            dist = 99999999
            tempN = start
            for n in self.getNeighbors(path[len(path) - 1]):
                d = self.sqDistance(n, goal)
                visited.append(n)
                if d <= dist  and n not in notAgain:
                    dist = d
                    tempN = n
            if tempN in path:
                notAgain.append(path[len(path) - 1])
                tempN = random.sample(self.getNeighbors(path[len(path)-1]),1)[0]
            path.append(tempN)
            print("path= "+str(tempN.abs)+","+str(tempN.ord))
            if tempN.abs == goal.abs and tempN.ord == goal.ord:
                done = True
                print("DONE")
            cnt += 1
        # print(len(path))
        path = self.cleanPath(path)
        # print(len(path))
        return visited, path

    def cleanPath(self, path):
        arr = []
        tempIDX = 0
        i = 0
        while i < len(path):
            tempIDX = i
            for j in range(len(path[i+1:])):
                if path[i] == path[i+1:][j]:
                    tempIDX = i + j + 1
            i = tempIDX
            arr.append(path[i])
            i += 1
        return arr



    def getObstacles(self):
        arr = []
        for row in grid.grid:
            for cell in row:
                if cell.fill and grid.isNotStartGoal(cell):
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
        return (xA- xB) * (xA- xB) + (yA - yB) * (yA - yB)

    def getNeighbors(self, point):
        arr = []
        x = point.abs
        y = point.ord
        xmax = len(grid.grid)
        ymax = len(grid.grid[0])

        obstacles = self.getObstacles()

        if self.MODE == "NODIAG":
            if x + 1 < xmax and self.isNotObstacle(obstacles, grid.grid[y][x+1]):
                 arr.append(grid.grid[y][x+1])
            if x - 1 >= 0 and self.isNotObstacle(obstacles, grid.grid[y][x-1]):
                 arr.append(grid.grid[y][x-1])
            if y - 1 >= 0 and self.isNotObstacle(obstacles, grid.grid[y-1][x]):
                 arr.append(grid.grid[y-1][x])
            if y + 1 < ymax and self.isNotObstacle(obstacles, grid.grid[y+1][x]):
                 arr.append(grid.grid[y+1][x])
        return arr

if __name__ == "__main__" :
    app = Tk()

    

    #grid = CellGrid(app, 50, 50, 20)
    grid = ImageGrid(app, 20, "img2.ppm")
    grid.setSearch(DumbSearch)
    grid.pack()

    app.mainloop()