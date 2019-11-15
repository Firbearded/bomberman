from math import sqrt


def is_circles_intersect(pos1, radius1, pos2, radius2):
    '''
    Функция, определяющая пересекаются ли две окружности
    pos(x, y) координаты цетров
    '''
    return (pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 <= (radius1 + radius2) ** 2


def is_close_enough(pos1, size1, pos2, size2):
    '''
    Функция, определяющая пересекаются ли окружности с центрами в центрах прямоугольников и с радиусами, равными половине их диагоналей
    pos (x, y) координаты верхнего левого угла
    size (width, heigth)
    '''
    radius1 = sqrt(size1.width ** 2 + size1.height ** 2) / 2
    radius2 = sqrt(size2.width ** 2 + size2.height ** 2) / 2
    return (pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 <= (radius1 + radius2) ** 2


def is_collide_rect(pos1, size1, pos2, size2):
    '''
    Пересекаются или касаются ли два прямоугольника
    pos (x, y) координаты верхнего левого угла
    size (width, heigth)
    '''
    tmp1 = False
    if pos1.x <= pos2.x and pos1.x + size1.width >= pos2.x and pos1.x + size1.width <= pos2.x + size2.width:
        tmp1 = True
    if pos1.x >= pos2.x and pos1.x <= pos2.x + size2.width and pos1.x + size1.width >= pos2.x + size2.width:
        tmp1 = True
    if pos1.y <= pos2.y and pos1.y + size1.height >= pos2.y and pos1.y + size1.height <= pos2.y + size2.height:
        tmp1 = True
    if pos1.y >= pos2.y and pos1.y <= pos2.y + size2.height and pos1.y + size1.height >= pos2.y +size2.height:
        tmp1 = True
    return tmp1


def collide_rect(pos1, size1, pos2, size2):
    '''
    Какие стороны первого прямоугольника пересекаются или касаются другого прямоугольника
    pos (x, y) координаты верхнего левого угла прямоугольника
    size (width, heigth)
    '''
    tmp1 = False
    if pos1.x <= pos2.x and pos1.x + size1.width >= pos2.x and pos1.x + size1.width <= pos2.x + size2.width:
        tmp1 = True
    if pos1.x >= pos2.x and pos1.x <= pos2.x + size2.width and pos1.x + size1.width >= pos2.x + size2.width:
        tmp1 = True
    if pos1.y <= pos2.y and pos1.y + size1.height >= pos2.y and pos1.y + size1.height <= pos2.y + size2.height:
        tmp1 = True
    if pos1.y >= pos2.y and pos1.y <= pos2.y + size2.height and pos1.y + size1.height >= pos2.y + size2.height:
        tmp1 = True
    top = False
    bottom = False
    left = False
    right = False
    if tmp1:
        if pos1.x >= pos2.x and pos1.x <= pos2.x + size2.width:
            left = True
        if pos1.x + size1.width >= pos2.x and pos1.x + size1.width <= pos2.x + size2.width:
            right = True
        if pos1.y >= pos2.y and pos1.y <= size2.height:
            top = True
        if pos1.y + size1.height >= pos2.y and pos1.y + size1.height <= size2.height:
            bottom = True
    l = (left, top, right, bottom)
    return tuple(l,)
