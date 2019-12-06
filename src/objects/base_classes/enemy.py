from random import random, choice

from src.objects.base_classes.entity import Entity
from src.objects.player import Player
from src.utils.constants import Color
from src.utils.intersections import is_circles_intersect
from src.utils.vector import Point, Vector


class Enemy(Entity):
    """ Класс мобов """
    SPEED_VALUE = .5  # Скорость моба
    SCORE = 100  # Очки, выпадаемые с моба
    CHANCE_TURN_ASIDE = 0.2  # Вероятность поворота в сторону
    CHANCE_TURN_BACK = 0.03  # Вероятность разворота

    delta = [Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]
    SPRITE_CATEGORY = "enemy_sprites"
    SPRITE_DELAY = 500
    COLOR = Color.MAGENTA

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field, pos, size)

        self.target = None  # Цель моба - соседняя клетка, в которую он переходит
        self.direction = None  # Направление движения моба

        self.animation = self.create_animation()

    def can_walk_at(self, tile):
        """ Может ли моб ходить по клетке tile? """
        return self.field_object.tile_at(tile).walkable

    def dot_product(self, vector1, vector2):
        """ Скалярное произведение векторов """
        return vector1.x * vector2.x + vector1.y * vector2.y

    def get_new_target(self):
        """ Обновление цели моба """
        # Если можем продолжить движение, меняем направление с некоторой вероятностью
        if self.direction and self.can_walk_at(self.tile + self.direction):
            # Пробуем развернуться
            if self.can_walk_at(self.tile - self.direction) and random() < self.CHANCE_TURN_BACK:
                self.direction = -self.direction
            else:
                # Пробуем повернуть в стороны
                if random() < self.CHANCE_TURN_ASIDE:
                    perpendicular = Vector(self.direction.y, -self.direction.x)
                    possible_targets = []
                    if self.can_walk_at(self.tile + perpendicular):
                        possible_targets.append(perpendicular)
                    if self.can_walk_at(self.tile - perpendicular):
                        possible_targets.append(-perpendicular)
                    if possible_targets:
                        self.direction = choice(possible_targets)
            return self.tile + self.direction
        # Выбор одного из доступных направлений
        possible_targets = []
        for v in self.delta:
            if self.can_walk_at(self.tile + v):
                possible_targets.append(self.tile + v)
        if not possible_targets:
            return None
        return choice(possible_targets)

    def update_target_and_direction(self):
        """ Обновление цели и направления (вызов получения цели и вычисление направления) """
        self.target = self.get_new_target()
        self.direction = self.target - self.tile if self.target else None

    def move(self):
        """ Движение моба """
        # Если нет цели, пробуем ее найти
        if not self.target:
            self.update_target_and_direction()
        # Если цель есть
        if self.target:
            # Перемещение
            speed_vector = self.direction.normalized * self.real_speed_value
            self.pos += speed_vector
            # Достигнута ли цель?
            if self.dot_product(speed_vector, self.target - self.pos) <= 0:
                self.pos = self.target
                self.update_target_and_direction()

    def check_collisions(self):
        """ Проверка на коллизии """
        # Коллизия с игроком
        for e in self.field_object.get_entities(Player):
            if e.is_enabled:
                r = (self.height + self.width) / 4 * self.COLLISION_MODIFIER
                r2 = (e.height + e.width) / 4 * e.COLLISION_MODIFIER
                if is_circles_intersect(self.pos, r, e.pos, r2):
                    e.hurt(self)
        # Коллизия с возникшей на пути преградой
        if self.target and not self.can_walk_at(self.target):
            self.direction = -self.direction
            self.target += self.direction

    def additional_logic(self):
        self.move()
        self.check_collisions()

    def hurt(self, from_):
        """ Метод смерти моба """
        from_.bomb_object.player_object.score += self.SCORE  # Добавляем счёт тому, чья бомба взорвала этого моба
        self.destroy()