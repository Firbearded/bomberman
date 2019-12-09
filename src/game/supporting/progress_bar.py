import pygame

from src.game.base_classes.pygame_object import PygameObject
from src.game.supporting.constants import Color
from src.utils.vector import Point


class ProgressBar(PygameObject):
    LINE_WIDTH = 1
    LINE_COLOR = Color.BLACK

    def __init__(self, game_object, pos, size, color1, color2, mn=0, mx=100, val=0, line_width=LINE_WIDTH, line_color=LINE_COLOR):
        super().__init__(game_object)

        self.pos = Point(pos)
        self.size = tuple(size)

        self.color1 = color1
        self.color2 = color2

        self.set_limit(mn, mx)
        self.set_value(val)
        self.line_width = line_width
        self.line_color = line_color

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
        if self.line_width > 0:
            pygame.draw.rect(self.game_object.screen, self.line_color, rect1, self.line_width)
