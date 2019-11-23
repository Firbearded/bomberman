from src.objects.base_classes.entity import Entity
from src.objects.field import Field
from src.objects.player import Player
from src.utils.constants import Color
from src.utils.intersections import is_collide_rect
from src.utils.vector import Point


class Item(Entity):
    SPRITE_CATEGORY = 'item_sprites'
    SPRITE_DELAY = 0

    SOUND_PICK_UP = 'item'

    COLOR = Color.YELLOW

    def __init__(self, field_object: Field, pos: Point, size: tuple):
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

    def additional_logic(self):
        for e in self.field_object.entities:
            if type(e) is Player:
                if is_collide_rect(self.pos, self.size, e.pos, e.size):
                    self.game_object.sounds['effect'][self.SOUND_PICK_UP].play()
                    self.on_take(e)
                    self.destroy()
