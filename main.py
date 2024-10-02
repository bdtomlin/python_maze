from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        _ = canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.wm_title("Maze")
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(self, top_left: Point, bottom_right: Point, win: Window):
        self._top_left = top_left
        self._top_right = Point(bottom_right.x, top_left.y)
        self._bottom_right = bottom_right
        self._bottom_left = Point(top_left.x, bottom_right.y)
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self, color: str = "white"):
        if self.has_left_wall:
            line = Line(self._top_left, self._bottom_left)
            self._win.draw_line(line, color)
        if self.has_right_wall:
            line = Line(self._top_right, self._bottom_right)
            self._win.draw_line(line, color)
        if self.has_top_wall:
            line = Line(self._top_right, self._top_left)
            self._win.draw_line(line, color)
        if self.has_bottom_wall:
            line = Line(self._bottom_right, self._bottom_left)
            self._win.draw_line(line, color)

    def center(self):
        x = self._bottom_left.x + (self._bottom_right.x - self._bottom_left.x) // 2
        y = self._top_right.y + (self._bottom_right.y - self._top_right.y) // 2

        return Point(x, y)

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"

        line = Line(self.center(), to_cell.center())
        self._win.draw_line(line, color)

# class Maze():


def main():
    # test_cell_drawing()
    # test_draw_move()


def test_draw_move():
    win = Window(800, 600)
    cell1 = Cell(Point(5, 5), Point(20, 20), win)
    cell1.draw()
    cell2 = Cell(Point(21, 21), Point(40, 40), win)
    cell2.draw()
    cell1.draw_move(cell2, True)
    win.wait_for_close()


def test_cell_drawing():
    win = Window(800, 600)
    point_groups = [
        {
            "tl": [5, 5],
            "br": [20, 20],
            "color": "red",
            "left": True,
            "right": True,
            "top": False,
            "bottom": True,
        },
        {
            "tl": [21, 21],
            "br": [40, 40],
            "color": "blue",
            "left": False,
            "right": False,
            "top": True,
            "bottom": True,
        },
        {
            "tl": [41, 41],
            "br": [80, 80],
            "color": "green",
            "left": True,
            "right": True,
            "top": True,
            "bottom": False,
        },
    ]
    for p in point_groups:
        tlx, tly = p["tl"]
        brx, bry = p["br"]
        top_left = Point(tlx, tly)
        bottom_right = Point(brx, bry)
        cell = Cell(top_left, bottom_right, win)
        cell.has_top_wall = p["top"]
        cell.has_bottom_wall = p["bottom"]
        cell.has_left_wall = p["left"]
        cell.has_right_wall = p["right"]
        cell.draw(p["color"])
    win.wait_for_close()


main()
