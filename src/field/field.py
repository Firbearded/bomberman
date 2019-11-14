import pygame
from src.base_classes import DrawableObject
from src.field.tiles import TILES
from src.supporting_classes.tuple import Tuple
from src.supporting_classes.vector import Vector
from src.constants import Color

'''
В Field сосредоточена основная информация об игровых объектах.
grid - двумерный список для статичных объектов, 
остальное - entities.
'''

class Field(DrawableObject):
    def __init__(self, game_object, pos: Vector, field_size: Tuple, tile_size: Tuple):
        super().__init__(game_object)
        self.pos = pos
        self.field_size = field_size
        self.tile_size = tile_size
        self.fill_grid()
        self.entities = []

    def fill_grid(self):
        '''
        grid заполняется стенами через одну клетку
        0 - пустота, 1 - стена
        '''
        # генерация двумерного списка, заполненного нулями:
        self.grid = [[0] * self.field_size.w for i in range(self.field_size.h)]

        for i in range(1, self.field_size.h, 2):
            for j in range(1, self.field_size.w, 2):
                self.grid[i][j] = 1

    def process_draw_tiles(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                # Временное решение:
                tile_x = self.pos.x + j * self.tile_size.w
                tile_y = self.pos.y + i * self.tile_size.h
                pygame.draw.rect(self.game_object.screen, Color.GREEN,
                    (tile_x, tile_y,
                     self.tile_size.w, self.tile_size.h),
                    TILES[self.grid[i][j]].line_width)

    def process_draw_entities(self):
        for i in range(len(self.entities)):
            self.entities[i].process_draw()

    def process_draw(self):
        self.process_draw_tiles()
        self.process_draw_entities()

    def process_step(self):
        for i in range(len(self.entities)):
            self.entities[i].process_step()


