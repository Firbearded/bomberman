from random import randint

from src.objects.base_classes.entity import Entity
from src.objects.player import Player
from src.utils.constants import Color
from src.utils.intersections import is_circles_intersect
from src.utils.vector import Point


class Enemy(Entity):
    SPEED_VALUE = .5
    SCORE = 100

    SPRITE_CATEGORY = "enemy_sprites"
    SPRITE_DELAY = 500

    COLOR = Color.MAGENTA

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field, pos, size)

        self.target = self.new_target()
        self.speed_vector = self.new_target_direction()

        self.animation = self.create_animation()

    def new_target_direction(self):
        target_direction = self.target - self.pos

        return target_direction.united

    def new_target(self):
        dx = -1, 0, 1, 0
        dy = 0, -1, 0, 1

        possible_target = []

        tile_x, tile_y = self.tile
        for x, y in zip(dx, dy):
            if self.field_object.tile_at(x + tile_x, y + tile_y).walkable:
                d = Point(x + tile_x, y + tile_y)
                possible_target.append(d)

        if not possible_target:
            return self.tile

        rand_i = randint(0, len(possible_target) - 1)  # Получение случайного направления из
        target = possible_target[rand_i]  # массива возможных направлений
        return target

    def additional_logic(self):
        if self.target == self.pos or not self.speed_vector:
            self.target = self.new_target()
            self.speed_vector = self.new_target_direction()

        normalized_speed_vector = self.speed_vector.normalized * self.real_speed_value
        new_pos = self.pos + normalized_speed_vector
        new_target_direction = (self.target - new_pos).united

        if self.target != self.tile and not self.field_object.tile_at(self.target).walkable:
            self.speed_vector *= -1
            self.target = self.tile

        if self.speed_vector == new_target_direction:
            self.pos = new_pos
        else:
            self.pos = self.target
            if self.field_object.tile_at(self.tile + self.speed_vector).walkable:
                self.target += self.speed_vector
            else:
                self.target = self.new_target()
                self.speed_vector = self.new_target_direction()

        for e in self.field_object.get_entities(Player):  # Проверка на коллизии c игроками
            if e.is_enabled:
                r = (self.height + self.width) / 4 * self.COLLISION_MODIFIER
                r2 = (e.height + e.width) / 4 * self.COLLISION_MODIFIER
                if is_circles_intersect(self.pos, r, e.pos, r2):
                    e.hurt(self)

    def hurt(self, from_):
        from_.bomb_object.player_object.score += self.SCORE
        self.destroy()
