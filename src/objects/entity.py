import pygame

from src.objects.base_classes import DrawableObject
from src.utils.constants import Color
from src.utils.vector import Vector, Point


class Entity(DrawableObject):
    """
    Базовый класс для сущностей.
    Сущность всегда принадлежит какому-то полю.
    `enabled` — активна ли эта сущность. Если нет, то она не рисуется и ни на что не реагирует.
    `animation` — специальный объект класса анимации. Нужен для хранения и переключения спрайтов.
    `speed_vector` — единичный вектор направления.
    `speed_value` — скорость (клеток в секунду)
    """
    SPEED_VALUE = 1  # клеток в секунду
    COLOR = Color.BLACK

    # необходимо ли методам (event, logic, draw), чтобы self.enabled был включён
    NEED_ENABLED = 1, 1, 0

    def __init__(self, field_object, pos: Point, size: tuple = (1, 1)):
        """
        Конструктор класса `сущности`.

        :param field_object: объект поля, к которому принадлежит эта сущность
        :param pos: координаты сущности на поле (в клетах)
        :param size: размер сущности на поле (в клетах)
        :type field_object: Field
        :type pos: Point
        :type size: tuple
        """
        super().__init__(field_object.game_object)
        self.field_object = field_object
        field_object.add_entity(self)

        self.pos = Point(pos)
        self.size = tuple(size)

        self.enabled = True
        self.speed_vector = Vector()  # Просто напровление, куда мы двигаемся
        self.speed_value = self.SPEED_VALUE
        self.animation = None

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def left(self):
        """
        Лево сущности.
        :rtype: float
        """
        return self.x

    @property
    def top(self):
        """
        Верх сущности.
        :rtype: float
        """
        return self.y

    @property
    def right(self):
        """
        Право сущности.
        :rtype: float
        """
        return self.left + self.width

    @property
    def bottom(self):
        """
        Низ сущности.
        :rtype: float
        """
        return self.top + self.height

    @property
    def center(self):
        """
        Центр сущности.
        :rtype: Point
        """
        return Point(self.left + self.width / 2, self.top + self.height / 2)

    @property
    def tile(self):
        """
        Клетка поля, в которой находится эта сущность.
        :rtype: Point
        """
        x, y = self.center
        return Point(int(x), int(y))

    @property
    def real_pos(self):
        """
        Реальные координаты сущности на экране (в пикселях)
        :rtype: tuple
        """
        x = self.field_object.pos[0] + self.x * self.field_object.tile_size[0]
        y = self.field_object.pos[1] + self.y * self.field_object.tile_size[1]
        return x, y

    @property
    def real_size(self):
        """
        Реальные размеры сущности на экране (в пикселях)
        :rtype: tuple
        """
        w = self.width * self.field_object.tile_size[0]
        h = self.height * self.field_object.tile_size[1]
        return w, h

    @property
    def is_enabled(self):
        """
        Активна ли сущность в данный момент.
        :rtype: bool
        """
        return self.enabled

    @property
    def is_disabled(self):
        """
        Не активна ли сущность в данный момент.
        :rtype: bool
        """
        return not self.enabled

    def enable(self):
        """
        Активировать сущность
        """
        self.enabled = True

    def disable(self):
        """
        Деактивировать сущность
        """
        self.enabled = False

    def toggle(self):
        """
        Переключить состояние сущности на противоположное
        """
        self.enabled = not self.enabled

    def set_enabled(self, b):
        """
        Устаносить состояние сущности.
        :param b: Состояние сущности
        :type b: bool
        """
        self.enabled = bool(b)

    def destroy(self):
        self.disable()
        self.field_object.delete_entity(self)

    def create_animation(self):
        """
        Метод для создания анимаций.
        """
        pass

    def additional_event(self, event):
        pass

    def additional_logic(self):
        """
        В этом методе писать логику для сущности.
        """
        speed_vector = Vector(self.speed_vector)

        self.pos = self.pos + (speed_vector.normalized * self.speed_value)

    def process_draw_animation(self):
        """
        В этом методе писать отрисовку анимаций сущности.
        """
        self.game_object.screen.blit(self.animation.current_image, (self.real_pos, self.real_size))

    def process_draw_reserve(self):
        """
        Метод запасной отрисовки.
        """
        pygame.draw.rect(self.game_object.screen, self.COLOR, (self.real_pos, self.real_size), 0)

    def process_event(self, event):
        if not (self.NEED_ENABLED[0] and self.is_disabled):
            self.additional_event(event)

    def process_logic(self):
        if not (self.NEED_ENABLED[1] and self.is_disabled):
            if self.animation is not None:
                self.animation.process_logic()
            self.additional_logic()

    def process_draw(self):
        if not (self.NEED_ENABLED[2] and self.is_disabled):
            if self.animation is not None:
                self.process_draw_animation()
            else:
                self.process_draw_reserve()
