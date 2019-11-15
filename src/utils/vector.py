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
        self.x = vector.x
        self.y = vector.y

    @property
    def normalized(self):
        return self.copy / self.length

    def normalize(self):
        l = self.length
        self.x /= l
        self.y /= l

    def __str__(self):
        return '{' + "{}; {}".format(*self.get) + '}'

    def __iter__(self):
        return self.get.__iter__()

    def __getitem__(self, item):
        return self.get[item]

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


Point = Vector
