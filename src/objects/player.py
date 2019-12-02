import pygame

from src.objects.base_classes.entity import Entity
from src.objects.bomb import BombWithoutTimer, Bomb
from src.objects.supporting.animation import SimpleAnimation
from src.utils.constants import Color
from src.utils.decorators import protect
from src.utils.intersections import collide_rect
from src.utils.sign import sign
from src.utils.vector import Vector, Point


class Player(Entity):
    SPRITE_CATEGORY = "bomberman_sprites"
    SPRITE_NAMES = {
        'standing': {
            'up': ('bb_standing_up',),
            'down': ('bb_standing_down',),
            'horizontal': ('bb_standing_horizontal',),
        },
        'walking': {
            'up': ('bb_walking1_up', 'bb_walking2_up',),
            'down': ('bb_walking1_down', 'bb_walking2',),
            'horizontal': ('bb_walking1_horizontal', 'bb_walking2_horizontal',),
        }
    }

    SOUND_BOMB = 'setbomb'

    TEMP_DIR = {(1, 0): 'right',
                (0, 1): 'down',
                (-1, 0): 'left',
                (0, -1): 'up'
                }

    #           keys; sp_vector[{}]; *({})
    KEYS_MOV = (((pygame.K_LEFT, pygame.K_a,), 0, -1),
                ((pygame.K_RIGHT, pygame.K_d,), 0, 1),
                ((pygame.K_UP, pygame.K_w,), 1, -1),
                ((pygame.K_DOWN, pygame.K_s,), 1, 1),
                )
    KEYS_BOMB = (pygame.K_SPACE, )
    KEYS_DETONATE_BOMB = (pygame.K_b, )

    COLOR = Color.BLUE

    SPEED_VALUE = 2
    LIVES = 2
    BOMBS_POWER = 2
    BOMBS_NUMBER = 1

    MAX_SPEED_VALUE = 5
    MAX_LIVES = 20
    MAX_BOMBS_POWER = 10
    MAX_BOMBS_NUMBER = 10

    def __init__(self, field_object, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__(field_object, pos, size)

        self.reset(True)
        self.animation = self.create_animation()

    def reset(self, full=False):
        if full:
            self.speed_value = self.SPEED_VALUE        # TODO: инкапсуляция
            self.lives = self.LIVES
            self.bombs_power = self.BOMBS_POWER
            self.bombs_number = self.BOMBS_NUMBER
            self.score = 0
            self.has_detonator = False
            '''
            Если у игрока есть детонатор, он может взорвать
            первую в списке бомбу (self.bombs_with_detonator), если
            та была поставлена после получения бонуса (иначе её не будет
            в этом списке). Такие бомбы могут стоять бесконечно долго.
            '''

        self.bombs_with_detonator = []
        self.current_bombs_number = 0
        self.direction = Vector(0, 1)
        self.is_moving = False
        self.speed_vector = Vector()
        self.pos = Point(1, self.field_object.height - 2)
        self.enable()
        self.show()
        print(self.speed_vector, self.direction)

    def get_state(self):
        state = 'walking' if self.is_moving else 'standing'
        d = list(self.direction)
        if 0 not in d:
            d[1] = 0
        direction = self.TEMP_DIR[tuple(d)]
        return '{}_{}'.format(state, direction)

    @protect
    def create_animation(self):
        if not self.game_object.images: return

        animation_dict = {}
        animation_delay = 150

        had_image_size = False
        for state in self.SPRITE_NAMES:
            for dir in self.SPRITE_NAMES[state]:
                print('PLAYER: GENERATING ANIMS: STATE = {}; DIR = {}'.format(state, dir))
                sprites = []
                sprites2 = []
                for sprite_name in self.SPRITE_NAMES[state][dir]:
                    sprite = self.game_object.images[self.SPRITE_CATEGORY][sprite_name]

                    if not had_image_size:
                        w, h = sprite.get_rect().size
                        k = w / self.real_size[0]
                        new_size = (int(w // k), int(h // k))
                        self.image_size = new_size
                        had_image_size = True

                    sprite = pygame.transform.scale(sprite, self.image_size)
                    if dir == 'horizontal':
                        other_sprite = pygame.transform.flip(sprite, 1, 0)
                        sprites2.append(other_sprite)
                    sprites.append(sprite)
                if dir == 'horizontal':
                    animation_dict[
                        "{}_{}".format(state, 'right')] = animation_delay if state != 'standing' else 0, tuple(sprites)
                    animation_dict[
                        "{}_{}".format(state, 'left')] = animation_delay if state != 'standing' else 0, tuple(sprites2)
                else:
                    animation_dict["{}_{}".format(state, dir)] = animation_delay if state != 'standing' else 0, tuple(
                        sprites)

        return SimpleAnimation(animation_dict, self.get_state())

    def corner_fixing(self, speed_vector):
        tile_x, tile_y = self.tile
        is_corner_fixing = 0  # Исправление застревания на углах
        for i in range(2):
            j = (i + 1) % 2
            if speed_vector[j] == 0:
                vec_dir = sign(speed_vector[i])
                d = ((-1, 0, 1), (vec_dir, vec_dir, vec_dir))
                fw, fh = self.field_object.size

                f = False  # TODO: костыли
                for k in range(3):
                    if not (0 <= tile_y + d[i][k] < fh and 0 <= tile_x + d[j][k] < fw):
                        f = True
                if f: continue

                up, nx, dn = [not self.field_object.tile_at(tile_x + d[j][k], tile_y + d[i][k]).walkable for k in
                              range(3)]
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
        speed_vector = speed_vector.normalized * self.real_speed_value
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
                    if (dx, dy)[i] != sign(tmp_speed_vector[i]): continue
                    if self.field_object.tile_at(tile_x + dx, tile_y + dy).walkable: continue
                    fw, fh = self.field_object.size
                    if not (0 <= tile_y + dy < fh and 0 <= tile_x + dx < fw): continue

                    l, t, r, b = collide_rect(new_pos, self.size, Point(tile_x + dx, tile_y + dy), (1, 1))

                    if (l, t)[i]:  # Проверка на коллизии и подгонка скорости, чтобы мы встали в ровные координаты
                        speed_vector[i] = self.tile[i] - self.pos[i]
                    if (r, b)[i]:
                        speed_vector[i] = self.tile[i] + 1 - (self.pos[i] + self.size[i])
        return speed_vector

    def additional_logic(self):
        normalized_speed_vector, is_fixing = self.corner_fixing(self.speed_vector.copy)

        if not is_fixing:
            normalized_speed_vector = self.wall_collisions(normalized_speed_vector)

        if 0 not in tuple(normalized_speed_vector):
            normalized_speed_vector[0] = 0

        self.pos = self.pos + normalized_speed_vector

        # TODO: screen shift
        # x, y = self.pos
        # top_interval = 200
        # left_interval = 50
        # right_interval = 50
        # x = max(-self.field_object.real_size[0] + right_interval + self.game_object.width / 2, min(left_interval, -self.x * self.field_object.tile_size[0] + self.game_object.width / 2))
        # y = max(-top_interval, -self.y * self.field_object.tile_size[1])
        #
        # print(x, y)
        # # x += self.game_object.width / 2
        # y += self.game_object.height / 2
        #
        self.field_object.pos = Point(-self.x * self.field_object.tile_size[0] + self.game_object.width / 2, -self.y * self.field_object.tile_size[1] + self.game_object.height / 2)

        if self.animation:
            self.is_moving = bool(normalized_speed_vector)
            if self.is_moving:
                self.direction = normalized_speed_vector.united
            self.animation.set_state(self.get_state())

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            for keys, i, m in self.KEYS_MOV:
                if key in keys:
                    self.speed_vector[i] += m
                    self.speed_vector[i] = sign(self.speed_vector[i])
                    break
        if event.type == pygame.KEYUP:
            key = event.key
            for keys, i, m in self.KEYS_MOV:
                if key in keys:
                    self.speed_vector[i] += (-m)
                    self.speed_vector[i] = sign(self.speed_vector[i])
                    break

        if event.type == pygame.KEYDOWN:
            if event.key in self.KEYS_BOMB:
                if self.current_bombs_number < self.bombs_number:
                    if self.field_object.can_place_bomb(self.tile):
                        self.current_bombs_number += 1
                        self.game_object.play('effect', self.SOUND_BOMB)
                        if self.has_detonator:
                            self.bombs_with_detonator.append(BombWithoutTimer(self, self.tile, self.bombs_power))
                        else:
                            Bomb(self, self.tile, self.bombs_power)

        if event.type == pygame.KEYDOWN:
            if event.key in self.KEYS_DETONATE_BOMB:
                if self.has_detonator and \
                    len(self.bombs_with_detonator) != 0:
                    deleting_bomb = self.bombs_with_detonator.pop(0)
                    deleting_bomb.blow_up()

    def process_draw_animation(self):
        p = Point(self.real_pos)
        rect = (p.x, p.y - (self.image_size[1] - self.real_size[1])), self.image_size
        self.game_object.screen.blit(self.animation.current_image, rect)

    def hurt(self, from_enemy):
        self.disable()
        self.game_object.play('effect', 'lose')

        if self.lives == 0:
            self.field_object.game_over()
        else:
            self.lives -= 1
            self.field_object.lose()
