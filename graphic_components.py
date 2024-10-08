from tkinter import Tk, Canvas

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
    
    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill = fill_color, width = 2)


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.canvas.pack()
        self.__isRunning = False
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__isRunning = True
        while self.__isRunning:
            self.redraw()
    
    def close(self):
        self.__isRunning = False
    
    def draw_line(self, line: Line, fill_color: str  = "black"):
        line.draw(self.canvas, fill_color)

