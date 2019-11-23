import pygame

from src.objects.base_classes.drawable_object import DrawableObject
from src.utils.constants import Color
from src.utils.vector import Point


class ProgressBar(DrawableObject):
    LINE_WIDTH = 1
    LINE_COLOR = Color.BLACK

    def __init__(self, game_object, pos, size, color1, color2, mn=0, mx=100, val=0):
        super().__init__(game_object)

        self.pos = Point(pos)
        self.size = tuple(size)

        self.color1 = color1
        self.color2 = color2

        self.set_limit(mn, mx)
        self.set_value(val)

    @property
    def is_empty(self):
        return self.value <= self.min_value

    @property
    def is_full(self):
        return self.value >= self.max_value

    def set_value(self, val):
        self.value = max(min(val, self.max_value), self.min_value)

    def add_value(self, val):
        self.value = max(min(self.value + val, self.max_value), self.min_value)

    def set_limit(self, mn=None, mx=None):
        if mn is None:
            mn = self.min_value
        if mx is None:
            mx = self.max_value

        if mn > mx:
            mn, mx = mx, mn

        self.min_value = mn
        self.max_value = mx

    def process_draw(self):
        rect1 = tuple(self.pos), self.size

        w, h = self.size
        w = self.value * w / self.max_value
        rect2 = tuple(self.pos), (w, h)

        pygame.draw.rect(self.game_object.screen, self.color1, rect1)
        pygame.draw.rect(self.game_object.screen, self.color2, rect2)
        if self.LINE_WIDTH > 0:
            pygame.draw.rect(self.game_object.screen, self.LINE_COLOR, rect1, self.LINE_WIDTH)
