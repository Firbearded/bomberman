from src.objects.base_classes.enemy import Enemy
from src.utils.constants import Color
from src.objects.player import Player
from src.utils.vector import Vector, Point

from queue import Queue

"""
    Внимание! При создании логики в мобах переопределять следующие методы:
1)_get_new_target(self) возвращает клетку цели, которую преследует моб (это игрок, или
  конечная точка некоторой траектории, или просто соседняя клетка, если моб не слишком умный);
2)_get_new_subtarget(self) возвращает следующую клетку на пути моба к цели;
3)_can_walk_at(self, pos) возвращает, может ли моб ходить по клетке, заданной позицией (по
  умолчанию метод не разрешает ходить по стенам).
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
    SPEED_VALUE = 0.5 # 2.75
    SCORE = 4000
    COLOR = Color.APRICOT
    delta = [Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]

    def _get_next_tile(self):
        queue = Queue()
        parent = []
        for i in range(self.field_object.width):
            parent.append(list())
            for j in range(self.field_object.height):
                parent[i].append(Point(-1, -1))
        parent[self.tile.x][self.tile.y] = self.tile
        queue.put(self.tile)
        while not queue.empty():
            current_pos = queue.get()
            for v in self.delta:
                new_pos = current_pos + v
                if self.can_walk_at(current_pos + v) and parent[new_pos.x][new_pos.y] == Point(-1, -1):
                    parent[new_pos.x][new_pos.y] = current_pos
                    queue.put(new_pos)
        if parent[self.target.x][self.target.y] == Point(-1, -1):
            return Point(-1, -1)
        current_pos = self.target
        while parent[current_pos.x][current_pos.y] != self.tile:
            current_pos = parent[current_pos.x][current_pos.y]
        return current_pos

    def _get_new_target(self):
        player_object = self.field_object.get_entities(Player)[0]
        return player_object.tile

    def _get_new_subtarget(self):
        next_pos = self._get_next_tile()
        # print(self.target, next_pos)
        if next_pos == Point(-1, -1):
            return self.tile
        else:
            return next_pos


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
