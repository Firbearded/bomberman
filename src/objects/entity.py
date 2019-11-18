import pygame
from src.objects.base_classes import DrawableObject
from src.utils.vector import Vector, Point


class Entity(DrawableObject):
    SPEED_VALUE = 0.02

    def __init__(self, field, pos: Point, size: tuple = (1, 1)):
        super().__init__(field.game_object)
        self.field = field

        self.pos = Point()
        self.pos.copy_from(pos)
        self.size = tuple(size)

        self.enabled = True
        self.speed_vector = Vector()  # Просто напровление, куда мы двигаемся
        self.speed_value = Entity.SPEED_VALUE

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

    @property
    def tile(self):
        x, y = self.center
        return Point(int(x), int(y))

    @property
    def real_pos(self):
        x = self.field.pos[0] + self.x * self.field.tile_size[0]
        y = self.field.pos[1] + self.y * self.field.tile_size[1]
        return x, y

    @property
    def real_size(self):
        w = self.width * self.field.tile_size[0]
        h = self.height * self.field.tile_size[1]
        return w, h

    def process_logic(self):
        speed_vector = Vector()
        speed_vector.copy_from(self.speed_vector)

        self.pos = self.pos + (speed_vector.normalized * self.speed_value)

    def process_draw(self):
        pygame.draw.rect(self.game_object.screen, (0, 0, 0), (self.real_pos, self.real_size), 0)
