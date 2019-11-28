import pygame

from src.objects.base_classes.base_objects.enableable_object import EnableableObject
from src.objects.base_classes.base_objects.geometric_object import GeometricObject
from src.objects.base_classes.base_objects.pygame_object import PygameObject
from src.objects.base_classes.base_objects.visible_object import VisibleObject
from src.objects.supporting.animation import SimpleAnimation
from src.utils.constants import Color
from src.utils.decorators import protect
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
    COLLISION_MODIFIER = .5
    COLOR = Color.BLACK

    SPRITE_CATEGORY = None
    SPRITE_NAMES = None
    SPRITE_DELAY = None

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
        field_object.add_entity(self)

        self.speed_vector = Vector()  # Просто напровление, куда мы двигаемся
        self.speed_value = self.SPEED_VALUE
        self.animation = None

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
    def real_speed_value(self):
        return self.speed_value * self.game_object.delta_time

    def destroy(self):
        self.disable()
        self.hide()
        self.field_object.delete_entity(self)

    # ======================== Эвенты ========================
    def process_event(self, event):
        if self.is_enabled:
            self.additional_event(event)

    def additional_event(self, event):
        pass

    # ======================== Логика ========================
    def process_logic(self):
        if self.animation is not None:
            self.animation.process_logic()
        if self.is_enabled:
            self.additional_logic()

    def additional_logic(self):
        """ В этом методе писать логику для сущности. """
        speed_vector = Vector(self.speed_vector)

        self.pos += (speed_vector.normalized * self.real_speed_value)

    # ======================= Отрисовка ======================
    def process_draw(self):
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
        pygame.draw.rect(self.game_object.screen, self.COLOR, (self.real_pos, self.real_size), 0)
