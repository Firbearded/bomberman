from random import randint

from src.objects.base_classes.enemy import Enemy
from src.objects.field.tiles import TileWall, TileUnreachableEmpty
from src.objects.player import Player
from src.utils.constants import Color
from src.utils.intersections import is_circles_intersect
from src.utils.vector import Point

"""
class Ballom (Enemy):
    SPEED_VALUE = 1
    SCORE = 100
    COLOR = Color.ORANGE
    SPRITE_NAMES = "ballom1", "ballom2", "ballom3"
    SPRITE_DELAY = 350
"""

class Onil (Enemy):
    SPEED_VALUE = 1.5
    SCORE = 200
    COLOR = (100, 100, 255)
    SPRITE_NAMES = "onil1", "onil2", "onil3"
    SPRITE_DELAY = 350


class Dahl (Enemy):
    """
    Чаще всего бегает слева направо, иногда меняя направление на сверху вниз
    """
    SPEED_VALUE = 1.75
    SCORE = 400


class Minvo (Enemy):
    """
    Преследует персонажа, если тот находится на
    прямой по направлению вектора движения до первой преграды (блока или бомбы)
    и в пределах 10 клеток

    В случае нахождения игрока, бежит в его сторону по прямой, не сворачивая,
    если персонаж отгородился или свернул, Minvo перестаёт преследование
    """
    SPEED_VALUE = 2.75
    SCORE = 800


class Doria (Enemy):
    """
    Бежит за игроком также, как Minvo, и при этом
    умеет ходить сквозь стены, но через стены не видит
    """
    SPEED_VALUE = 0.75
    SCORE = 1000


class Ovape (Enemy):
    """
    Ходит сквозь стены, но за игроком не бегает
    """
    chance_of_turning = 0 #Шанс поворота в процентах, растет на 20 процентов на каждом перекрёстке, вплоть до 50 процентов,

    def can_walk_at(self, pos):
        return self.field_object.tile_at(pos) != TileWall and self.field_object.tile_at(pos) != TileUnreachableEmpty

    def additional_logic(self):
        if self.target == self.pos or not self.speed_vector:  # Если мы стоим на месте,
            self.target = self.new_target()                   # то пытаемся выбрать новое направление
            self.speed_vector = self.new_target_direction()

        normalized_speed_vector = self.speed_vector.normalized * self.real_speed_value
        new_pos = self.pos + normalized_speed_vector             # Следующая позиция (которая будет в следующий тик)
        new_target_direction = (self.target - new_pos).united    # Направление к цели от следующей позиции

        if self.target != self.tile and not self.can_walk_at(self.target):
            self.speed_vector *= -1   # Проверка на коллизии. Если мы вдруг идём прямо в клетку, по которой нельзя
            self.target = self.tile   # ходить, то разворачиваемся.

        if self.speed_vector == new_target_direction:
            self.pos = new_pos   # Если новый вектор направления и старый совпрадают, то ничего
        else:                    # Если же новый вектор направления не равен со старым, то значит, что мы в следующий
            self.pos = self.target  # тик перейдём клетку-цель, поэтому

            if self.tile.x % 2 != 0 and self.tile.y % 2 != 0: # Проверка на изменение цели, происходит только на "перекрёстках"
                self.chance_of_turning += 20
                if self.chance_of_turning > 60:
                    self.chance_of_turning = 50
                if randint (1, 100) <= self.chance_of_turning:
                    self.target = self.new_target ()
                    self.speed_vector = self.new_target_direction ()
                    self.chance_of_turning = 0

            if self.field_object.tile_at(self.tile + self.speed_vector) != TileWall and self.field_object.tile_at(self.tile + self.speed_vector) != TileUnreachableEmpty:
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

    SPEED_VALUE = 1.5
    SCORE = 2000

class Ballom (Ovape): # Выполняет функцию подопытного, в данный момент является Ovape
    SPEED_VALUE = 1.5
    SCORE = 100
    COLOR = Color.ORANGE
    SPRITE_NAMES = "ballom1", "ballom2", "ballom3"
    SPRITE_DELAY = 350

class Pass (Enemy):
    """
    Обнаруживвает персонажа также, как Minvo, но при нахождении
    преследует не по прямой, а по какому-нибудь (не обязательно кратчайшему)
    пути до персонажа, пока доступ к персонажу не будет закрыт
    (больше не будет возможных путей или персонаж не спрячется в блоке)

    Если при преследовании на единственном пути до персонажа появилась бомба,
    Pass убегает в обратную сторону от неё, при этом он не останавливается,
    добежав до угла, а просто забывает о бомбе и начинает действовать,
    как обычный моб, пока вновь не найдёт персонажа
    Если путь не единственный, то Pass старается обойти бомбу, а убегать в обратную сторону начинает
    лишь если бомбу заспавнили в 4 или меньше блоках от него на его пути к персонажу
    """
    SPEED_VALUE = 2.75
    SCORE = 4000


class Coin (Doria):
    """
    Как Doria, но быстрый
    """
    SPEED_VALUE = 2.25
    SCORE = 8000
    COLOR = Color.RED
    SPRITE_NAMES = "coin1", "coin2", "coin3", "coin4"
    SPRITE_DELAY = 100


ENEMIES = (Ballom, Onil, Coin)
