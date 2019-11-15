import pygame
from src.objects.base_classes import DrawableObject
from src.objects.tiles import TILES
from src.utils.vector import Point
from src.utils.constants import Color

"""
В Field сосредоточена основная информация об игровых объектах.
grid - двумерный список для статичных объектов, 
остальное - entities.
"""


class Field(DrawableObject):
    LINE_WIDTH = 1

    def __init__(self, game_object, pos: Point, field_size: tuple, tile_size: tuple):
        super().__init__(game_object)

        self.pos = Point()
        self.pos.copy_from(pos)
        self.field_size = tuple(field_size)
        self.tile_size = tuple(tile_size)
        self.entities = []
        self.grid = [[]]

        self.grid_init()

    @property
    def size(self):
        return self.field_size

    @property
    def width(self):
        return self.field_size[0]

    @property
    def height(self):
        return self.field_size[1]

    def grid_init(self):
        """
        grid заполняется стенами через одну клетку
        0 - пустота, 1 - стена
        """
        # генерация двумерного списка, заполненного нулями:
        self.grid = [[0] * self.width for _ in range(self.height)]

        for i in range(0, self.width):
            self.grid[0][i] = 1
            self.grid[-1][i] = 1

        for j in range(0, self.height):
            self.grid[j][0] = 1
            self.grid[j][-1] = 1

        for i in range(2, self.height, 2):
            for j in range(2, self.width, 2):
                self.grid[i][j] = 1

    def process_draw_tiles(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                # TODO Временное решение:
                tile_pos = [self.pos[k] + (j, i)[k] * self.tile_size[k] for k in range(2)]
                rect = tile_pos, self.tile_size
                pygame.draw.rect(self.game_object.screen, TILES[self.grid[i][j]].color, rect, 0)
                pygame.draw.rect(self.game_object.screen, Color.BLACK, rect, Field.LINE_WIDTH)

    def process_draw_entities(self):
        for e in self.entities:
            e.process_draw()

    def process_draw(self):
        self.process_draw_tiles()
        self.process_draw_entities()

    def process_step(self):
        for e in self.entities:
            e.process_step()

    def process_event(self, event):
        for e in self.entities:
            e.process_event(event)
