import random
import time

from .cell import Cell
from .graphic_components import Window, Point


class Maze:
    def __init__(self, origin: Point, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int, win: Window = None,
                 seed: int = None):
        self.__origin = origin
        self.__numRows = num_rows
        self.__numCols = num_cols
        self.__cellSizeX = cell_size_x
        self.__cellSizeY = cell_size_y
        self._cells = None
        self._win = win
        self._seed = random.seed(seed) if seed else seed

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for _ in range(self.__numRows)] for _ in range(self.__numCols)]
        for i in range(self.__numRows):
            for j in range(self.__numCols):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int):
        if not self._win:
            return
        top_left = Point(self.__origin.x + j * self.__cellSizeX, self.__origin.y + i * self.__cellSizeY)
        bottom_right = Point(top_left.x + self.__cellSizeX, top_left.y + self.__cellSizeY)
        self._cells[i][j].draw(top_left, bottom_right)
        self._animate()

    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        time.sleep(0.005)

    def _break_wall(self, i: int, j: int, direction: str):
        top_left = Point(self.__origin.x + j * self.__cellSizeX, self.__origin.y + i * self.__cellSizeY)
        bottom_right = Point(top_left.x + self.__cellSizeX, top_left.y + self.__cellSizeY)
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
        self._cells[i][j].draw(top_left, bottom_right)

    def _break_entrance_and_exit(self):
        self._break_wall(0, 0, 'top')
        self._break_wall(self.__numRows - 1, self.__numCols - 1, 'bottom')
        self._win.redraw()

    def _break_walls_r(self, i: int, j: int):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []

            # Check if the cell has any unvisited neighbors
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            if i < self.__numRows - 1 and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if j < self.__numCols - 1 and not self._cells[i][j + 1].visited:
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

    def _reset_cells_visited(self):
        for i in range(self.__numRows):
            for j in range(self.__numCols):
                self._cells[i][j].visited = False

    def _solve_r(self, i: int, j: int):
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self.__numRows - 1 and j == self.__numCols - 1:
            return True

        # Move left if possible and it hasn't been visited
        if j > 0 and not self._cells[i][j - 1].visited and not current_cell.has_left_wall:
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j - 1], True)

        # Move right if possible and it hasn't been visited
        if j < self.__numCols - 1 and not self._cells[i][j + 1].visited and not current_cell.has_right_wall:
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j + 1], True)

        # Move up if possible and it hasn't been visited
        if i > 0 and not self._cells[i - 1][j].visited and not current_cell.has_top_wall:
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i - 1][j], True)

        # Move down if possible and it hasn't been visited
        if i < self.__numRows - 1 and not self._cells[i + 1][j].visited and not current_cell.has_bottom_wall:
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i + 1][j], True)

        return False

    # Check if the maze has been solved
    def did_solve(self):
        return self._solve_r(0, 0)

    # Solve the maze and add the start and end of the solution (half moves)
    def solve(self):
        self._cells[0][0].draw_half_move('top')
        self.did_solve()
        self._cells[self.__numRows - 1][self.__numCols - 1].draw_half_move('bottom')
