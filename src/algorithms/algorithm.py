import time
from src import Maze

class Algorithm:
    def __init__(self, maze: Maze):
        self._maze = maze
        self._cells = maze.cells
        self._numRows = maze.numRows
        self._numCols = maze.numCols
        self._origin = maze.origin
        self._win = maze.win

    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        time.sleep(0.005)

    def solve(self):
        raise NotImplementedError("Subclasses should implement this!")
