from graphic_components import Line, Point

class Cell():
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self._visited = False
    
    def draw(self, topLeft: Point, bottomRight: Point):
        self._x1 = topLeft.x
        self._x2 = bottomRight.x
        self._y1 = topLeft.y
        self._y2 = bottomRight.y

        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.drawLine(line)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.drawLine(line, "white")

        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.drawLine(line)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.drawLine(line, "white")
        
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.drawLine(line)
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.drawLine(line, "white")

        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.drawLine(line)
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.drawLine(line, "white")
    
    def drawMove(self, targetCell, undo: bool = False):
        color = "white" if undo else "red"
        centerOfOriginCell = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        centerOfTargetCell = Point((targetCell._x1 + targetCell._x2) // 2, (targetCell._y1 + targetCell._y2) // 2)
        self._win.drawLine(Line(centerOfOriginCell, centerOfTargetCell), color)
    
    # Draw half a move to better visualize the start and end of the maze solution
    def drawHalfMove(self, direction: str):
        center = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        if direction == 'top':
            self._win.drawLine(Line(center, Point(center.x, self._y1)), "red")
        elif direction == 'bottom':
            self._win.drawLine(Line(center, Point(center.x, self._y2)), "red")
        elif direction == 'left':
            self._win.drawLine(Line(center, Point(self._x1, center.y)), "red")
        elif direction == 'right':
            self._win.drawLine(Line(center, Point(self._x2, center.y)), "red")
       