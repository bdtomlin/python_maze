class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        if self.p1 == other.p1 and self.p2 == other.p2:
            return True
        if self.p1 == other.p2 and self.p2 == other.p1:
            return True
        return False

    def draw(self, canvas, fill_color):
        _ = canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=1
        )
