from src.objects.base_classes.enemy import Enemy
from src.objects.base_classes.item import Item
from src.objects.player import Player
from src.utils.constants import Sounds
from src.utils.vector import Point
from src.objects.base_classes.base_objects.timer_object import TimerObject


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
    SPRITE_NAMES = ("wallpass", )

    def on_take(self, player_object): player_object.get_wallpass()


class BombpassUp(Item):
    SPRITE_NAMES = ("bombpass", )

    def on_take(self, player_object): player_object.get_bombpass()


class FlamepassUp(Item):
    SPRITE_NAMES = ("flamepass", )

    def on_take(self, player_object): player_object.get_flamepass()


class MysteryUp(Item):
    SPRITE_NAMES = ("mystery", )

    def on_take(self, player_object): player_object.get_mystery()


class Door(Item):
    def __init__(self, field_object, pos: Point, size: tuple = None):
        super().__init__(field_object, pos, size)
        self.is_exploded = False


    SPRITE_NAMES = ("door",)
    SOUND_WIN = Sounds.Music.round_win.value
    SIZE = 1, 1

    def on_take(self, player_object):
        self.game_object.mixer.channels['effects'].sound_play(self.SOUND_WIN)
        self.field_object.round_win()

    def on_explosion(self): #функция, выполняющаяся при подрыве двери
        self.is_exploded = False
        self.field_object._generate_enemies (self.field_object._enemies_on_door, self.tile)

    def hurt(self, from_e):
        if not self.is_exploded:
            self.is_exploded = True
            spawn_timer = TimerObject(from_e.delay + 5)          # Создание таймера,
            spawn_timer.on_timeout = self.on_explosion      # призывающего мобов
            self.game_object.add_timer(spawn_timer) # при подрыве двери

    def additional_logic(self):
        for e in self.field_object.get_entities(Player):
            if e.is_enabled:
                if self.tile == e.tile:
                    if len(self.field_object.get_entities(Enemy)) == 0:
                        self.on_take(e)
                        self.destroy()


DROP_LIST = (BombNumberUp, PowerUp, Detonator, SpeedUp, LifeUp,
             WallpassUp, BombpassUp, FlamepassUp, MysteryUp)
