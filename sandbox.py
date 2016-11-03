from tkinter import *
import random
import time
from searchAlgorithms import *
import os


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
    color = ""

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False

    def _switch(self):
        """ Switch if the cell is OBSTACLE or not. """
        self.fill = not self.fill

    def draw(self, color):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None:
            fill = color
            outline = "black"
            self.color = color

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(
                xmin, ymin, xmax, ymax, fill=fill, outline=outline)


class CellGrid(Canvas):
    START = [0, 0]
    GOAL = [0, 0]
    SEARCH = None
    dirty = False

    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):

        self.START[0] = int(0.2 * columnNumber)
        self.START[1] = int(0.2 * columnNumber)
        self.GOAL[0] = int(rowNumber - 0.2 * rowNumber)
        self.GOAL[1] = int(rowNumber - 0.2 * rowNumber)

        Canvas.__init__(self, master, width=cellSize * columnNumber,
                        height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        # memorize the cells that have been modified to avoid many switching of
        # state during mouse motion.
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        # bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        # bind enter key to start
        self.bind("<Return>", self.handleEnter)

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
        # add the cell to the list of cell switched during the click
            self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched and self.isNotStartGoal(cell):
            cell._switch()
            cell.draw("black")
            self.switched.append(cell)


    def handleEnter(self, event):

        if self.dirty:
            print("cleaned")
            self.cleanGrid()
            self.dirty = False
        else:
            print(self.SEARCH.NAME + " ... processing")
            visited, path = self.SEARCH.run()
            for v in visited:
                if not v.fill and v.color != "pink":
                    v._switch()
                v.draw("pink")
                # self.update()
                # time.sleep(0.00015)
            for p in path:
                if not p.fill:
                    p._switch()
                p.draw("green")
                # self.update()
                # time.sleep(0.00015)

            cell = self.grid[self.START[0]][self.START[1]]
            cell.draw("blue")

            cell = self.grid[self.GOAL[0]][self.GOAL[1]]
            cell.draw("red")

            self.dirty = True

    def cleanGrid(self):
        for row in self.grid:
            for cell in row:
                if cell.color != "black" and cell.fill and self.isNotStartGoal(cell):
                    cell.fill = False
                    cell.draw("black")


    def setSearch(self, search):
        self.SEARCH = search(self)


class ImageGrid(CellGrid):
    SEARCH = ""
    START = [0, 0]
    GOAL = [0, 0]

    def __init__(self, master, cellSize, image, *args, **kwargs):
        img, imgx, imgy = ImageImport(image)

        rowNumber = imgx
        columnNumber = imgy

        Canvas.__init__(self, master, width=cellSize * columnNumber,
                        height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        # memorize the cells that have been modified to avoid many switching of
        # state during mouse motion.
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        # bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        # bind enter key to start
        self.bind("<Return>", self.handleEnter)

        self.draw(img)
        self.focus_set()

    def draw(self, img):
        i = 0
        for row in self.grid:
            for cell in row:
                if img[i] == "0" and img[i + 1] == "0" and img[i + 2] == "0":
                    cell._switch()
                    cell.draw("black")
                else:
                    if img[i] == "255" and img[i + 1] == "0" and img[i + 2] == "0":
                        cell._switch()
                        cell.draw("red")
                        self.GOAL = [cell.ord, cell.abs]
                    else:
                        if img[i] == "0" and img[i + 1] == "0" and img[i + 2] == "255":
                            cell._switch()
                            cell.draw("blue")
                            self.START = [cell.ord, cell.abs]
                        else:
                            cell.draw("black")
                i += 3


if __name__ == "__main__":
    app = Tk()

    grid = CellGrid(app, 50, 50, 20)
    # grid = ImageGrid(app, 9, "maze2.ppm")
    # grid.setSearch(AStarHeap)
    # grid.setSearch(AStar)
    grid.setSearch(AStarNoLists)
    grid.pack()

    app.mainloop()
