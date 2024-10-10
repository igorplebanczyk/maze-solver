from src.dfs import DFS
from src.graphic_components import Window, Point
from src.maze import Maze


def main():
    window = Window(1000, 1000)
    maze = Maze(Point(100, 100), 16, 16, 50, 50, window)
    maze.solve(DFS(maze))
    window.wait_for_close()
