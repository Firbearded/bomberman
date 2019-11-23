from src.objects.base_classes.enemy import Enemy
from src.utils.constants import Color


class Ballom(Enemy):
    SPEED_VALUE = .5
    SCORE = 100
    COLOR = Color.ORANGE


class Onil(Enemy):
    SPEED_VALUE = 1
    SCORE = 200
    COLOR = (100, 100, 255)
