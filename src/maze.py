import random
import time

from src.cell import Cell
from src.graphic_components import Window, Point


class Maze:
    def __init__(self, origin: Point, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int, win: Window = None, seed: int = None) -> None:
        self.origin: Point = origin
        self.numRows: int = num_rows
        self.numCols: int = num_cols
        self.__cellSizeX: int = cell_size_x
        self.__cellSizeY: int = cell_size_y
        self.cells: list[Cell] = []
        self.win: Window = win
        self._seed: int = random.seed(seed) if seed else seed

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        self.cells = [[Cell(self.win) for _ in range(self.numRows)] for _ in range(self.numCols)]
        for i in range(self.numRows):
            for j in range(self.numCols):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int) -> None:
        if not self.win:
            return
        top_left = Point(self.origin.x + j * self.__cellSizeX, self.origin.y + i * self.__cellSizeY)
        bottom_right = Point(top_left.x + self.__cellSizeX, top_left.y + self.__cellSizeY)
        self.cells[i][j].draw(top_left, bottom_right)
        self._animate()

    def _animate(self) -> None:
        if not self.win:
            return
        self.win.redraw()
        time.sleep(0.005)

    def _break_wall(self, i: int, j: int, direction: str) -> None:
        top_left = Point(self.origin.x + j * self.__cellSizeX, self.origin.y + i * self.__cellSizeY)
        bottom_right = Point(top_left.x + self.__cellSizeX, top_left.y + self.__cellSizeY)
        match direction:
            case 'top':
                self.cells[i][j].has_top_wall = False
            case 'bottom':
                self.cells[i][j].has_bottom_wall = False
            case 'left':
                self.cells[i][j].has_left_wall = False
            case 'right':
                self.cells[i][j].has_right_wall = False
            case _:
                pass
        self.cells[i][j].draw(top_left, bottom_right)

    def _break_entrance_and_exit(self) -> None:
        self._break_wall(0, 0, 'top')
        self._break_wall(self.numRows - 1, self.numCols - 1, 'bottom')
        self.win.redraw()

    def _break_walls_r(self, i: int, j: int) -> None:
        current_cell = self.cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []

            # Check if the cell has any unvisited neighbors
            if i > 0 and not self.cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            if i < self.numRows - 1 and not self.cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j > 0 and not self.cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if j < self.numCols - 1 and not self.cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            if not to_visit:
                return

            # Choose a random neighbor to visit and break the walls between the current cell and the neighbor
            next_cell = random.choice(to_visit)
            if next_cell[0] == i - 1:
                self._break_wall(i, j, 'top')
                self._break_wall(next_cell[0], next_cell[1], 'bottom')
            elif next_cell[0] == i + 1:
                self._break_wall(i, j, 'bottom')
                self._break_wall(next_cell[0], next_cell[1], 'top')
            elif next_cell[1] == j - 1:
                self._break_wall(i, j, 'left')
                self._break_wall(next_cell[0], next_cell[1], 'right')
            elif next_cell[1] == j + 1:
                self._break_wall(i, j, 'right')
                self._break_wall(next_cell[0], next_cell[1], 'left')

            # Recursively visit the neighbor
            self._break_walls_r(*next_cell)

    def _reset_cells_visited(self) -> None:
        for i in range(self.numRows):
            for j in range(self.numCols):
                self.cells[i][j].visited = False

    @staticmethod
    def solve(algorithm) -> None:
        algorithm.solve()
