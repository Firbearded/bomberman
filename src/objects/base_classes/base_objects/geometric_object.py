from src.utils.vector import Point


class GeometricObject(object):
    def __init__(self, pos: Point = Point(), size: tuple = (1, 1)):
        self._pos = Point(pos)
        self._size = tuple(size)

    @property
    def pos(self):
        return Point(self._pos)

    @pos.setter
    def pos(self, value):
        self._pos = Point(value)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = tuple(value)

    @property
    def x(self):
        return self._pos[0]

    @x.setter
    def x(self, value):
        self._pos[0] = float(value)

    @property
    def y(self):
        return self._pos[1]

    @y.setter
    def y(self, value):
        self._pos[1] = float(value)

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    @width.setter
    def width(self, value):
        self._size = float(value), self.height

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def center(self):
        return Point(self.left + self.width / 2, self.top + self.height / 2)

    @center.setter
    def center(self, pos):
        x, y = pos
        self._pos = Point(x - self.width / 2, y - self.height / 2)
