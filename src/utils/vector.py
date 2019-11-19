class Vector:
    """
    Класс двумерного вектора с координатами (x, y).
    Поддерживает некоторые базовые операции над векторами.
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def get(self):
        return self.x, self.y

    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** .5
    
    @property
    def copy(self):
        return Vector(self.x, self.y)
    
    def copy_from(self, vector):
        self.x, self.y = vector

    @property
    def normalized(self):
        ln = self.length
        if ln == 0:
            return Vector()
        return self.copy / ln

    def normalize(self):
        ln = self.length
        if ln == 0:
            return
        self.x /= ln
        self.y /= ln

    def __str__(self):
        return '{' + "{}; {}".format(*self.get) + '}'

    def __iter__(self):
        return self.get.__iter__()

    def __getitem__(self, key):
        return self.get[key]

    def __setitem__(self, key, value):
        if key not in (0, 1):
            raise KeyError
        if key == 0:
            self.x = value
        else:
            self.y = value

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        return self + (-vector)

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __truediv__(self, n):
        return Vector(self.x / n, self.y / n)

    def __bool__(self):
        return self.x != 0 or self.y != 0


Point = Vector
