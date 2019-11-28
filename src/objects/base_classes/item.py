from src.objects.base_classes.entity import Entity
from src.utils.constants import Color
from src.utils.intersections import is_collide_rect
from src.utils.vector import Point


class Item(Entity):
    SPRITE_CATEGORY = 'item_sprites'
    SPRITE_DELAY = 0

    SOUND_PICK_UP = 'item'

    SIZE = .75, .75
    COLOR = Color.YELLOW

    def __init__(self, field_object, pos: Point, size: tuple = None):
        if size is None:
            size = self.SIZE
        super().__init__(field_object, pos, size)
        self.animation = self.create_animation()
        self.centralize_pos()

    def centralize_pos(self):
        cx, cy = self.tile
        cx += .5 - self.width / 2
        cy += .5 - self.width / 2
        self.pos = Point(cx, cy)

    def on_take(self, player_object):
        pass

    def hurt(self, from_e):
        self.destroy()

    def additional_logic(self):
        from src.objects.player import Player
        for e in self.field_object.get_entities(Player):
            if is_collide_rect(self.pos, self.size, e.pos, e.size):
                self.game_object.play('effect', self.SOUND_PICK_UP)
                self.on_take(e)
                self.destroy()
