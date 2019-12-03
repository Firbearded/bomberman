import pygame

from src.objects.base_classes.entity import Entity
from src.objects.bomb import Bomb, BombRemote
from src.objects.supporting.animation import SimpleAnimation
from src.utils.constants import Color, Sounds
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
            'down': ('bb_walking1_down', 'bb_walking2_down',),
            'horizontal': ('bb_h1', 'bb_h2', 'bb_h3', 'bb_h4', 'bb_h5', 'bb_h6', 'bb_h7',),
        }
    }

    SOUND_BOMB = Sounds.Effects.bomb_place.value

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
    SPEED_DELTA = 0.2
    LIVES = 2
    BOMBS_POWER = 2
    BOMBS_NUMBER = 1

    MAX_SPEED_VALUE = 5
    MAX_LIVES = 20
    MAX_BOMBS_POWER = 10
    MAX_BOMBS_NUMBER = 10

    def __init__(self, field_object):
        super().__init__(field_object, Point(0, 0), (1, 1))

        self.reset(full=True)
        self.animation = self.create_animation()

    def reset(self, full=False):
        if full:
            self.speed_vector = Vector()
            self.speed_value = self.SPEED_VALUE
            self._score = 0
            self._current_lives = self.LIVES
            self._bombs_power = self.BOMBS_POWER
            self._bombs_number = self.BOMBS_NUMBER
            self._has_detonator = False

        self.pos = Point(1, self.field_object.height - 2)
        self._direction = Vector(0, 1)
        self._is_moving = False

        self._active_bombs_number = 0
        self._bombs_remote = []
        self._has_wallpass = False
        self._has_flamepass = False
        self._has_mystery = False
        self.enable()
        self.show()

    # ================= Для анимаций ==================
    def get_state(self):
        state = 'walking' if self._is_moving else 'standing'
        d = list(self._direction)
        if 0 not in d:
            d[1] = 0
        direction = self.TEMP_DIR[tuple(d)]
        return '{}_{}'.format(state, direction)

    @protect
    def create_animation(self):
        if not self.game_object.images: return

        animation_dict = {}
        animation_delay = 100

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
                        k = w / (self.real_size[0] * 1.4)
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

    def process_draw_animation(self):
        p = Point(self.real_pos)
        rect = (p.x, p.y - (self.image_size[1] - self.real_size[1])), self.image_size
        self.game_object.screen.blit(self.animation.current_image, rect)

    # ============== Движеник и коллизии ==============
    def corner_fixing(self, speed_vector):
        """ Метод, где мы обрабатываем столкновения в углы и обход их """
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
        """ Метод на обработку коллизий со стенами """
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
        """ Движение, вызов обработки столкновений и изменение состояния анимации """
        normalized_speed_vector, is_fixing = self.corner_fixing(self.speed_vector.copy)

        if not is_fixing:
            normalized_speed_vector = self.wall_collisions(normalized_speed_vector)

        if 0 not in tuple(normalized_speed_vector):
            normalized_speed_vector[0] = 0

        self.pos = self.pos + normalized_speed_vector

        if self.animation:
            self._is_moving = bool(normalized_speed_vector)
            if self._is_moving:
                self._direction = normalized_speed_vector.united
            self.animation.set_state(self.get_state())

    # =============== Обработка нажатий ================
    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            for keys, i, m in self.KEYS_MOV:
                if key in keys:
                    self.speed_vector[i] += m
                    self.speed_vector[i] = sign(self.speed_vector[i])
                    break
            if event.key in self.KEYS_BOMB:
                if self._active_bombs_number < self._bombs_number:
                    if self.field_object.can_place_bomb(self.tile):
                        self.game_object.mixer.channels['effects'].sound_play(self.SOUND_BOMB)
                        if self._has_detonator:
                            self._bombs_remote.append(
                                BombRemote(self, self.tile, self.bombs_power))
                        else:
                            Bomb(self, self.tile, self._bombs_power)
            if event.key in self.KEYS_DETONATE_BOMB:
                if self._has_detonator and self._bombs_remote:
                    self._bombs_remote.pop(0).on_timeout()

        if event.type == pygame.KEYUP:
            key = event.key
            for keys, i, m in self.KEYS_MOV:
                if key in keys:
                    self.speed_vector[i] += (-m)
                    self.speed_vector[i] = sign(self.speed_vector[i])
                    break

    # =============== Улучшения ================
    def bomb_up(self):
        self._bombs_number = min(self._bombs_number + 1, self.MAX_BOMBS_NUMBER)

    def power_up(self):
        self._bombs_power = min(self._bombs_power + 1, self.MAX_BOMBS_POWER)

    def speed_up(self):
        self.speed_value = min(self.speed_value + self.SPEED_DELTA, self.MAX_SPEED_VALUE)

    def life_up(self):
        self._current_lives = min(self._current_lives + 1, self.MAX_LIVES)

    def get_detonator(self):
        self._has_detonator = True

    def get_wallpass(self):
        self._has_wallpass = True

    def get_flamepass(self):
        self._has_flamepass = True

    def get_mystery(self):
        self._has_mystery = True

    # =============== Остальное ================
    def hurt(self, from_enemy):
        """ Когда больно """
        self.disable()

        if self._current_lives == 0:
            self.field_object.game_over()
        else:
            self._current_lives -= 1
            self.field_object.round_lose()

    @property
    def score(self):
        return self._score

    def add_score(self, score):
        self._score += int(score)

    @property
    def current_lives(self):
        return self._current_lives

    @property
    def bombs_number(self):
        return self._bombs_number

    @property
    def bombs_power(self):
        return self._bombs_power

    def inc_active_bombs_number(self):
        self._active_bombs_number += 1

    def dec_active_bombs_number(self):
        self._active_bombs_number -= 1

    def _to_save(self):
        return "_score", "_current_lives", "_bombs_power", "_bombs_number", "_has_detonator"

    def to_str(self):
        s = " ".join(map(str, [vars(self)[v] for v in self._to_save()]))
        return s

    def from_str(self, string):
        string = string.strip()
        vdict = vars(self)
        for var, s in zip(self._to_save(), string.split()):
            vdict[var] = type(vdict[var])(s)
