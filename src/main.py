from .graphic_components import Window, Point
from .maze import Maze
from src.algorithms import DFS

def main():
    spawn_maze()

def spawn_maze():
    window = Window(1000, 1000)

    maze = Maze(Point(100, 100), 16, 16, 50, 50, window)
    maze.solve(DFS(maze))

    window.wait_for_close()