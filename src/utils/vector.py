def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1


class Vector:
    """
    Класс двумерного вектора с координатами (x, y).
    Поддерживает некоторые базовые операции над векторами.
    """
    def __init__(self, *args):
        """
        В конструктор можно передавать:
        или итерируемый объект длинной 2,
        или две координаты,
        или ничего.

        Например,
        Vector(1, 2)      # Vector(1, 2)
        Vector([3, 4])    # Vector(3, 4)
        Vector()          # Vector(0, 0)
        Vector(Vector())  # Vector(0, 0)
        """
        if len(args) == 0:
            args = (0, 0)
        elif len(args) == 1:
            args = args[0]
        self.x, self.y = args

    @property
    def get(self):
        """
        Кортеж из координат вектора
        :rtype: tuple
        """
        return self.x, self.y

    @property
    def length(self):
        """
        Длинна или модуль вектора.
        """
        return (self.x ** 2 + self.y ** 2) ** .5
    
    @property
    def copy(self):
        """
        Возвращает новый объект класса Vector с такими же координатами
        :rtype: Vector
        """
        return Vector(self.x, self.y)

    @property
    def normalized(self):
        """
        Возвращает новый вектор, равный нормализированному от данного.
        :rtype: Vector
        """
        ln = self.length
        if ln == 0:
            return Vector()
        return self.copy / ln

    def normalize(self):
        """
        Нормализирует данный вектор
        :rtype: Vector
        """
        ln = self.length
        if ln == 0:
            return
        self.x /= ln
        self.y /= ln

    @property
    def united(self):
        """
        Возвращает единичный вектор (не с длинной 1, а с координатами -1, 0 или 1)
        :rtype: Vector
        """
        x = sign(self.x)
        y = sign(self.y)
        return Vector(x, y)

    def unit(self):
        """
        Делает данный вектор единичным (не с длинной 1, а с координатами -1, 0 или 1)
        :rtype: Vector
        """
        self.x = sign(self.x)
        self.y = sign(self.y)

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
        """
        :rtype: Vector
        """
        return Vector(-self.x, -self.y)

    def __add__(self, vector):
        """
        :type vector: Vector
        :rtype: Vector
        """
        return Vector(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        """
        :type vector: Vector
        :rtype: Vector
        """
        return self + (-vector)

    def __mul__(self, other):
        """
        :type other: float, Vector
        :rtype: Vector
        """
        if type(other) is Vector:
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, n):
        """
        :type n: float
        :rtype: Vector
        """
        return Vector(self.x / n, self.y / n)

    def __bool__(self):
        """
        :rtype: bool
        """
        return self.x != 0 or self.y != 0

    def __eq__(self, other):
        return self.get == other.get


Point = Vector
