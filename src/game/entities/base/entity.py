import pygame

from src.game.base_classes.enableable_object import EnableableObject
from src.game.base_classes.geometric_object import GeometricObject
from src.game.base_classes.pygame_object import PygameObject
from src.game.base_classes.visible_object import VisibleObject
from src.game.supporting.constants import Color
from src.utils.animations import SimpleAnimation
from src.utils.decorators import protect
from src.utils.intersections import is_collide_rect
from src.utils.vector import Vector, Point


class Entity(PygameObject, GeometricObject, EnableableObject, VisibleObject):
    """
    Базовый класс для сущностей.
    Сущность всегда принадлежит какому-то полю.
    `animation` — специальный объект класса анимации. Нужен для хранения и переключения спрайтов.
    `speed_vector` — единичный вектор направления.
    `speed_value` — скорость (клеток в секунду)
    """
    SPEED_VALUE = 1  # клеток в секунду
    COLLISION_MODIFIER = .5  # процент от половины среднего арифметического размера —
    # — расстояние, на котором фиксируется столкновение между мобами и игроками
    COLOR = Color.BLACK   # Цвет объекта на запасную отрисовку (если проблемы с анимациями и спрайтами)

    SPRITE_CATEGORY = None  # Категория спрайтов
    SPRITE_NAMES = None     # tuple из названий спрайтов
    SPRITE_DELAY = None     # Задержка междку спрайтами
    # (Эти три переменные для упрощённых анимаций, состоящих из одной группы спрайтов, переключаемых по циклу.
    # Для более сложных анимаций надо писать самому)

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
        PygameObject.__init__(self, field_object.game_object)
        GeometricObject.__init__(self, pos, size)
        EnableableObject.__init__(self, True)
        VisibleObject.__init__(self, True)

        self.field_object = field_object
        field_object.add_entity(self)        # Сущность сама добавляется в поле

        self.speed_vector = Vector()         # Просто напровление, куда мы двигаемся
        self.speed_value = self.SPEED_VALUE  # Значение скорости (клеток в секунду)
        self.animation = None                # Объект класса анимаций

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
    def real_rect(self):
        x, y = self.real_pos
        w, h = self.real_size
        return x, y, w, h

    @property
    def real_speed_value(self):
        """
        Значение скорости, рассчитанное на данный момент
        (чтобы скорость не зависела от количества кадров в секунду, использовать это значение для рассчётов)
        :rtype: float
        """
        return self.speed_value * self.game_object.delta_time

    def destroy(self):
        """
        Уничтожение объекта.
        (деактивируем, делаем невидимым и удаляем из поля)
        """
        self.disable()
        self.hide()
        self.field_object.delete_entity(self)

    # ======================== Эвенты ========================
    def process_event(self, event):
        """ Если сущность активна, то проверяем события """
        if self.is_enabled:
            self.additional_event(event)

    def additional_event(self, event):
        """ Сюда писать проверку на события """
        pass

    # ======================== Логика ========================
    def process_logic(self):
        """
        Обработка логики:
        если есть анимации, то вызываем логику у анимации,
        если сущность активка, то вызываем дополнительную логику
        """
        if self.animation is not None:
            self.animation.process_logic()
        if self.is_enabled:
            self.additional_logic()

    def additional_logic(self):
        """ В этом методе писать логику для сущности """
        speed_vector = Vector(self.speed_vector)

        self.pos += (speed_vector.normalized * self.real_speed_value)

    # ======================= Отрисовка ======================
    def process_draw(self):
        """
        Отрисовка:  если сущность видна, то рисуем.
        Если есть анимации, то рисуем анимации,
        иначе — дополнительный метод отрисовки.
        """
        if not is_collide_rect(Point(0, 0), self.game_object.size, Point(self.real_pos), self.real_size):
            return
        if self.is_visible:
            if self.animation is not None:
                self.process_draw_animation()
            else:
                self.process_draw_reserve()

    @protect
    def create_animation(self):
        """ Метод для создания анимаций. """

        if not self.game_object.images: return
        if not self.SPRITE_CATEGORY: return
        if not self.SPRITE_NAMES: return
        if self.SPRITE_DELAY is None: return

        animation_dict = {}
        animation_delay = self.SPRITE_DELAY

        if len(self.SPRITE_NAMES) == 1:
            animation_delay = 0

        sprites = []

        w, h = self.real_size
        w, h = round(w), round(h)

        for sprite_name in self.SPRITE_NAMES:
            sprite = self.game_object.images[self.SPRITE_CATEGORY][sprite_name]
            sprite = pygame.transform.scale(sprite, (w, h))
            sprites.append(sprite)

        animation_dict['standard'] = animation_delay, sprites
        return SimpleAnimation(animation_dict, 'standard')

    def process_draw_animation(self):
        """ В этом методе писать отрисовку анимаций сущности. """
        self.game_object.screen.blit(self.animation.current_image, (self.real_pos, self.real_size))

    def process_draw_reserve(self):
        """ Метод запасной отрисовки. """
        pygame.draw.rect(self.game_object.screen, self.COLOR, self.real_rect, 0)
