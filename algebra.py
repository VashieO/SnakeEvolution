
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Vector(self.x, self.y)

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, o):
        return Vector(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vector(self.x - o.x, self.y - o.y)

    def __repr__(self):
        return str((self.x, self.y))
