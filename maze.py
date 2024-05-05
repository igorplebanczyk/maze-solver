from graphicComponents import Window, Line, Point
from cell import Cell
import time
import random

class Maze():
    def __init__(self, origin: Point, numRows: int, numCols: int, cellSizeX: int, cellSizeY: int, win: Window = None, seed: int = None):
        self.__origin = origin
        self.__numRows = numRows
        self.__numCols = numCols
        self.__cellSizeX = cellSizeX
        self.__cellSizeY = cellSizeY
        self._cells = None
        self._win = win
        self._seed = random.seed(seed) if seed else seed

        self._createCells()
        self._breakEntranceAndExit()
        self._breakWallsR(0, 0)
        self._resetCellsVisited()


    def _createCells(self):
        self._cells = [[Cell(self._win) for _ in range(self.__numRows)] for _ in range(self.__numCols)]
        for i in range(self.__numRows):
            for j in range(self.__numCols):
                self._drawCells(i, j)
    
    def _drawCells(self, i: int, j: int):
        if not self._win:
            return
        topLeft = Point(self.__origin.x + j * self.__cellSizeX, self.__origin.y + i * self.__cellSizeY)
        bottomRight = Point(topLeft.x + self.__cellSizeX, topLeft.y + self.__cellSizeY)
        self._cells[i][j].draw(topLeft, bottomRight)
        self._animate()
    
    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        time.sleep(0.005)

    def _breakWall(self, i: int, j: int, direction: str):
        topLeft = Point(self.__origin.x + j * self.__cellSizeX, self.__origin.y + i * self.__cellSizeY)
        bottomRight = Point(topLeft.x + self.__cellSizeX, topLeft.y + self.__cellSizeY)
        match direction:
            case 'top':
                self._cells[i][j].has_top_wall = False
            case 'bottom':
                self._cells[i][j].has_bottom_wall = False
            case 'left':
                self._cells[i][j].has_left_wall = False
            case 'right':
                self._cells[i][j].has_right_wall = False
            case _:
                pass
        self._cells[i][j].draw(topLeft, bottomRight)

    def _breakEntranceAndExit(self):
        self._breakWall(0, 0, 'top')
        self._breakWall(self.__numRows - 1, self.__numCols - 1, 'bottom')
        self._win.redraw()
    
    def _breakWallsR(self, i: int, j: int):
        currentCell = self._cells[i][j]
        currentCell._visited = True
        while True:
            toVisit = []

            # Check if the cell has any unvisited neighbors
            if i > 0 and not self._cells[i - 1][j]._visited:
                toVisit.append((i - 1, j))
            if i < self.__numRows - 1 and not self._cells[i + 1][j]._visited:
                toVisit.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1]._visited:
                toVisit.append((i, j - 1))
            if j < self.__numCols - 1 and not self._cells[i][j + 1]._visited:
                toVisit.append((i, j + 1))
            if not toVisit:
                return
            
            # Choose a random neighbor to visit and break the walls between the current cell and the neighbor
            nextCell = random.choice(toVisit)
            if nextCell[0] == i - 1:
                self._breakWall(i, j, 'top')
                self._breakWall(nextCell[0], nextCell[1], 'bottom')
            elif nextCell[0] == i + 1:
                self._breakWall(i, j, 'bottom')
                self._breakWall(nextCell[0], nextCell[1], 'top')
            elif nextCell[1] == j - 1:
                self._breakWall(i, j, 'left')
                self._breakWall(nextCell[0], nextCell[1], 'right')
            elif nextCell[1] == j + 1:
                self._breakWall(i, j, 'right')
                self._breakWall(nextCell[0], nextCell[1], 'left')
            
            # Recursively visit the neighbor
            self._breakWallsR(*nextCell)
    
    def _resetCellsVisited(self):
        for i in range(self.__numRows):
            for j in range(self.__numCols):
                self._cells[i][j]._visited = False

    def _solveR(self, i: int, j: int):
        self._animate()

        currentCell = self._cells[i][j]
        currentCell._visited = True
        if i == self.__numRows - 1 and j == self.__numCols - 1:
            return True

        # Move left if possible and it hasn't been visited
        if j > 0  and not self._cells[i][j - 1]._visited and not currentCell.has_left_wall:
            currentCell.drawMove(self._cells[i][j - 1])
            if self._solveR(i, j - 1):
                return True
            else:
                currentCell.drawMove(self._cells[i][j - 1], True)

        # Move right if possible and it hasn't been visited
        if j < self.__numCols - 1 and not self._cells[i][j + 1]._visited and not currentCell.has_right_wall:
            currentCell.drawMove(self._cells[i][j + 1])
            if self._solveR(i, j + 1):
                return True
            else:
                currentCell.drawMove(self._cells[i][j + 1], True)

        # Move up if possible and it hasn't been visited
        if i > 0 and not self._cells[i - 1][j]._visited and not currentCell.has_top_wall:
            currentCell.drawMove(self._cells[i - 1][j])
            if self._solveR(i - 1, j):
                return True
            else:
                currentCell.drawMove(self._cells[i - 1][j], True)

        # Move down if possible and it hasn't been visited
        if i < self.__numRows - 1 and not self._cells[i + 1][j]._visited and not currentCell.has_bottom_wall:
            currentCell.drawMove(self._cells[i + 1][j])
            if self._solveR(i + 1, j):
                return True
            else:
                currentCell.drawMove(self._cells[i + 1][j], True)

        return False

    # Check if the maze has been solved
    def didSolve(self):
        return self._solveR(0, 0)
    
    # Solve the maze and add the start and end of the solution (half moves)
    def solve(self):
        self._cells[0][0].drawHalfMove('top')
        self.didSolve()
        self._cells[self.__numRows - 1][self.__numCols - 1].drawHalfMove('bottom')