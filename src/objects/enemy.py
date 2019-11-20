import random
import pygame
from src.objects.base_classes import DrawableObject
from src.objects.entity import Entity
from src.utils.vector import Vector, Point

class Enemy(Entity):

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__ (field, pos, size)

    def new_target_direction(self):
        d_x = {-1, 0, 1, 0}
        d_y = {0, -1, 0, 1}
        possible_directions = []
        target_direction = Vector()
        tile_x, tile_y = self.tile
        for i in range(4):
            if (self.field.grid[d_y[i] + tile_y][d_x[i] + tile_x] == 0):
                d = Vector(d_x[i], d_y[i])
                possible_directions.append(d)
        if len(possible_directions) == 0:
            return target_direction

        direction_number = random.randint(1, len(possible_directions)) - 1
        target_direction.x = possible_directions[direction_number].x
        target_direction.y = possible_directions[direction_number].y
        return target_direction


    def process_logic(self):
        pass





