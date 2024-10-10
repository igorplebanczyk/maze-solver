from src.graphic_components import Line, Point, Window


class Cell:
    def __init__(self, win: Window) -> None:
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.x1: int = -1
        self.x2: int = -1
        self.y1: int = -1
        self.y2: int = -1
        self._win: Window = win
        self.visited: bool = False

    def draw(self, top_left: Point, bottom_right: Point) -> None:
        self.x1 = top_left.x
        self.x2 = bottom_right.x
        self.y1 = top_left.y
        self.y2 = bottom_right.y

        if self.has_left_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self._win.draw_line(line, "white")

        if self.has_top_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self._win.draw_line(line, "white")

        if self.has_right_wall:
            line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self._win.draw_line(line, "white")

        if self.has_bottom_wall:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self._win.draw_line(line, "white")

    def draw_move(self, target_cell, undo: bool = False) -> None:
        color = "white" if undo else "red"
        center_of_origin_cell = Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        center_of_target_cell = Point((target_cell.x1 + target_cell.x2) // 2, (target_cell.y1 + target_cell.y2) // 2)
        self._win.draw_line(Line(center_of_origin_cell, center_of_target_cell), color)

    # Draw half a move to better visualize the start and end of the maze solution
    def draw_half_move(self, direction: str) -> None:
        center = Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        if direction == 'top':
            self._win.draw_line(Line(center, Point(center.x, self.y1)), "red")
        elif direction == 'bottom':
            self._win.draw_line(Line(center, Point(center.x, self.y2)), "red")
        elif direction == 'left':
            self._win.draw_line(Line(center, Point(self.x1, center.y)), "red")
        elif direction == 'right':
            self._win.draw_line(Line(center, Point(self.x2, center.y)), "red")
