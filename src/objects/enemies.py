from src.objects.base_classes.enemy import Enemy
from src.utils.constants import Color


class Ballom (Enemy):
    SPEED_VALUE = 1
    SCORE = 100
    COLOR = Color.ORANGE
    SPRITE_NAMES = "ballom1", "ballom2", "ballom3"
    SPRITE_DELAY = 350


class Onil (Enemy):
    SPEED_VALUE = 2
    SCORE = 200
    COLOR = (100, 100, 255)
    SPRITE_NAMES = "onil1", "onil2", "onil3"
    SPRITE_DELAY = 350


class Dahl (Enemy):
    SPEED_VALUE = 2.25
    SCORE = 400


class Minvo (Enemy):
    """
    Преследует персонажа, если тот находится на
    прямой по направлению вектора движения до первой преграды (блока или бомбы)
    и в пределах 10 клеток

    В случае нахождения игрока, бежит в его сторону по прямой, не сворачивая,
    если персонаж отгородился или свернул, Minvo перестаёт преследование
    """
    SPEED_VALUE = 3
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
    SPEED_VALUE = 2
    SCORE = 2000


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
    SPEED_VALUE = 3
    SCORE = 4000


class Coin (Doria):
    """
    Как Doria, но быстрый
    """
    SPEED_VALUE = 3
    SCORE = 8000
    COLOR = Color.RED
    SPRITE_NAMES = "coin1", "coin2", "coin3", "coin4"
    SPRITE_DELAY = 100


ENEMIES = (Ballom, Onil, Coin)
