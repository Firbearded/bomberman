from src.objects.base_classes.enemy import Enemy
from src.objects.player import Player
from src.utils.constants import Color
from src.utils.vector import Vector, Point

"""
    Внимание! При создании логики в мобах переопределять следующие методы:
1)can_walk_at(self, pos) возвращает, может ли моб ходить по клетке, заданной позицией (по
  умолчанию метод не разрешает ходить по стенам);
2)get_new_target(self) возвращает цель моба - соседнюю мобом клетку, в которую он должен
  перейти.
  
  Внимание! При создании логики в мобах использовать значения из следующих полей класса:
1)self.target - текущая цель моба (None, если моб стоит на месте);
2)self.direction - направление движения моба (единичный вектор; None, если моб стоит на месте).
Информация в этих полях всегда корректна при вызове can_walk_at и get_new_target.

  Внимание! При создании логики в мобах могут понадобиться следующие инструменты:
1)self.field_object.tracker - класс, следящий за игроком (см. src.objects.field.tracker.py);
2)super.get_next_target() - метод, возвращающий следующую цель при встроенном глупом поведении
  моба.
"""

class Ballom (Enemy):
    SPEED_VALUE = 1
    SCORE = 100
    COLOR = Color.ORANGE
    SPRITE_NAMES = "ballom1", "ballom2", "ballom3"
    SPRITE_DELAY = 350


class Onil(Enemy):
    SPEED_VALUE = 1.5
    SCORE = 200
    COLOR = Color.BLUE
    SPRITE_NAMES = "onil1", "onil2", "onil3"
    SPRITE_DELAY = 350


class Dahl(Enemy):
    """
    Чаще всего бегает слева направо, иногда меняя направление на сверху вниз
    Оказывается, ещё и бегает за игроком, как Minvo, пожтому теперь всё наследуется из него
    """
    VISION_DIST = 6

    def get_next_tile(self): #Находит, с какой стороны игрок, и возвращает тайл по направлению в его сторону
        target = self.field_object.get_entities (Player)[0].tile
        next_tile = self.tile
        if self.tile.x - target.x > 0 and self.tile.x - target.x <= self.VISION_DIST and self.tile.y == target.y:
            next_tile += Vector (-1, 0)
        elif self.tile.x - target.x < 0 and self.tile.x - target.x >= -self.VISION_DIST and self.tile.y == target.y:
            next_tile += Vector (1, 0)
        elif self.tile.y - target.y > 0 and self.tile.y - target.y <= self.VISION_DIST and self.tile.x == target.x:
            next_tile += Vector (0, -1)
        elif self.tile.y - target.y < 0 and self.tile.y - target.y >= -self.VISION_DIST and self.tile.x == target.x:
            next_tile += Vector (0, 1)
        else:
            next_tile = None
        return next_tile

    def straight_line_check(self): #Находится ли игрок на прямой, нужно для Doria
        if self.field_object.tracker.get_straight_vision(self.tile):
            return True
        else:
            return False

    def get_new_target(self): #Как у Пасса, но подстроенный под других мобов
        if self.straight_line_check():
            next_tile = self.get_next_tile()
            if not next_tile:
                return super().get_new_target()
            else:
                return next_tile
        else:
            return super().get_new_target()

    SPEED_VALUE = 1.75
    SCORE = 400

    CHANCE_TURN_ASIDE = 0.02
    CHANCE_TURN_BACK = 0.05

    COLOR = Color.BROWN


class Minvo(Dahl):
    """
    Преследует персонажа, если тот находится на
    прямой по направлению вектора движения до первой преграды (блока или бомбы)
    и в пределах 10 клеток

    В случае нахождения игрока, бежит в его сторону по прямой, не сворачивая,
    если персонаж отгородился или свернул, Minvo перестаёт преследование
    """
    VISION_DIST = 10

    SPEED_VALUE = 2.75
    SCORE = 800
    COLOR = Color.ORANGE


class Ovape(Enemy):
    """
    Ходит сквозь стены, но за игроком не бегает
    """
    SPEED_VALUE = 1.5
    SCORE = 2000
    COLOR = Color.LIGHT_GREY

    def can_walk_at(self, pos):
        return self.field_object.tile_at(pos).wallpass


class Doria(Dahl, Ovape):
    """
    Бежит за игроком также, как Minvo, и при этом
    умеет ходить сквозь стены
    """
    VISION_DIST = 5

    def straight_line_check(self):  # Находится ли игрок на прямой, нужно для Doria
        if self.field_object.transparrent_tracker.get_straight_vision (self.tile):
            return True
        else:
            return False

    SPEED_VALUE = 0.75
    SCORE = 1000
    COLOR = Color.NAVY


class Pass(Enemy):
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
    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field, pos, size)
        self.chasing = False

    def get_new_target(self):
        if self.field_object.tracker.get_straight_vision(self.tile) or self.chasing:
            # Если уже преследуем или видим игрока по прямой
            next_tile = self.field_object.tracker.get_next_tile(self.tile)
            if not next_tile:
                return super().get_new_target()
            else:
                self.chasing = True
                return next_tile
        else:
            # Если не преследуем и игрок не виден
            return super().get_new_target()

    SPEED_VALUE = 2.75
    SCORE = 4000
    COLOR = Color.APRICOT


class Pontan(Doria):
    """
    Как Doria, но быстрый
    """
    VISION_DIST = 6
    SPEED_VALUE = 2.25
    SCORE = 8000
    SPRITE_NAMES = "coin1", "coin2", "coin3", "coin4"
    SPRITE_DELAY = 100
    COLOR = Color.RED


ENEMIES = (Ballom, Onil, Dahl, Minvo, Ovape, Doria, Pass, Pontan)
