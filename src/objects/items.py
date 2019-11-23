from src.objects.base_classes.item import Item


class ItemPowerUp(Item):
    SPRITE_NAMES = "power_up",

    def on_take(self, player_object):
        player_object.bombs_power += 1


class ItemLifeUp(Item):
    SPRITE_NAMES = "life",

    def on_take(self, player_object):
        player_object.lives += 1
