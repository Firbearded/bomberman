import os
import sys
from random import randint, choice
from time import strftime

import pygame

from src.objects.base_classes.base_objects.geometric_object import GeometricObject
from src.objects.base_classes.base_objects.pygame_object import PygameObject
from src.objects.base_classes.base_objects.timer_object import TimerObject
from src.objects.enemies import ENEMIES
from src.objects.field.breaking_wall import BreakingWall
from src.objects.field.stage import Stage
from src.objects.field.tiles import TILES, CATEGORY
from src.objects.items import Door, DROP
from src.utils.constants import Path


class Field(PygameObject, GeometricObject):
    """
    В Field сосредоточена основная информация об игровых объектах.
    """
    LINE_WIDTH = 0  # ширина линии при отрисовки (0 - нет линии)
    _PLAYER_BUFFER = 3  # Ширина буфера для игрока (чтобы враги не появлялись рядом)
    ENEMIES_ON_DOOR = 0, 5, 0  # Выпадаемые враги со двери

    TILE_TYPES = \
        TILE_EMPTY, TILE_WALL, TILE_SOFT_WALL, TILE_UNREACHABLE_EMPTY = \
        0, 1, 2, 3

    _BACKGROUND_TILE_TYPE = TILE_EMPTY  # Клетка, которая на заднем фоне
    _BACKGROUND_TILE = TILES[_BACKGROUND_TILE_TYPE]

    KEYS_EXIT = (pygame.K_ESCAPE,)  # Кнопки на выход из игры

    STAGES = (  # Уровки игры (смотрите класс Stage)
        Stage(name="Stage 1", enemies=(6, 0, 0)),
        Stage(name="Stage test 0", enemies=(1, 1, 1), upgrades_number=999),
        Stage(name="Stage HELL", enemies=(1, 0, 0), upgrades_number=999, time=10),
        Stage(field_size=(9, 17), name="Enemy collision test 0", enemies=(5, 0, 0), soft_wall_number=10),
        Stage(field_size=(9, 7), name="Stage test 1", enemies=(0, 0, 0), soft_wall_number=1),
        Stage(field_size=(9, 7), name="Stage test 2", enemies=(1, 0, 0), soft_wall_number=3),
        Stage(field_size=(11, 11), name="Stage test 3", enemies=(2, 0, 0), soft_wall_number=4),
    )

    GAMEOVER_MSG = "GAME OVER"
    WIN_MSG = "WIN"
    SOUND_GAMEWIN = "gamewin"
    SOUND_TIMEOUT = 'timeout'

    def __init__(self, game_object, tile_size: tuple):
        PygameObject.__init__(self, game_object)
        GeometricObject.__init__(self)

        self._tile_size = tuple(tile_size)
        from src.objects.bomb import Fire
        from src.objects.bomb import Bomb
        from src.objects.base_classes.item import Item
        from src.objects.base_classes.enemy import Enemy
        from src.objects.player import Player

        self._grid = None  # Двумерный список — типы клеток
        self._field_size = (1, 1)  # Размеры поля
        self._entities = {}  # Список сущностей, принадлежащих этому полю
        self._class_priority = (Player, Enemy, Fire, Bomb, Item,)  # Приоритет классов на отрисовку (по убыванию)
        self._enemies_on_door = Field.ENEMIES_ON_DOOR

        self._soft_number = None
        self._upgrade_numbers = None
        self._has_door = None
        self._enemies = None
        self._extra_enemies = None

        self._current_stage_index = 0  # Индекс уровня
        self._entities_queue = []  # Очередь сущностей на добавление. Нельзя добавлять сущности в словарь во время
        # использования этого же словаря

        self.timer = TimerObject(0)
        self.timer.on_timeout = self.on_timeout

        self.load_images()

    @property
    def size(self):
        return self._field_size

    @property
    def width(self):
        return self._field_size[0]

    @property
    def height(self):
        return self._field_size[1]

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def real_size(self):
        """ Реальный размер поля (в пикселях) """
        w, h = self.tile_size
        return self.width * w, self.height * h

    def add_entity(self, entity):
        """ Добвить сущность в поле (на самом деле добавить в очередь) """
        cls = type(entity)

        for c in self._class_priority:
            if issubclass(cls, c):
                cls = c
                break

        self._entities_queue.append((cls, entity))

    def flush_enitites(self):
        """ А тут добавить все сущности из очереди в поле """
        for cls, entity in self._entities_queue:
            if cls not in self._entities:
                self._entities[cls] = []

            if entity not in self._entities[cls]:
                self._entities[cls].append(entity)

        self._entities_queue.clear()

    def delete_entity(self, entity):
        """ Удалить сущность из поля """
        for cls in self._entities:
            if entity in self._entities[cls]:
                self._entities[cls].remove(entity)
                return

    def get_entities(self, cls):
        """ Получить сущности одного класса """
        if cls in self._entities:
            return self._entities[cls]
        return []

    @property
    def main_player(self):
        """ Основной игрок (если будет мультиплеер, то там будет один основной, а остальные - дополнительные для
        каждого клиента) """
        from src.objects.player import Player
        return self._entities[Player][0]

    def tile_at(self, *args):
        """
        Получить класс клетки в данной позиции (x, y)
        Аргументы: или tile_at(x, y),
                   или tile_at(Point(x, y)),
                   или tile_at((x, y))...
        :rtype: Tile
        """
        x, y = 0, 0
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        x %= self.width
        y %= self.height
        return TILES[self._grid[y][x]]

    def tile_set(self, *args):
        """
        Установить другую клетку (v) на позицию (x, y).
        Аргументы: или tile_set(x, y, v),
                   или tile_set(Point(x, y), v),
                   или tile_set((x, y), v)...
        """
        x, y = 0, 0
        v = 0
        if len(args) == 2:
            x, y = args[0]
            v = args[1]
        elif len(args) == 3:
            x, y, v = args
        assert v in Field.TILE_TYPES
        x %= self.width
        y %= self.height
        self._grid[y][x] = v

    def can_place_bomb(self, pos):
        """ Проверка на то, можно ли поставить бомбу в клетку на позиции pos """
        from src.objects.bomb import Bomb

        pos = tuple(pos)

        for b in self.get_entities(Bomb):
            if tuple(b.tile) == pos:
                return False

        return True

    def destroy_wall(self, pos, delay):
        """ Запускает анимацию уничтожения клетки pos за delay миллисекунд. """
        BreakingWall(self, pos, delay)

    def try_drop_item(self, pos):
        """ Дроп предмета на позиции pos (если рандом) """
        if self._soft_number == 1 and not self._has_door:
            self._has_door = True
            Door(self, pos)
        else:
            r = randint(1, self._soft_number)
            if r <= self._upgrade_numbers + (not self._has_door):
                if not self._has_door and r == 1:
                    self._has_door = True
                    Door(self, pos)
                else:
                    self._upgrade_numbers -= 1
                    choice(DROP)(self, pos)

    def load_images(self):
        """ Загрузка и resize изображений клеток для дальнейшего использования """
        self.tile_images = {}
        if self.game_object.images:
            for key in self.game_object.images[CATEGORY]:
                self.tile_images[key] = pygame.transform.scale(self.game_object.images[CATEGORY][key], self.tile_size)
                print("FIELD: resized '{}'".format(key))

    @property
    def current_stage(self):
        """
        :rtype: Stage
        """
        return self.STAGES[self._current_stage_index]

    def _get_empty_tiles(self):
        """ Получить пустые клетки """
        empty_tiles = []

        for h in range(0, self.height):
            for w in range(0, self.width):
                if self.tile_at(w, h).empty:
                    empty_tiles.append((w, h))

        return empty_tiles

    def _get_player_buffer(self):
        """ Получить клетки, которые входят в буффер игроков """
        from src.objects.player import Player

        buffer = []
        for player in self.get_entities(Player):
            x, y = player.tile
            rad = Field._PLAYER_BUFFER
            for dx in range(-rad, rad + 1):
                for dy in range(-rad, rad + 1):
                    buffer.append(((x + dx), (y + dy)))

        return buffer

    def _get_empty_tiles_without_buffer(self):
        """ Пустые клетки без буффера игроков """
        empty_tiles = self._get_empty_tiles()

        for b in self._get_player_buffer():
            if b in empty_tiles:
                empty_tiles.remove(b)

        return empty_tiles

    def reset_stage(self, full=False):
        """ Сброс уровня """
        stage = self.current_stage
        self._field_size = stage.field_size
        self._start_soft_number = stage.soft_wall_number
        self._soft_number = self._start_soft_number
        self._upgrade_numbers = stage.upgrades_number
        self._enemies = stage.enemies
        self.timer.delay = stage.time * 1000
        self._extra_enemies = stage.enemies_on_timeout
        self._has_door = False
        for cls in self._entities:
            from src.objects.player import Player
            if cls is not Player:
                for e in self._entities[cls]:
                    e.disable()
                    e.hide()
                self._entities[cls] = []
            else:
                for e in self._entities[cls]:
                    e.reset(full=full)

    def grid_init(self):
        """ Заполнение неразрущаемыми стенами границы и остальное через одну клетку """

        # Создание двумерного списка, заполненного пустыми клетками:
        self._grid = [[Field.TILE_EMPTY] * self.width for _ in range(self.height)]

        # Создание стен по границам
        for i in range(0, self.width):
            self._grid[0][i] = Field.TILE_WALL
            self._grid[-1][i] = Field.TILE_WALL

        for j in range(0, self.height):
            self._grid[j][0] = Field.TILE_WALL
            self._grid[j][-1] = Field.TILE_WALL

        # Создание стен через одну
        for i in range(2, self.height, 2):
            for j in range(2, self.width, 2):
                self._grid[i][j] = Field.TILE_WALL

    def generate_soft_walls(self):
        """ Случайная генерация ломающихся стен """
        empty_tiles = self._get_empty_tiles_without_buffer()

        for _ in range(self._start_soft_number):
            pos = empty_tiles.pop(randint(0, len(empty_tiles) - 1))
            self.tile_set(pos, Field.TILE_SOFT_WALL)

    def generate_enemies(self, enemies, pos=None):
        """ Генерация мобов """
        if pos is None:
            empty_tiles = self._get_empty_tiles_without_buffer()

            for e_type, e_number in enumerate(enemies):
                if e_number <= 0: continue

                for _ in range(e_number):
                    ENEMIES[e_type](self, empty_tiles.pop(randint(0, len(empty_tiles) - 1)))
        else:
            for e_type, e_number in enumerate(enemies):
                if e_number <= 0: continue

                for _ in range(e_number):
                    ENEMIES[e_type](self, pos)

    def start_game(self, new_game, restart=True):
        """ Метод дял Начала игры """
        if not new_game:
            self.load(full=not restart)
        self.reset_stage(full=new_game)
        self.grid_init()
        self.generate_soft_walls()
        self.generate_enemies(self._enemies)
        if new_game:
            self.save_stage()
        self.timer.start()

    def next_stage(self):
        """ Переключение на следующий уровень """
        self._current_stage_index += 1
        if self._current_stage_index + 1 > len(Field.STAGES):
            self.game_over(win=True)
            return
        self.save_stage()
        self.start_game(new_game=False)
        self.game_object.set_scene(self.game_object.GAME_SCENE_INDEX, 3000, self.current_stage.name)

    def game_over(self, win=False):
        """ Окончание игры (полный проигрыш или выигрыш) """
        self._current_stage_index = 0
        self.save_score()
        self.start_game(True, False)

        if win:
            self.game_object.stop_all()
            self.game_object.play('effect', self.SOUND_GAMEWIN)
        self.game_object.set_scene(self.game_object.MENU_SCENE_INDEX, 3000, (Field.GAMEOVER_MSG, Field.WIN_MSG)[win])

    def lose(self):
        """ Проигрыш (не полный, жизни ещё есть) """
        self.game_object.set_scene(self.game_object.GAME_SCENE_INDEX, 3000, self.current_stage.name)

    def save_score(self):
        """ Сохранить счёт """
        highscores = get_highscores()
        player = self.main_player

        second_str = strftime('%x %X')

        highscores.append((player.score, second_str))
        highscores.sort(reverse=True)
        highscores = ["{} {}\n".format(c, s) for c, s in highscores]

        save_highscores(highscores)

    def save_stage(self, on_exit=False):
        """ Сохранить уровень """
        check_dir(Path.SAVE_DIR)
        if on_exit:
            self.load()

        with open(Path.STAGE_SAVE, 'w') as f:
            sys.stdout = f
            print(self._current_stage_index)

            player = self.main_player
            print(player.score)
            print(player.lives)
            print(player.speed_value)
            print(player.bombs_number)
            print(player.bombs_power)

        sys.stdout = sys.__stdout__

    def load(self, full=False):
        """ Загрузить уровень """
        check_dir(Path.SAVE_DIR)
        if os.path.exists(Path.STAGE_SAVE):
            with open(Path.STAGE_SAVE, 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    player = self.main_player
                    lines = list(map(float, lines))
                    self._current_stage_index, player.score, lives, player.speed_value, \
                    player.bombs_number, player.bombs_power = lines
                    self._current_stage_index = int(self._current_stage_index)
                    player.score = int(player.score)
                    if full:
                        player.lives = int(lives)
                    player.bombs_number = int(player.bombs_number)
                    player.bombs_power = int(player.bombs_power)

    def on_timeout(self):
        """ Метод, когда время на таймере закончится """
        self.game_object.play('effect', self.SOUND_TIMEOUT)
        self.generate_enemies(self._extra_enemies)

    # ======================== Эвенты ========================
    def additional_event(self, event):
        """ Проверка на выход из игры в меню """
        if event.type == pygame.KEYDOWN:
            if event.key in Field.KEYS_EXIT:
                print("Exit from game to menu")
                self.save_stage(on_exit=True)
                self.game_object.set_scene(self.game_object.MENU_SCENE_INDEX)
                return

    def process_event(self, event):
        """ Обработка событий """
        self.additional_event(event)

        for cls in self._entities:
            for e in self._entities[cls]:
                e.process_event(event)

    # ======================== Логика ========================
    def process_logic(self):
        """ Логика таймера, обработка логики и добавление сущностей из очереди """
        self.timer.timer_logic()
        for cls in self._entities:
            for e in self._entities[cls]:
                e.process_logic()

        self.flush_enitites()

    # ======================= Отрисовка ======================
    def process_draw_tiles(self):
        """ Отрисовка самого поля, т.е. его клеток. """
        for h in range(self.height):
            for w in range(self.width):
                grid_start_pos = self.pos

                if self.width * self.tile_size[0] < self.game_object.width:
                    grid_start_pos[0] = (self.game_object.width - self.width * self.tile_size[0]) / 2
                else:
                    grid_start_pos[0] = min(grid_start_pos[0], 0)
                    grid_start_pos[0] = max(grid_start_pos[0], self.game_object.width - self.width * self.tile_size[0])

                if self.height * self.tile_size[1] < self.game_object.height:
                    grid_start_pos[1] = (self.game_object.height - self.height * self.tile_size[1]) / 2
                else:
                    grid_start_pos[1] = min(grid_start_pos[1], 0)
                    grid_start_pos[1] = max(grid_start_pos[1],
                                            self.game_object.height - self.height * self.tile_size[1])

                tile_real_pos = [grid_start_pos[0] + w * self.tile_size[0], grid_start_pos[1] + h * self.tile_size[1]]

                rect = tile_real_pos, self.tile_size

                tile = self.tile_at(w, h)
                if self.tile_images and tile.image_name and Field._BACKGROUND_TILE.image_name:
                    # Если есть спрайты и названия спайтов у клеток, то рисуем текстуры
                    self.game_object.screen.blit(self.tile_images[Field._BACKGROUND_TILE.image_name], rect)
                    if tile is not Field._BACKGROUND_TILE:
                        self.game_object.screen.blit(self.tile_images[tile.image_name], rect)
                else:  # Иначе запасной план: рисуем квадраты
                    pygame.draw.rect(self.game_object.screen, tile.color, rect, 0)

                if Field.LINE_WIDTH > 0:
                    pygame.draw.rect(self.game_object.screen, (0, 0, 0), rect, Field.LINE_WIDTH)

    def process_draw_entities(self):
        """ Отрисовка всех сущностей, принадлежащих этому полю """
        other_keys = set(self._entities.keys()).difference(set(self._class_priority))
        for cls in tuple(reversed(self._class_priority)) + tuple(other_keys):
            if cls in self._entities:
                for e in reversed(self._entities[cls]):
                    e.process_draw()

    def process_draw(self):
        self.process_draw_tiles()
        self.process_draw_entities()


def check_dir(dir_path):
    """ Проверка на то, существует ли папка. Если нет, то создаём"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_highscores():
    """ Загрузка всех результатов """
    check_dir(Path.SAVE_DIR)

    highscores = []
    if os.path.exists(Path.HIGHSCORES_SAVE):
        with open(Path.HIGHSCORES_SAVE, 'r') as f:
            for line in f:
                score, other = line.strip().split(maxsplit=1)
                score = int(score)
                highscores.append((score, other))

    return highscores


def save_highscores(highscores):
    """ Сохранение результатов """
    check_dir(Path.SAVE_DIR)

    with open(Path.HIGHSCORES_SAVE, 'w') as f:
        f.writelines(highscores)
