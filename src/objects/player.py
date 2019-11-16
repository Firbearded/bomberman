import pygame
from src.objects.entity import Entity
from src.utils.vector import Vector, Point
from src.utils.intersections import is_collide_rect


class Player(Entity):
    #           keys; sp_vector[{}]; *({})
    KEYS_MOV = (((pygame.K_LEFT, pygame.K_a,), 0, -1),
                ((pygame.K_RIGHT, pygame.K_d,), 0, 1),
                ((pygame.K_UP, pygame.K_w,), 1, -1),
                ((pygame.K_DOWN, pygame.K_s,), 1, 1),
                )

    def __init__(self, field, pos: Point, size: tuple):
        super().__init__(field, pos, size)

    def process_logic(self):
        speed_vector = Vector()
        speed_vector.copy_from(self.speed_vector)
        speed_vector = speed_vector.normalized * self.speed_value  # self.speed_vector - всего лишь вектор для
        # направления, тут я делаю, чтобы длина самого вектора была равна self.speed_value

        # TODO: проверка на коллизии со стенами

        self.pos = self.pos + (speed_vector.normalized * self.speed_value)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            for keys, i, m in Player.KEYS_MOV:
                if key in keys:
                    self.speed_vector[i] += m
                    break
        if event.type == pygame.KEYUP:
            key = event.key
            for keys, i, m in Player.KEYS_MOV:
                if key in keys:
                    self.speed_vector[i] += (-m)
                    break
