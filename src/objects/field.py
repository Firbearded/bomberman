from math import ceil
from random import randint

import pygame

from src.objects.base_classes import DrawableObject
from src.objects.entity import Entity
from src.objects.tiles import TILES, CATEGORY
from src.utils.animation import SimpleAnimation
from src.utils.vector import Point


class Field(DrawableObject):
    """
    В Field сосредоточена основная информация об игровых объектах.
    grid - двумерный список для статичных объектов,
    остальное - entities.
    """
    DRAW_GRID = False
    LINE_WIDTH = 1  # ширина линии при отрисовки

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

        self.pos = Point()
        self.pos.copy_from(pos)
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
        Заполнение стенами границы и остальное через одну клетку
        0 - пустота, 1 - стена...
        """
        # Создание двумерного списка, заполненного нулями:
        self.grid = [[0] * self.width for _ in range(self.height)]

        # Создание стен по границам
        for i in range(0, self.width):
            self.grid[0][i] = 1
            self.grid[-1][i] = 1

        for j in range(0, self.height):
            self.grid[j][0] = 1
            self.grid[j][-1] = 1

        # Создание стен через одну
        for i in range(2, self.height, 2):
            for j in range(2, self.width, 2):
                self.grid[i][j] = 1

    def rand_fill(self, type_=2, n=20):  # TODO: переработать
        c = 0
        while c < n:
            i = randint(1, self.height - 1)
            j = randint(1, self.width - 1)
            if self.grid[i][j] == 0:
                c += 1
                self.grid[i][j] = type_

    def process_draw_tiles(self):
        """
        Отрисовка самого поля, те его клеток.
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):  # TODO Временное решение:
                tile_pos = [self.pos[k] + (j, i)[k] * self.tile_size[k] for k in range(2)]
                rect = tile_pos, self.tile_size
                tile_index = self.grid[i][j]

                self.game_object.screen.blit(self.tile_images[TILES[0].image_name], rect)  # Траву сзади всех рисуем
                if tile_index == 0: continue

                tile = TILES[tile_index]
                if tile.image_name:
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
        # TODO: анимации разрушения стены
        self.grid[y][x] = 3
        BreakingWall(self, Point(x, y), delay)

    def load_images(self):
        for key in self.game_object.images[CATEGORY]:
            self.tile_images[key] = pygame.transform.scale(self.game_object.images[CATEGORY][key], self.tile_size)
            print("FIELD: resized '{}'".format(key))

    def __getitem__(self, item):
        return self.grid.__getitem__

    def __setitem__(self, key, value):
        return self.grid.__setitem__


class BreakingWall(Entity):
    def __init__(self, field, pos: Point, delay):
        x, y = pos
        super().__init__(field, Point(int(x), int(y)), (1, 1))
        self.delay = delay

        self.anim = self.create_anim()
        self.start_time = pygame.time.get_ticks()

    def create_anim(self):
        imgs = ['break_wall', 'break_wall1', 'break_wall2', 'break_wall3']
        imgs = [self.field.tile_images[i] for i in imgs]
        dl = ceil(self.delay / len(imgs))
        anim_dict = {'breaking': (dl, imgs)}
        return SimpleAnimation(anim_dict, 'breaking')

    def process_draw(self):
        self.game_object.screen.blit(self.anim.current_image, (self.real_pos, self.real_size))

    def process_logic(self):
        self.anim.process_logic()
        if pygame.time.get_ticks() - self.start_time >= self.delay:
            self.enabled = False
            x, y = self.pos
            self.field.grid[y][x] = 0
            self.field.delete_entity(self)
