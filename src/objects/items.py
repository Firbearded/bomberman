from src.objects.base_classes.item import Item
from src.objects.player import Player


class BombNumberUp(Item):
    SPRITE_NAMES = ("count_up",)

    def on_take(self, player_object):
        player_object.max_bombs_number += 1


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
    SOUND_WIN = 'win'
    SIZE = 1, 1

    def on_take(self, player_object):
        self.game_object.sounds['effect'][self.SOUND_WIN].play()
        # TODO : задержка
        self.field_object.next_stage()

    def additional_logic(self):
        for e in self.field_object.entities:
            if type(e) is Player:
                if self.tile == e.tile:
                    if self.field_object.enemies_count == 0:
                        self.on_take(e)
                        self.destroy()


ITEMS = (SpeedUp, LifeUp, BombNumberUp, PowerUp)
