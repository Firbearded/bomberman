from math import sqrt


def is_circles_intersect(pos1, radius1, pos2, radius2):
    """
    Функция, определяющая пересекаются ли две окружности,
    pos (x, y) - координаты цетров
    
    :param pos1: координаты цетра первой окружности
    :param radius1: радиус первой окружности
    :param pos2: координаты цетра второй окружности
    :param radius2: радиус второй окружности
    :return: пересекаются ли окружности
    :type pos1: Point
    :type radius1: float
    :type pos2: Point
    :type radius2: float
    :rtype: bool
    """
    return (pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 < (radius1 + radius2) ** 2


def is_close_enough(pos1, size1, pos2, size2):
    """
    Функция, определяющая пересекаются ли окружности с центрами в центрах прямоугольников
    и с радиусами, равными половине их диагоналей.
    pos (x, y) - координаты верхнего левого угла прямоугольника
    size (width, heigth) - размер прямоугольника
    
    :param pos1: координаты левого верхнего угла первого прямоугольника
    :param size1: размеры первого прямоугольника
    :param pos2: координаты левого верхнего угла второго прямоугольника
    :param size2: размеры второго прямоугольника
    :return: пересекаются ли
    :type pos1: Point
    :type size1: tuple
    :type pos2: Point
    :type size2: tuple
    :rtype: bool
    """
    w1, h1 = size1
    w2, h2 = size2
    radius1 = sqrt(w1 ** 2 + h1 ** 2) / 2
    radius2 = sqrt(w2 ** 2 + h2 ** 2) / 2
    return (pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 < (radius1 + radius2) ** 2


def is_collide_rect(pos1, size1, pos2, size2, can_touch=(True, True)):
    """
    Пересекаются или касаются ли два прямоугольника.
    pos (x, y) - координаты верхнего левого угла
    size (width, heigth) - размер прямоугольника

    :param can_touch: Могут ли они касаться по осям (Ox, Oy) соответсвтенно
    :param pos1: координаты левого верхнего угла первого прямоугольника
    :param size1: размеры первого прямоугольника
    :param pos2: координаты левого верхнего угла второго прямоугольника
    :param size2: размеры второго прямоугольника
    :return: пересекаются ли
    :type pos1: Point
    :type size1: tuple
    :type pos2: Point
    :type size2: tuple
    :rtype: bool
    """
    w1, h1 = size1
    w2, h2 = size2

    if not can_touch[0]:
        if pos1.x > pos2.x + w2 or pos2.x > pos1.x + w1:
            return False
    else:
        if pos1.x >= pos2.x + w2 or pos2.x >= pos1.x + w1:
            return False
    if not can_touch[1]:
        if pos1.y > pos2.y + h2 or pos2.y > pos1.y + h1:
            return False
    else:
        if pos1.y >= pos2.y + h2 or pos2.y >= pos1.y + h1:
            return False
    return True


def collide_rect(pos1, size1, pos2, size2):
    """
    Какие стороны первого прямоугольника пересекают стороны другого прямоугольника
    pos (x, y) - координаты верхнего левого угла прямоугольника
    size (width, heigth) - размер прямоугольника

    :param pos1: координаты левого верхнего угла первого прямоугольника
    :param size1: размеры первого прямоугольника
    :param pos2: координаты левого верхнего угла второго прямоугольника
    :param size2: размеры второго прямоугольника
    :return: (left, top, right, bottom) - пересекаются ли соответствующие стороны
    :type pos1: Point
    :type size1: tuple
    :type pos2: Point
    :type size2: tuple
    :rtype: tuple
    """
    w1, h1 = size1
    w2, h2 = size2

    if not is_collide_rect(pos1, size1, pos2, size2):
        return False, False, False, False,

    left = False
    top = False
    right = False
    bottom = False

    if pos2.x < pos1.x < pos2.x + w2:
        left = True
    if pos2.x < pos1.x + w1 < pos2.x + w2:
        right = True
    if pos2.y < pos1.y < pos2.y + h2:
        top = True
    if pos2.y < pos1.y + h1 < pos2.y + h2:
        bottom = True

    return left, top, right, bottom
