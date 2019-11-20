import pygame
from src.objects.entity import Entity
from src.utils.vector import Vector, Point
from src.utils.intersections import collide_rect


def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1


class Player(Entity):
    #           keys; sp_vector[{}]; *({})
    KEYS_MOV = (((pygame.K_LEFT, pygame.K_a,), 0, -1),
                ((pygame.K_RIGHT, pygame.K_d,), 0, 1),
                ((pygame.K_UP, pygame.K_w,), 1, -1),
                ((pygame.K_DOWN, pygame.K_s,), 1, 1),
                )

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field, pos, size)

    def corner_fixing(self, speed_vector):
        tile_x, tile_y = self.tile
        is_corner_fixing = 0  # Исправление застревания на углах
        for i in range(2):
            j = (i + 1) % 2
            if speed_vector[j] == 0:
                vec_dir = sign(speed_vector[i])
                d = ((-1, 0, 1), (vec_dir, vec_dir, vec_dir))
                up, nx, dn = [self.field.grid[tile_y + d[i][k]][tile_x + d[j][k]] != 0 for k in
                              range(3)]  # TODO: tile == 0
                if not nx:
                    if (speed_vector[i] > 0 and (self.right, self.bottom)[i] == (tile_x + 1, tile_y + 1)[i]) or \
                            (speed_vector[i] < 0 and (self.left, self.top)[i] == (tile_x, tile_y)[i]):
                        if up and self.center[j] < self.tile[j] + .5:
                            is_corner_fixing = 1
                            speed_vector[i] = 0
                            speed_vector[j] = 1
                        elif dn and self.center[j] > self.tile[j] + .5:
                            is_corner_fixing = 1
                            speed_vector[i] = 0
                            speed_vector[j] = -1
        speed_vector = speed_vector.normalized * self.speed_value  # self.speed_vector - всего лишь вектор для
        # направления, тут я делаю, чтобы длина самого вектора была равна self.speed_value
        if is_corner_fixing:  # Если мы исправляем застревания на углах,
            for i in range(2):  # то проверяем, чтобы подойти ровно в клетку
                if abs(self.pos[i] - round(self.pos[i])) < \
                        abs((self.pos[i] + speed_vector[i]) - round(self.pos[i] + speed_vector[i])):
                    speed_vector[i] = round(self.pos[i]) - self.pos[i]
        return speed_vector, is_corner_fixing

    def wall_collisions(self, speed_vector):
        tile_x, tile_y = self.tile
        for i in range(2):  # страшный код на проверку и исправления коллизий
            if speed_vector[i] == 0:
                continue
            tmp_speed_vector = Vector()
            tmp_speed_vector[i] = speed_vector[i]
            new_pos = self.pos + tmp_speed_vector

            for dx in (-1, 0, 1):  # range(-max(1, round(self.size[0])), max(1, round(self.size[0])) + 1):
                for dy in (-1, 0, 1):  # range(-max(1, round(self.size[1])), max(1, round(self.size[1])) + 1):
                    # Проверка на то, подходит ли нам клетка для проверки
                    if dx == dy == 0: continue
                    if self.field.grid[tile_y + dy][tile_x + dx] == 0: continue
                    fw, fh = self.field.size
                    if not (0 <= tile_y + dy < fh and 0 <= tile_x + dx < fw): continue

                    l, t, r, b = collide_rect(new_pos, self.size, Point(tile_x + dx, tile_y + dy), (1, 1))

                    if (l, t)[i]:  # Проверка на коллизии и подгонка скорости, чтобы мы встали в ровные координаты
                        speed_vector[i] = self.tile[i] - self.pos[i]
                    if (r, b)[i]:
                        speed_vector[i] = self.tile[i] + 1 - (self.pos[i] + self.size[i])
        return speed_vector

    def process_logic(self):
        normalized_speed_vector, is_fixing = self.corner_fixing(Vector(*self.speed_vector))

        if not is_fixing:
            normalized_speed_vector = self.wall_collisions(normalized_speed_vector)

        self.pos = self.pos + normalized_speed_vector

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
