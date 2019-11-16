import pygame
from src.objects.entity import Entity
from src.utils.vector import Point


class Player(Entity):
    #           keys; sp_vector[{}]; *({})
    KEYS_MOV = (((pygame.K_LEFT, pygame.K_a,), 0, -1),
                ((pygame.K_RIGHT, pygame.K_d,), 0, 1),
                ((pygame.K_UP, pygame.K_w,), 1, -1),
                ((pygame.K_DOWN, pygame.K_s,), 1, 1),
                )

    def __init__(self, field, pos: Point, size: tuple):
        super().__init__(field, pos, size)


class Bomb(Entity):
    def __init__(self, player_object, pos: Point, time, power):
        super().__init__(player_object.field, pos, (1, 1))
        self.player_object = player_object
        self.field = player_object.field

        self.pos = Point()
        self.pos.copy_from(pos)
        self.power = power
        self.time = time
