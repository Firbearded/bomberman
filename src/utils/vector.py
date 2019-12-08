from src.utils.functions import sign


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
        self._x, self._y = args

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)

    @property
    def get(self):
        """
        Кортеж из координат вектора
        :rtype: tuple
        """
        return self.x, self.y

    @property
    def copy(self):
        """
        Возвращает новый объект класса Vector с такими же координатами
        :rtype: Vector
        """
        return Vector(self.x, self.y)

    @property
    def length(self):
        """
        Длинна или модуль вектора.
        """
        return (self.x ** 2 + self.y ** 2) ** .5

    @length.setter
    def length(self, value):
        ln = self.length
        self._x /= ln
        self._y /= ln
        self._x *= float(value)
        self._y *= float(value)

    def changed_to(self, new_length):
        v = self.copy
        return (v / v.length) * new_length

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
        self._x = sign(self.x)
        self._y = sign(self.y)

    @staticmethod
    def dot_product(vector1, vector2):
        """ Скалярное произведение векторов """
        return vector1.x * vector2.x + vector1.y * vector2.y

    def __str__(self):
        return 'Vector{' + "{}; {}".format(*self.get) + '}'

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
        """
        :type other: Vector
        :rtype: bool
        """
        return tuple(self) == tuple(other)

    def __round__(self):
        return Vector(int(self.x), int(self.y))


Point = Vector
