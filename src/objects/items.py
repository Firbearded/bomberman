from src.objects.base_classes.enemy import Enemy
from src.objects.base_classes.item import Item
from src.objects.player import Player
from src.utils.constants import Sounds


class BombNumberUp(Item):
    SPRITE_NAMES = ("count_up",)

    def on_take(self, player_object):
        player_object.bombs_number += 1


class SpeedUp(Item):
    SPRITE_NAMES = ("speed_up",)

    def on_take(self, player_object):
        player_object.speed_value += .2


class PowerUp(Item):
    SPRITE_NAMES = ("power_up",)

    def on_take(self, player_object):
        player_object.bombs_power += 1


class LifeUp(Item):
    SPRITE_NAMES = ("life",)

    def on_take(self, player_object):
        player_object.lives += 1


class Door(Item):
    SPRITE_NAMES = ("door",)
    SOUND_WIN = Sounds.Music.round_win.value
    SIZE = 1, 1

    def on_take(self, player_object):
        self.game_object.mixer['effects'].sound_play(self.SOUND_WIN)
        # TODO : задержка
        self.field_object.next_stage()

    def hurt(self, from_e):
        pass  # self.field_object.generate_enemies(self.field_object._enemies_on_door, self.pos)  # TODO: new enemies

    def additional_logic(self):
        for e in self.field_object.get_entities(Player):
            if e.is_enabled:
                if self.tile == e.tile:
                    if len(self.field_object.get_entities(Enemy)) == 0:
                        self.on_take(e)
                        self.destroy()


DROP = (SpeedUp, LifeUp, BombNumberUp, PowerUp)
