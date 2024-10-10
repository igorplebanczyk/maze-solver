import time

from src.graphic_components import Point, Window
from src.maze import Maze
from src.cell import Cell

class DFS:
    def __init__(self, maze: Maze) -> None:
        self._maze: Maze = maze
        self._cells: list[Cell] = maze.cells
        self._numRows: int = maze.numRows
        self._numCols: int = maze.numCols
        self._origin: Point = maze.origin
        self._win: Window = maze.win

    def _animate(self) -> None:
        if not self._win:
            return

        self._win.redraw()
        time.sleep(0.005)

    def _solve_r(self, i: int, j: int) -> bool:
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self._numRows - 1 and j == self._numCols - 1:
            return True

        # Move left if possible and it hasn't been visited
        if j > 0 and not self._cells[i][j - 1].visited and not current_cell.has_left_wall:
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j - 1], True)

        # Move right if possible and it hasn't been visited
        if j < self._numCols - 1 and not self._cells[i][j + 1].visited and not current_cell.has_right_wall:
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
        if i < self._numRows - 1 and not self._cells[i + 1][j].visited and not current_cell.has_bottom_wall:
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i + 1][j], True)

        return False

    def solve(self) -> None:
        start_time = time.time()
        self._cells[0][0].draw_half_move('top')
        self._solve_r(0, 0)
        self._cells[self._numRows - 1][self._numCols - 1].draw_half_move('bottom')
        end_time = time.time()
        elapsed_time = end_time - start_time
        if self._win:
            self._win.display_time(elapsed_time)
