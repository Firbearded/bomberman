from random import randint, choice

from src.objects.base_classes.entity import Entity
from src.objects.player import Player
from src.utils.constants import Color
from src.utils.intersections import is_circles_intersect
from src.utils.vector import Point, Vector


class Enemy(Entity):
    """ Класс мобов """
    SPEED_VALUE = .5  # Скорость моба
    SCORE = 100  # Очки, выпадаемые с моба
    delta = [Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]

    SPRITE_CATEGORY = "enemy_sprites"
    SPRITE_DELAY = 500
    COLOR = Color.MAGENTA

    '''
    TURN_CHANCE_MODIFIER = 1 - .05   # Больше = Реже

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        """
        self.target — клетка, куда стремится моб
        self.speed_vector — направление, которое выбрал моб
        """
        super().__init__(field, pos, size)

        self.update_target()

        self._chance_of_not_turning = 1.

        self.animation = self.create_animation()

    def can_walk_at(self, pos):
        """ Может ли моб ходить по клетке pos? """
        return self.field_object.tile_at(pos).walkable

    # ======= Цель (куда мы движемся) и направление, чтобы попасть в эту цель =======
    def _get_new_target(self):
        """ Выбор мобом следующей цели (При стандартном поведение моба) """
        dx = -1, 0, 1, 0
        dy = 0, -1, 0, 1

        possible_targets = []

        for x, y in zip(dx, dy):
            p = self.tile + Point(x, y)
            if self.can_walk_at(p):
                possible_targets.append(p)

        if not possible_targets:
            return self.tile

        target = choice(possible_targets)  # Получение случайного направления из массива возможных направлений
        return target

    def _get_new_subtarget(self):
        """
        Расчёт сдедующей клетки для моба, чтобы попасть в target.

        Должен возвращать одну из четырёх клеткок, которые вокруг моба —
         в какую сторону мы сейчас хотим двигаться,
         чтобы от pos прийти в Enemy.target
        """
        return self.target

    def _get_direction(self, pos):
        self.subtarget = self._get_new_subtarget()
        return (self.subtarget - pos).united

    def update_direction(self):
        self.speed_vector = self._get_direction(self.pos)

    def update_target(self):
        self.target = self._get_new_target()
        self.update_direction()

    def set_target(self, pos):
        self.target = pos
        self.update_direction()

    # =========== Методы на проверку ===========
    def check_environment(self):
        """ Проверка окружения (застряли, увидели игрока и тд), то есть проверка, которая всегда происходит """
        if self.subtarget == self.pos or not self.speed_vector:
            self.update_target()  # Если мы стоим на месте, # то пытаемся выбрать новое направление

        if self.subtarget != self.tile and not self.can_walk_at(self.subtarget):
            # Если мы вдруг идём прямо в клетку, по которой нельзяходить, то возвращаемся.
            self.set_target(self.tile)

    def check_moving(self):
        real_speed_vector = self.speed_vector.normalized * self.real_speed_value
        new_pos = self.pos + real_speed_vector  # Следующая позиция (которая будет в следующий тик)
        new_target_direction = self._get_direction(new_pos)  # Направление к цели от следующей позиции
        if self.speed_vector == new_target_direction:
            self.pos = new_pos  # Если новый вектор направления и старый совпрадают, то ничего
        else:  # Если же новый вектор направления не равен со старым, то значит, что мы в следующий
            self.pos = self.subtarget  # тик перейдём клетку-цель, поэтому немного сами сдвигаемся
            self.on_new_tile()      # вызываем новую проверку

    def check_collisions(self):
        """ Проверка на коллизии """
        for e in self.field_object.get_entities(Player):
            if e.is_enabled:
                r = (self.height + self.width) / 4 * self.COLLISION_MODIFIER
                r2 = (e.height + e.width) / 4 * e.COLLISION_MODIFIER
                if is_circles_intersect(self.pos, r, e.pos, r2):
                    e.hurt(self)

    def on_new_tile(self):
        """ Проверка, когда мы пришли в новую клетку """

        if self.can_walk_at(self.subtarget + self.speed_vector):  # Если можно идти в следующую клетку, то идём дальше
            self.set_target(self.subtarget + self.speed_vector)
        else:
            self.update_target()  # иначе ищем новую цель

        if self.tile.x % 2 + self.tile.y % 2 > 1:  # Проверка на изменение цели, происходит только на "перекрёстках"
            self._chance_of_not_turning *= self.TURN_CHANCE_MODIFIER  # Случайный поворот моба
            mod = 1000
            if randint(1, mod) > self._chance_of_not_turning * mod:
                self.update_target()
                self._chance_of_not_turning = 1.

    # ================ Остальное ===============
    def additional_logic(self):
        self.check_environment()  # Проверка на всякие неожиданности

        self.check_moving()  # Движение и проверка на попадание в новую клетку

        self.check_collisions()  # Проверка на коллизии с игроками

    def hurt(self, from_):
        """ Метод смерти моба """
        from_.bomb_object.player_object.score += self.SCORE  # Добавляем счёт тому, чья бомба взорвала этого моба
        self.destroy()
    '''

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
        # Если можем продолжить движение, не меняем направление
        if self.direction and self.can_walk_at(self.tile + self.direction):
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