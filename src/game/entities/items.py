from src.game.base_classes.timer_object import TimerObject
from src.game.entities.base.enemy import Enemy
from src.game.entities.base.item import Item
from src.game.entities.player import Player
from src.game.supporting.constants import Sounds
from src.utils.vector import Point


class BombNumberUp(Item):
    SPRITE_NAMES = ("count_up",)

    def on_take(self, player_object): player_object.bomb_up()


class SpeedUp(Item):
    SPRITE_NAMES = ("speed_up",)

    def on_take(self, player_object): player_object.speed_up()


class PowerUp(Item):
    SPRITE_NAMES = ("power_up",)

    def on_take(self, player_object): player_object.power_up()


class LifeUp(Item):
    SPRITE_NAMES = ("life",)

    def on_take(self, player_object): player_object.life_up()


class Detonator(Item):
    SPRITE_NAMES = ("detonator",)

    def on_take(self, player_object): player_object.get_detonator()


class WallpassUp(Item):
    SPRITE_NAMES = ("wallpass",)

    def on_take(self, player_object): player_object.get_wallpass()


class BombpassUp(Item):
    SPRITE_NAMES = ("bombpass",)

    def on_take(self, player_object): player_object.get_bombpass()


class FlamepassUp(Item):
    SPRITE_NAMES = ("flamepass",)

    def on_take(self, player_object): player_object.get_flamepass()


class MysteryUp(Item):
    SPRITE_NAMES = ("mystery",)

    def on_take(self, player_object): player_object.get_mystery()


class Door(Item):
    SPRITE_NAMES = ("door",)
    SOUND_WIN = Sounds.Music.round_win.value
    SIZE = 1, 1

    def __init__(self, field_object, pos: Point, size: tuple = None):
        super().__init__(field_object, pos, size)
        self.is_exploded = False

    def on_take(self, player_object):
        self.game_object.mixer.channels['effects'].sound_play(self.SOUND_WIN)
        self.field_object.round_win()

    def on_explosion(self):  # функция, выполняющаяся при подрыве двери
        self.is_exploded = False
        self.field_object.door_explosion(self.tile)

    def hurt(self, from_e):
        if not self.is_exploded:
            self.is_exploded = True
            spawn_timer = TimerObject(from_e.delay + 5)  # Создание таймера,
            spawn_timer.on_timeout = self.on_explosion  # призывающего мобов
            self.game_object.add_global_timer(spawn_timer)  # при подрыве двери

    def additional_logic(self):
        for e in self.field_object.get_entities(Player):
            if e.is_enabled:
                if self.tile == e.tile:
                    if len(self.field_object.get_entities(Enemy)) == 0:
                        self.on_take(e)
                        self.destroy()


DROP_LIST = (BombNumberUp, PowerUp, Detonator, SpeedUp, LifeUp,
             WallpassUp, BombpassUp, FlamepassUp, MysteryUp)
