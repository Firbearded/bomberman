from random import randint

from src.objects.base_classes.entity import Entity
from src.objects.player import Player
from src.objects.tiles import TILES
from src.utils.constants import Color
from src.utils.vector import Point


class Enemy(Entity):
    SPEED_VALUE = .5
    SCORE = 100

    COLOR = Color.MAGENTA

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field, pos, size)

        self.target = self.new_target()
        self.speed_vector = self.new_target_direction()

    def new_target_direction(self):
        target_direction = self.target - self.pos

        return target_direction.united

    def new_target(self):
        dx = -1, 0, 1, 0
        dy = 0, -1, 0, 1

        possible_target = []

        tile_x, tile_y = self.tile
        for x, y in zip(dx, dy):
            if TILES[self.field_object.grid[y + tile_y][x + tile_x]].walkable:
                d = Point(x + tile_x, y + tile_y)
                possible_target.append(d)

        if not possible_target:
            return self.target

        rand_i = randint(0, len(possible_target) - 1)  # Получение случайного направления из
        target = possible_target[rand_i]  # массива возможных направлений
        return target

    def additional_logic(self):
        if self.target == self.pos or not self.speed_vector:
            self.target = self.new_target()
            self.speed_vector = self.new_target_direction()

        normalized_speed_vector = self.speed_vector.normalized * self.speed_value * self.game_object.delta_time
        new_pos = self.pos + normalized_speed_vector
        new_target_direction = (self.target - new_pos).united

        if self.speed_vector == new_target_direction:
            self.pos = new_pos
        else:
            self.pos = self.target
            if TILES[self.field_object.at(self.tile + self.speed_vector)].walkable:
                self.target += self.speed_vector
            else:
                self.target = self.new_target()
                self.speed_vector = self.new_target_direction()

        for e in self.field_object.entities:  # Проверка на коллизии и игроками
            if e.is_enabled:
                if type(e) is Player:
                    if self.tile == e.tile:
                        e.on_hurt(self)

    def on_hurt(self, from_enemy):
        from_enemy.bomb_object.player_object.score += self.SCORE
        self.destroy()
