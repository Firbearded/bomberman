import pygame
from src.objects.entity import Entity
from src.objects.field import Field
from src.utils.vector import Vector, Point
from src.objects.player import Player
from src.utils.intersections import is_collide_rect

class Item(Entity):
    def __init__(self, field_object: Field, pos: Point, size: tuple):
        super().__init__(field_object, pos, size)

    def on_take(self, player_object):
        pass

    def additional_logic(self):
        for item in self.field_object.entities:
            if type(item) is Player:
                if(is_collide_rect(self.pos, self.size, item.pos, item.size, )):
                    self.on_take(item)
                    self.disable()
                    self.field_object.delete_entity(self)

    def process_draw(self):
        if self.animation is not None:
            self.game_object.screen.blit(self.animation.current_image, (self.real_pos, self.real_size))
        else:
            pygame.draw.rect(self.game_object.screen, (255, 255, 0), (self.real_pos, self.real_size), 0)

