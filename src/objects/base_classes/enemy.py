from random import randint

from src.objects.base_classes.entity import Entity
from src.objects.player import Player
from src.utils.constants import Color
from src.utils.intersections import is_circles_intersect
from src.utils.vector import Point


class Enemy(Entity):
    """ Класс мобов """
    SPEED_VALUE = .5  # Скорость моба
    SCORE = 100       # Очки, выпадаемые с моба

    SPRITE_CATEGORY = "enemy_sprites"
    SPRITE_DELAY = 500

    COLOR = Color.MAGENTA

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        """
        self.target — клетка, куда стремится моб
        self.speed_vector — направление, которое выбрал моб
        """
        super().__init__(field, pos, size)

        self.target = self.new_target()
        self.speed_vector = self.new_target_direction()

        self.animation = self.create_animation()

    def new_target_direction(self):
        """ Расчёт направления для моба """
        target_direction = self.target - self.pos

        return target_direction.united

    def new_target(self):
        """ Выбор мобом следующей цели """
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
        if self.target == self.pos or not self.speed_vector:  # Если мы стоим на месте,
            self.target = self.new_target()                   # то пытаемся выбрать новое направление
            self.speed_vector = self.new_target_direction()

        normalized_speed_vector = self.speed_vector.normalized * self.real_speed_value
        new_pos = self.pos + normalized_speed_vector             # Следующая позиция (которая будет в следующий тик)
        new_target_direction = (self.target - new_pos).united    # Направление к цели от следующей позиции

        if self.target != self.tile and not self.field_object.tile_at(self.target).walkable:
            self.speed_vector *= -1   # Проверка на коллизии. Если мы вдруг идём прямо в клетку, по которой нельзя
            self.target = self.tile   # ходить, то разворачиваемся.
            return

        if self.speed_vector == new_target_direction:
            self.pos = new_pos   # Если новый вектор направления и старый совпрадают, то ничего
        else:                    # Если же новый вектор направления не равен со старым, то значит, что мы в следующий
            self.pos = self.target  # тик перейдём клетку-цель, поэтому
            if self.field_object.tile_at(self.tile + self.speed_vector).walkable:
                self.target += self.speed_vector  # Если можно идти в следующую клетку, то идём дальше
            else:
                self.target = self.new_target()   # иначе ищем новую цель
                self.speed_vector = self.new_target_direction()

        for e in self.field_object.get_entities(Player):  # Проверка на коллизии c игроками
            if e.is_enabled:
                r = (self.height + self.width) / 4 * self.COLLISION_MODIFIER
                r2 = (e.height + e.width) / 4 * self.COLLISION_MODIFIER
                if is_circles_intersect(self.pos, r, e.pos, r2):
                    e.hurt(self)

    def hurt(self, from_):
        """ Метод смерти моба """
        from_.bomb_object.player_object.score += self.SCORE  # Добавляем счёт тому, чья бомба взорвала этого моба
        self.destroy()
