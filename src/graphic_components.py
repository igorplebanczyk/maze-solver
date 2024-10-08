from tkinter import Tk, Canvas, Label, TOP


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start: Point = start
        self.end: Point = end

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2)


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root: Tk = Tk()
        self.__root.title("Maze")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.time_label: Label = Label(self.__root, text="", font=("Helvetica", 16))
        self.time_label.pack(side=TOP)

        self.canvas: Canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.canvas.pack()

        self.__isRunning: bool = False

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__isRunning = True
        while self.__isRunning:
            self.redraw()

    def close(self) -> None:
        self.__isRunning = False

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        line.draw(self.canvas, fill_color)

    def display_time(self, elapsed_time: float) -> None:
        self.time_label.config(text=f"Time taken: {elapsed_time:.2f} seconds")
