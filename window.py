from tkinter import Tk, BOTH, Canvas
from draw import Line


class Window:
    def __init__(self, width: int, height: int):
        self._root = Tk()
        self._root.wm_title("Maze")
        self._canvas = Canvas(self._root, bg="black", height=height, width=width)
        self._canvas.pack(fill=BOTH, expand=1)
        self._running = False
        self._root.protocol("WM_DELETE_WINDOW", self._close)

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()

    def _close(self):
        self._running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self._canvas, fill_color)
