from math import ceil
from random import randint

import pygame

from src.objects.base_classes.drawable_object import DrawableObject
from src.objects.base_classes.entity import Entity
from src.objects.tiles import TILES, CATEGORY
from src.utils.animation import SimpleAnimation
from src.utils.decorators import protect
from src.utils.vector import Point


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
    TILE_BREAKABLE_WALL = 2
    TILE_UNREACHABLE_EMPTY = 3

    def __init__(self, game_object, pos: Point, field_size: tuple, tile_size: tuple):
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

        self.entities = []  # Список сущностей, принадлежащих этому полю
        self.grid = None  # Двумерный список — типы клеток
        self.tile_images = {}  # Словарь для маштабированных изображений

        self.load_images()
        self.grid_init()

    @property
    def size(self):
        return self.field_size

    @property
    def width(self):
        return self.field_size[0]

    @property
    def height(self):
        return self.field_size[1]

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

    def rand_fill(self, type_=TILE_BREAKABLE_WALL, n=20):  # TODO: переработать
        c = 0
        while c < n:
            i = randint(1, self.height - 1)
            j = randint(1, self.width - 1)
            if self.grid[i][j] == 0:
                c += 1
                self.grid[i][j] = type_

    def process_draw_tiles(self):
        """
        Отрисовка самого поля, т.е. его клеток.
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):  # TODO Временное решение:
                tile_real_pos = [self.pos[k] + (j, i)[k] * self.tile_size[k] for k in range(2)]
                rect = tile_real_pos, self.tile_size

                tile_type = self.grid[i][j]

                tile = TILES[tile_type]
                if self.tile_images and tile.image_name and TILES[0].image_name:
                    self.game_object.screen.blit(self.tile_images[TILES[0].image_name], rect)
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
        for e in self.entities:
            e.process_logic()

    def process_event(self, event):
        for e in self.entities:
            e.process_event(event)

    def add_entity(self, entity):
        self.entities.append(entity)

    def delete_entity(self, entity):
        self.entities.remove(entity)

    def destroy_wall(self, x, y, delay):
        """
        Запускает уничтожение клетки (x, y) за delay миллисекунд
        """
        self.grid[y][x] = Field.TILE_UNREACHABLE_EMPTY
        BreakingWall(self, Point(x, y), delay)

    def load_images(self):
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


class BreakingWall(Entity):
    """
    Сущность уничтожающейся стены.
    Нужна для анимации разрушения.
    """
    SPRITE_NAMES = ('break_wall', 'break_wall1', 'break_wall2', 'break_wall3')
    COLOR = TILES[Field.TILE_BREAKABLE_WALL].color

    def __init__(self, field_object, pos: Point, delay):
        x, y = pos
        super().__init__(field_object, Point(int(x), int(y)))
        self.delay = delay

        self.animation = self.create_animation()
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
        self.field_object.grid[y][x] = Field.TILE_EMPTY
        self.field_object.delete_entity(self)

    def process_draw_animation(self):
        self.game_object.screen.blit(self.animation.current_image, (self.real_pos, self.real_size))

    def additional_logic(self):
        if pygame.time.get_ticks() - self.start_time >= self.delay:
            self.on_timeout()
