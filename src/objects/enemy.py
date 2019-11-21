import random
import pygame
from src.objects.base_classes import DrawableObject
from src.objects.entity import Entity
from src.utils.vector import Vector, Point

class Enemy(Entity):

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__ (field, pos, size)
        self.speed_vector = self.new_target_direction()

        self.dist_from_center = 0
        self.groving = 1
        self.changed_block_counter = 0

    def new_target_direction(self):
        d_x = -1, 0, 1, 0
        d_y = 0, -1, 0, 1
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
        target_direction = possible_directions[direction_number]
        return target_direction

    def wall_colision(self, normalized_speed_vector, past_tile):
        self.dist_from_center += normalized_speed_vector.length * self.groving
        print (self.dist_from_center)
        if (self.dist_from_center > -0.000001) and (self.dist_from_center < 0.000001):
            self.changed_block_counter += 1
            if self.changed_block_counter == 2:
                self.changed_block_counter = 0
                self.speed_vector = self.new_target_direction ()
        if (self.tile != past_tile):
            self.dist_from_center -= normalized_speed_vector.length * self.groving
            self.groving *= -1

    def process_logic(self):
        past_tile = self.tile

        normalized_speed_vector = self.speed_vector.normalized * self.speed_value
        self.pos = self.pos + normalized_speed_vector

        self.wall_colision (normalized_speed_vector, past_tile)







