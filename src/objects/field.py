from math import ceil
from os import mkdir
from os.path import exists
from random import randint, choice
from time import strftime

import pygame

from src.objects.base_classes.drawable_object import DrawableObject
from src.objects.base_classes.entity import Entity
from src.objects.enemies import ENEMIES
from src.objects.items import ITEMS, Door
from src.objects.tiles import TILES, CATEGORY
from src.utils.animation import SimpleAnimation
from src.utils.constants import Path
from src.utils.decorators import protect
from src.utils.vector import Point


class Stage:
    SOFT_WALL_NUMBER = 60
    UPGRADES_NUMBER = 1
    TIME = 180
    ON_TIMEOUT = (0, 0, 30)

    def __init__(self, field_size, name, enemies, soft_wall_number=SOFT_WALL_NUMBER, upgrades_number=UPGRADES_NUMBER,
                 time=TIME, on_timeout=ON_TIMEOUT):
        self.field_size = field_size
        self.name = name
        self.soft_wall_number = soft_wall_number
        self.enemies = enemies  # see -> src.objects.enemies.ENEMIES
        self.upgrades_number = upgrades_number
        self.time = time
        self.on_timeout = on_timeout


class Field(DrawableObject):
    """
    В Field сосредоточена основная информация об игровых объектах.
    grid - двумерный список для статичных объектов,
    остальное - entities.
    """
    DRAW_GRID = False
    LINE_WIDTH = 1  # ширина линии при отрисовки

    TILE_EMPTY = 0
    TILE_WALL = 1
    TILE_SOFT_WALL = 2
    TILE_UNREACHABLE_EMPTY = 3

    FIELD_SIZE = 31, 13
    STAGES = (
        Stage(FIELD_SIZE, "Stage 1", (6, 0, 0)),
        Stage(FIELD_SIZE, "Stage test 0", (1, 1, 1), 50, 999),
        Stage(FIELD_SIZE, "Stage HELL", (1, 0, 0), 50, 999, 10, (0, 0, 30)),
        Stage((9, 7), "Stage test 2", (1, 0, 0), 2),
        Stage((9, 7), "Stage test 3", (1, 1, 0), 3),
        Stage((9, 7), "Stage test 4", (1, 1, 0), 4),
    )

    def __init__(self, game_object, pos: Point, tile_size: tuple, field_size: tuple = FIELD_SIZE):
        """
        Создание поля.
        :param game_object: объект класса Game, которому принадлежит поле
        :param pos: реальная позиция левого верхнего угла поля
        :param field_size: размер поля в клетках (по ширине и высоте)
        :param tile_size: реальный размер клетки в пикселях (по ширине и высоте)
        :type game_object: Game
        :type pos: Point
        :type field_size: tuple
        :type tile_size: tuple
        """
        super().__init__(game_object)

        self.pos = Point(pos)
        self.field_size = tuple(field_size)
        self.tile_size = tuple(tile_size)

        self.current_stage = 0

        self.entities = []  # Список сущностей, принадлежащих этому полю
        self.players = []  # Список игроков
        self.grid = None  # Двумерный список — типы клеток

        self.reload_animations()

    @property
    def size(self):
        return self.field_size

    @property
    def width(self):
        return self.field_size[0]

    @property
    def height(self):
        return self.field_size[1]

    @property
    def real_size(self):
        w, h = self.tile_size
        return self.width * w, self.height * h

    def grid_init(self):
        """
        Заполнение неразрущаемыми стенами границы и остальное через одну клетку
        0 - пустота, 1 - стена
        """
        # Создание двумерного списка, заполненного нулями:
        self.grid = [[Field.TILE_EMPTY] * self.width for _ in range(self.height)]

        # Создание стен по границам
        for i in range(0, self.width):
            self.grid[0][i] = Field.TILE_WALL
            self.grid[-1][i] = Field.TILE_WALL

        for j in range(0, self.height):
            self.grid[j][0] = Field.TILE_WALL
            self.grid[j][-1] = Field.TILE_WALL

        # Создание стен через одну
        for i in range(2, self.height, 2):
            for j in range(2, self.width, 2):
                self.grid[i][j] = Field.TILE_WALL

    def generate_field(self):
        stage = self.STAGES[self.current_stage]

        self.field_size = stage.field_size
        self.soft_number = stage.soft_wall_number
        self.upgrade_numbers = stage.upgrades_number
        self.time = stage.time
        self.has_door = False
        self.timeout = False
        for e in self.entities:
            e.disable()
        self.entities = [] + self.players
        self.enemies_count = 0
        self.has_door = False

        self.grid_init()

        empty_tiles = []

        for h in range(0, self.height):
            for w in range(0, self.width):
                if self.at(w, h) == Field.TILE_EMPTY:
                    empty_tiles.append((w, h))

        buffer = [(1, self.height - 2), (1, self.height - 3), (2, self.height - 2)]
        for b in buffer:
            if b in empty_tiles:
                empty_tiles.remove(b)

        for _ in range(self.soft_number):
            pos = empty_tiles.pop(randint(0, len(empty_tiles) - 1))

            self.grid[pos[1]][pos[0]] = self.TILE_SOFT_WALL

        self.generate_enemies(stage.enemies, buffer)

    def generate_enemies(self, enemies, buffer=()):
        empty_tiles = []

        for h in range(0, self.height):
            for w in range(0, self.width):
                if self.at(w, h) == Field.TILE_EMPTY:
                    empty_tiles.append((w, h))

        for b in buffer:
            if b in empty_tiles:
                empty_tiles.remove(b)

        for e_type, e_number in enumerate(enemies):
            if e_number <= 0: continue

            for _ in range(e_number):
                pos = empty_tiles.pop(randint(0, len(empty_tiles) - 1))

                ENEMIES[e_type](self, pos)

    def next_stage(self):
        self.current_stage += 1
        if self.current_stage + 1 > len(self.STAGES):
            self.game_over(True)
            return
        self.reset_stage(False)

    def reset_stage(self, full=True, load=False):
        self.generate_field()
        self.reset_players(full)
        if not load:
            self.save_stage()
        else:
            self.load()
        self.game_object.set_scene(self.game_object.GAME_SCENE_INDEX, 2000, self.STAGES[self.current_stage].name)
        self.start_time = pygame.time.get_ticks()

    def game_over(self, win=False):
        self.current_stage = 0
        self.save_score()
        with open(Path.STAGE_SAVE, 'w') as f:
            pass

        # TODO: sound gamewin
        message = "GAME OVER"
        if win:
            message = "WIN"
        self.game_object.set_scene(self.game_object.MENU_SCENE_INDEX, 3000, message)

    def reset_players(self, full):
        for p in self.players:
            p.enable()
            p.reset(full)

    def process_draw_tiles(self):
        """
        Отрисовка самого поля, т.е. его клеток.
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                tile_real_pos = [self.pos[k] + (j, i)[k] * self.tile_size[k] for k in range(2)]
                rect = tile_real_pos, self.tile_size

                tile_type = self.grid[i][j]

                tile = TILES[tile_type]
                if self.tile_images and tile.image_name and TILES[0].image_name:
                    self.game_object.screen.blit(self.tile_images[TILES[0].image_name], rect)
                    if tile_type > 0:
                        self.game_object.screen.blit(self.tile_images[tile.image_name], rect)
                else:
                    pygame.draw.rect(self.game_object.screen, tile.color, rect, 0)

                if Field.DRAW_GRID:
                    pygame.draw.rect(self.game_object.screen, (0, 0, 0), rect, Field.LINE_WIDTH)

    def process_draw_entities(self):
        """
        Отрисовка всех сущностей, принадлежащих этому полю
        """
        for e in reversed(self.entities):
            e.process_draw()

    def process_draw(self):
        self.process_draw_tiles()
        self.process_draw_entities()

    def process_logic(self):
        if not self.timeout:
            if pygame.time.get_ticks() - self.start_time > self.time * 1000:
                self.game_object.sounds['effect']['timeout'].play()  # TODO: timeout sound
                self.timeout = True
                buffer = []
                for player in self.players:
                    x, y = player.tile
                    rad = 1
                    for dx in range(-rad, rad + 1):
                        for dy in range(-rad, rad + 1):
                            buffer.append(((x + dx), (y + dy)))
                self.generate_enemies(self.STAGES[self.current_stage].on_timeout, buffer)
        for e in self.entities:
            e.process_logic()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Exit from game to menu")
                self.save_stage()
                self.game_object.set_scene(self.game_object.MENU_SCENE_INDEX)
                return
        for e in self.entities:
            e.process_event(event)

    def add_entity(self, entity):
        self.entities.append(entity)

    def delete_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def destroy_wall(self, x, y, delay):
        """
        Запускает уничтожение клетки (x, y) за delay миллисекунд
        """
        self.grid[y][x] = Field.TILE_UNREACHABLE_EMPTY
        BreakingWall(self, Point(x, y), delay)

    def load_images(self):
        self.tile_images = {}
        if self.game_object.images:
            for key in self.game_object.images[CATEGORY]:
                self.tile_images[key] = pygame.transform.scale(self.game_object.images[CATEGORY][key], self.tile_size)
                print("FIELD: resized '{}'".format(key))

    def __getitem__(self, item):
        return self.grid.__getitem__

    def __setitem__(self, key, value):
        return self.grid.__setitem__

    def at(self, *args):
        x, y = 0, 0
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        return self.grid[y][x]

    def reload_animations(self):
        self.load_images()
        for e in self.entities:  # TODO: reload
            e.reload_animations()

    def empty_at(self, pos):  # TODO: bomb place
        from src.objects.bomb import Bomb

        pos = tuple(pos)

        for e in self.entities:
            if type(e) is Bomb:
                if e.tile == pos:
                    return False

        return True

    def save_data(self):
        if not exists(Path.SAVE_DIR):
            mkdir(Path.SAVE_DIR)

        self.save_stage()
        self.save_score()

    def save_stage(self):
        with open(Path.STAGE_SAVE, 'w') as f:
            print(self.current_stage, file=f)
            print(self.players[0].score, file=f)
            print(self.players[0].lives, file=f)
            print(self.players[0].speed_value, file=f)
            print(self.players[0].bombs_power, file=f)
            print(self.players[0].max_bombs_number, file=f)

    def save_score(self):
        highscores = []
        if exists(Path.HIGHSCORES_SAVE):
            with open(Path.HIGHSCORES_SAVE, 'r') as f:
                for line in f:
                    score, other = line.strip().split(maxsplit=1)
                    score = int(score)
                    highscores.append((score, other))

        if self.players[0].score > 0:
            highscores.append((self.players[0].score, strftime('%x %X')))

        highscores.sort(reverse=True)
        highscores = ["{} {}\n".format(*i) for i in highscores]

        with open(Path.HIGHSCORES_SAVE, 'w') as f:
            f.writelines(highscores)

    def load(self):
        if exists(Path.STAGE_SAVE):
            with open(Path.STAGE_SAVE, 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    lines = list(map(float, lines))
                    self.current_stage, self.players[0].score, self.players[0].lives, self.players[0].speed_value, self.players[
                        0].bombs_power, self.players[0].max_bombs_number = lines
                    self.current_stage = int(self.current_stage)
                    self.players[0].score = int(self.players[0].score)
                    self.players[0].lives = int(self.players[0].lives)
                    self.players[0].bombs_power = int(self.players[0].bombs_power)
                    self.players[0].max_bombs_number = int(self.players[0].max_bombs_number)


class BreakingWall(Entity):
    """
    Сущность уничтожающейся стены.
    Нужна для анимации разрушения.
    """
    SPRITE_CATEGORY = CATEGORY
    SPRITE_NAMES = ('break_wall', 'break_wall1', 'break_wall2', 'break_wall3')
    COLOR = TILES[Field.TILE_SOFT_WALL].color

    def __init__(self, field_object, pos: Point, delay):
        x, y = pos
        self.delay = delay
        super().__init__(field_object, Point(int(x), int(y)))

        self.reload_animations()
        self.start_time = pygame.time.get_ticks()

    @protect
    def create_animation(self):
        if not self.game_object.images: return

        sprites = [self.field_object.tile_images[i] for i in BreakingWall.SPRITE_NAMES]
        animation_delay = ceil(self.delay / len(sprites))
        animation_dict = {'breaking': (animation_delay, sprites)}
        return SimpleAnimation(animation_dict, 'breaking')

    def on_timeout(self):
        self.disable()
        x, y = self.pos

        if self.field_object.soft_number == 1 and not self.field_object.has_door:
            self.field_object.has_door = True
            Door(self.field_object, self.pos)
        else:
            r = randint(1, self.field_object.soft_number)
            if r <= self.field_object.upgrade_numbers + (not self.field_object.has_door):
                if not self.field_object.has_door and r == 1:
                    self.field_object.has_door = True
                    Door(self.field_object, self.pos)
                else:
                    self.field_object.upgrade_numbers -= 1
                    choice(ITEMS)(self.field_object, self.pos)

        self.field_object.grid[y][x] = Field.TILE_EMPTY
        self.field_object.soft_number -= 1

        self.field_object.delete_entity(self)

    def process_draw_animation(self):
        self.game_object.screen.blit(self.animation.current_image, (self.real_pos, self.real_size))

    def additional_logic(self):
        if pygame.time.get_ticks() - self.start_time >= self.delay:
            self.on_timeout()
