from time import sleep
from draw import Point, Line
import random


class Maze:
    def __init__(
        self,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        origin=Point(0, 0),
        win=None,
        seed=None,
        animate=True,
    ):
        if seed:
            random.seed(seed)
        self.animate = animate
        self._origin = origin
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self._draw_cells()

    def _create_cells(self):
        current_origin = self._origin

        for _ in range(self._num_cols):
            col = []
            for _ in range(self._num_rows):
                top_left = current_origin
                bottom_right = Point(
                    current_origin.x + self._cell_size_x,
                    current_origin.y + self._cell_size_y,
                )

                cell = Cell(top_left, bottom_right, self._win)
                col.append(cell)
                current_origin = Point(top_left.x, bottom_right.y)
            self._cells.append(col)

            current_origin = Point(bottom_right.x, self._origin.y)

    def _draw_cells(self):
        if self._win is None:
            return

        for col in self._cells:
            for cell in col:
                cell.draw()
                # self._maybe_animate()

    def _maybe_animate(self):
        if self.animate:
            self._win.redraw()
            sleep(0.05)

    def _break_entrance_and_exit(self):
        self.get_cell(0, 0).has_top_wall = False
        self.get_cell(-1, -1).has_bottom_wall = False

    def _break_walls_r(self, coli, celli):
        cell = self.get_cell(coli, celli)
        cell.visited = True
        while True:
            adjacent_unvisited = self.adjacent_unvisited(coli, celli)
            if not adjacent_unvisited:
                return
            rand = random.choice(adjacent_unvisited)
            random_cell = self.get_cell(rand)
            cell.remove_adjacent_walls(random_cell)
            self._break_walls_r(rand[0], rand[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, coli, celli):
        self._maybe_animate()
        cell = self.get_cell(coli, celli)
        cell.visited = True

        if cell == self.get_cell(-1, -1):
            return True

        adjacent_unvisited = self.adjacent_unvisited(coli, celli)
        for adj in adjacent_unvisited:
            adj_cell = self.get_cell(adj)
            if cell.can_move_to_cell(adj_cell):
                cell.draw_move(adj_cell)
                self._maybe_animate()
                is_solved = self._solve_r(adj[0], adj[1])
                if is_solved:
                    return True
                else:
                    adj_cell.draw_move(cell, True)

            next

    def get_cell(self, col=None, cell=None):
        try:
            if type(col) is list:
                return self.get_cell(col[0], col[1])

            if col == -1 and cell == -1:
                return self._cells[-1][-1]
            elif col >= 0 and cell >= 0:
                return self._cells[col][cell]
        except IndexError:
            return None
        return None

    def adjacent_unvisited(self, coli, celli):
        adj_unv = []
        possible_adj = [
            [coli + 1, celli],
            [coli - 1, celli],
            [coli, celli + 1],
            [coli, celli - 1],
        ]
        for pa in possible_adj:
            cell = self.get_cell(pa)
            if cell is not None and not cell.visited:
                adj_unv.append(pa)

        return adj_unv


class Cell:
    def __init__(self, top_left, bottom_right, win):
        self.visited = False
        self.top_left = top_left
        self.top_right = Point(bottom_right.x, top_left.y)
        self.bottom_right = bottom_right
        self.bottom_left = Point(top_left.x, bottom_right.y)
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.top_wall = Line(self.top_left, self.top_right)
        self.bottom_wall = Line(self.bottom_left, self.bottom_right)
        self.left_wall = Line(self.top_left, self.bottom_left)
        self.right_wall = Line(self.top_right, self.bottom_right)

    def draw(self, color: str = "white"):
        if self.has_left_wall:
            self._win.draw_line(self.left_wall, color)
        if self.has_right_wall:
            self._win.draw_line(self.right_wall, color)
        if self.has_top_wall:
            self._win.draw_line(self.top_wall, color)
        if self.has_bottom_wall:
            self._win.draw_line(self.bottom_wall, color)

    def remove_adjacent_walls(self, cell):
        if self.top_wall == cell.bottom_wall:
            self.has_top_wall = False
            cell.has_bottom_wall = False
        if self.bottom_wall == cell.top_wall:
            self.has_bottom_wall = False
            cell.has_top_wall = False
        if self.left_wall == cell.right_wall:
            self.has_left_wall = False
            cell.has_right_wall = False
        if self.right_wall == cell.left_wall:
            self.has_right_wall = False
            cell.has_left_wall = False

    def can_move_to_cell(self, cell):
        if self.top_wall == cell.bottom_wall and self.has_top_wall == False:
            return True
        if self.bottom_wall == cell.top_wall and self.has_bottom_wall == False:
            return True
        if self.left_wall == cell.right_wall and self.has_left_wall == False:
            return True
        if self.right_wall == cell.left_wall and self.has_right_wall == False:
            return True
        return False

    def center(self):
        x = self.bottom_left.x + (self.bottom_right.x - self.bottom_left.x) // 2
        y = self.top_right.y + (self.bottom_right.y - self.top_right.y) // 2

        return Point(x, y)

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "red"
        else:
            color = "gray"

        line = Line(self.center(), to_cell.center())
        self._win.draw_line(line, color)
