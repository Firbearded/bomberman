from src.objects.base_classes.enemy import Enemy
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
    """
    SPEED_VALUE = 1.75
    SCORE = 400
    TURN_CHANCE_MODIFIER = 1 - .0005
    COLOR = Color.BROWN


class Minvo(Enemy):
    """
    Преследует персонажа, если тот находится на
    прямой по направлению вектора движения до первой преграды (блока или бомбы)
    и в пределах 10 клеток

    В случае нахождения игрока, бежит в его сторону по прямой, не сворачивая,
    если персонаж отгородился или свернул, Minvo перестаёт преследование
    """
    SPEED_VALUE = 2.75
    SCORE = 800
    COLOR = Color.ORANGE


class Ovape(Enemy):
    """
    Ходит сквозь стены, но за игроком не бегает
    """
    SPEED_VALUE = 1.5
    SCORE = 2000
    TURN_CHANCE_MODIFIER = 1 - .1
    COLOR = Color.LIGHT_GREY

    def can_walk_at(self, pos):
        return self.field_object.tile_at(pos).get_wallpass


class Doria(Minvo, Ovape):
    """
    Бежит за игроком также, как Minvo, и при этом
    умеет ходить сквозь стены, но через стены не видит
    """
    SPEED_VALUE = 0.75
    SCORE = 1000
    COLOR = Color.NAVY


class Pass(Minvo):
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
    COLOR = Color.APRICOT

    CHANCE_TURN_ASIDE = 0.2
    CHANCE_TURN_BACK = 0.03

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field, pos, size)
        self.chasing = False

    def get_new_target(self):
        if self.field_object.tracker.get_straight_vision(self.tile) or self.chasing:
            # Если уже преследуем или видим игрока по прямой
            next_tile = self.field_object.tracker.get_next_tile(self.tile)
            if not next_tile:
                self.chasing = False
                return super().get_new_target()
            else:
                self.chasing = True
                return next_tile
        else:
            # Если не преследуем и игрок не виден
            return super().get_new_target()


class Pontan(Doria):
    """
    Как Doria, но быстрый
    """
    SPEED_VALUE = 2.25
    SCORE = 8000
    SPRITE_NAMES = "coin1", "coin2", "coin3", "coin4"
    SPRITE_DELAY = 100
    COLOR = Color.RED


ENEMIES = (Ballom, Onil, Dahl, Minvo, Ovape, Doria, Pass, Pontan)
