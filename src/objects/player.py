from math import floor

import pygame
from src.objects.entity import Entity
from src.utils.vector import Vector, Point
from src.utils.intersections import is_collide_rect, collide_rect


class Player(Entity):
    #           keys; sp_vector[{}]; *({})
    KEYS_MOV = (((pygame.K_LEFT, pygame.K_a,), 0, -1),
                ((pygame.K_RIGHT, pygame.K_d,), 0, 1),
                ((pygame.K_UP, pygame.K_w,), 1, -1),
                ((pygame.K_DOWN, pygame.K_s,), 1, 1),
                )

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field, pos, size)

    def process_logic(self):
        # print("pos({:.4f}; {:.4f})".format(*self.pos))
        speed_vector = Vector()
        speed_vector.copy_from(self.speed_vector)
        speed_vector = speed_vector.normalized * self.speed_value  # self.speed_vector - всего лишь вектор для
        # направления, тут я делаю, чтобы длина самого вектора была равна self.speed_value

        for i in range(2):  # страшный код на проверку и исправления коллизий  # TODO: исправить застревание на углах
            if speed_vector[i] == 0:
                continue
            tmp_speed_vector = Vector()
            tmp_speed_vector[i] = speed_vector[i]
            new_pos = self.pos + tmp_speed_vector

            tile_x, tile_y = self.tile
            for dx in range(-max(1, round(self.size[0])), max(1, round(self.size[0])) + 1):
                for dy in range(-max(1, round(self.size[1])), max(1, round(self.size[1])) + 1):
                    if dx == dy == 0:
                        continue
                    fw, fh = self.field.size
                    if not (0 <= tile_y + dy < fh and 0 <= tile_x + dx < fw):
                        continue
                    if self.field.grid[tile_y + dy][tile_x + dx] == 0:
                        continue

                    l, t, r, b = collide_rect(new_pos, self.size, Point(tile_x + dx, tile_y + dy), (1, 1))

                    if (l, t)[i]:
                        speed_vector[i] = self.tile[i] - self.pos[i]  # (tile_x + dx, tile_y + dy)[i] - self.pos[i]
                        print("first Collide detected! {} {} {} {}".format(tile_x + dx, tile_y + dy, dx, dy))
                        print("Fixing shift({}) = {} ({} - {})".format("xy"[i], round(self.pos[i]) - self.pos[i], round(self.pos[i]), self.pos[i]))
                    if (r, b)[i]:
                        speed_vector[i] = self.tile[i] + 1 - (self.pos[i] + self.size[i])  # (tile_x + dx, tile_y + dy)[i] - self.pos[i]
                        print("second Collide detected! {} {} {} {}".format(tile_x + dx, tile_y + dy, dx, dy))
                        print("Fixing shift({}) = {} ({} - {}) {}".format("xy"[i], int(self.pos[i]) - (self.pos[i] - self.size[i]), int(self.pos[i]), self.pos[i], self.size[i]))

                    if 0 in (dx, dy):
                        continue

                    if speed_vector[i] == 0:
                        continue

                    if speed_vector[i] > 0:
                        if (dx, dy) not in (((1, -1), (1, 1)), ((-1, 1), (1, 1)))[i]:
                            continue
                    else:
                        if (dx, dy) not in (((-1, 1), (-1, -1)), ((1, -1), (-1, -1)))[i]:
                            continue

        self.pos = self.pos + speed_vector

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
