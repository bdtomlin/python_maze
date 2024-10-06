import unittest


from maze import Maze, Cell
from draw import Point
from window import Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_create_cells_with_origin(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(num_rows, num_cols, 10, 10, Point(5, 5))
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_reset_visited_cells(self):
        num_cols = 2
        num_rows = 2
        m1 = Maze(num_rows, num_cols, 10, 10, Point(5, 5))
        for col in m1._cells:
            for cell in col:
                cell.visited = True
        m1._reset_cells_visited()
        for col in m1._cells:
            for cell in col:
                self.assertFalse(cell.visited)

    def test_get_cell(self):
        num_cols = 2
        num_rows = 2
        m = Maze(num_rows, num_cols, 10, 10, Point(5, 5))
        self.assertEqual(m.get_cell(1, 1), m._cells[1][1])
        self.assertEqual(m.get_cell([1, 1]), m._cells[1][1])

    def test_solve(self):
        win = Window(1000, 1000)
        m = Maze(20, 20, 20, 20, Point(5, 5), win)
        m.solve()
        win.wait_for_close()

    def test_create_maze(self):
        win = Window(1000, 1000)
        Maze(20, 20, 20, 20, Point(5, 5), win)
        win.wait_for_close()
        win = Window(1000, 1000)
        Maze(40, 40, 20, 20, Point(5, 5), win)
        win.wait_for_close()

    def test_draw_move(self):
        win = Window(800, 600)
        cell1 = Cell(Point(5, 5), Point(20, 20), win)
        cell1.draw()
        cell2 = Cell(Point(21, 21), Point(40, 40), win)
        cell2.draw()
        cell1.draw_move(cell2, True)
        win.wait_for_close()

    def test_cell_drawing(self):
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


if __name__ == "__main__":
    unittest.main()
