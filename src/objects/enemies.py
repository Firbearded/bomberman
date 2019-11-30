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
    SPEED_VALUE = 3
    SCORE = 800
    # Должен преследовать персонажа, если тот находится прямиком перед ним


class Doria (Enemy):
    SPEED_VALUE = 0.75
    SCORE = 1000
    # Умеет ходить сквозь стены


class Ovape (Doria):
    SPEED_VALUE = 2
    SCORE = 2000


class Pass (Minvo):
    SCORE = 4000
    # Умеет убегать от бомб, когда видит их, тоесть они прямиком перед ним


class Coin (Doria):
    SPEED_VALUE = 3
    SCORE = 400
    COLOR = Color.RED
    SPRITE_NAMES = "coin1", "coin2", "coin3", "coin4"
    SPRITE_DELAY = 100


ENEMIES = (Ballom, Onil, Coin)
