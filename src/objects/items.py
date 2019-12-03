from src.objects.base_classes.enemy import Enemy
from src.objects.base_classes.item import Item
from src.objects.player import Player
from src.utils.constants import Sounds


# TODO:  + Bomb-Walk + Wall-Walker + Mystery + Flame-Proof +

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
    SPRITE_NAMES = ()  # TODO: нужен спрайт для детонатора

    def on_take(self, player_object): player_object.get_detonator()


class Door(Item):
    SPRITE_NAMES = ("door",)
    SOUND_WIN = Sounds.Music.round_win.value
    SIZE = 1, 1

    def on_take(self, player_object):
        self.game_object.mixer.channels['effects'].sound_play(self.SOUND_WIN)
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


DROP = (BombNumberUp, PowerUp, Detonator, SpeedUp, LifeUp, )
