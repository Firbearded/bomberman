import os
from random import randint, choice, shuffle
from time import strftime

import pygame

from src.game.base_classes.geometric_object import GeometricObject
from src.game.base_classes.pygame_object import PygameObject
from src.game.base_classes.timer_object import TimerObject
from src.game.entities.enemies import ENEMIES
from src.game.entities.items import Door, DROP_LIST
from src.game.field.breaking_wall import BreakingWall
from src.game.field.stage import Stage
from src.game.field.tiles import TILES, CATEGORY
from src.game.field.tracker import Tracker
from src.game.field.transparrent_tracker import TransparrentTracker
from src.game.supporting.constants import Path, Sounds
from src.utils.vector import Point


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
        Stage(name="Stage 1", enemies=(6,), upgrades=(0, 1)),
        Stage(name="Stage 2", enemies=(3, 3), upgrades=(1,)),
        Stage(name="Stage 3", enemies=(2, 2, 2), upgrades=(0, 0, 1)),
        Stage(name="Stage 4", enemies=(1, 1, 2, 2), upgrades=(0, 0, 0, 1)),
        Stage(name="Stage 5", enemies=(0, 4, 3), upgrades=(1,)),
        Stage(name="Stage zoo", enemies=(1, 1, 1, 1, 1, 1, 1, 1,), upgrades=(0, 0, 0, 0, 0, 10, 10, 10, 10)),
        Stage(name="Stage HELL", enemies=(1, 0, 0), upgrades=(100, 100, 5, 100, 100), time=10,
              on_timeout=(5, 5, 5, 5, 5, 5, 5, 10)),
    )

    GAMEOVER_MSG = "GAME OVER"
    WIN_MSG = "WIN"
    SOUND_GAMEWIN = Sounds.Music.game_win.value
    SOUND_TIMEOUT = Sounds.Effects.timeout.value
    SOUND_LOSE = Sounds.Music.round_lose.value

    def __init__(self, game_object, tile_size: tuple):
        PygameObject.__init__(self, game_object)
        GeometricObject.__init__(self)

        self._tile_size = tuple(tile_size)
        from src.game.entities.bomb import Fire
        from src.game.entities.bomb import Bomb
        from src.game.entities.base.item import Item
        from src.game.entities.base.enemy import Enemy
        from src.game.entities.player import Player

        self._grid = None  # Двумерный список — типы клеток
        self._field_size = (1, 1)  # Размеры поля
        self.surface = pygame.Surface(self.real_size)
        self._entities = {}  # Список сущностей, принадлежащих этому полю
        self._class_priority = (Player, Enemy, Fire, Bomb, Item,)
        # Приоритет классов на отрисовку (по убыванию)
        self._enemies_on_door = Field.ENEMIES_ON_DOOR

        self._soft_number = None
        self._upgrades = None
        self._has_door = None
        self._enemies = None
        self._extra_enemies = None

        self._current_stage_index = 0  # Индекс уровня
        self._entities_queue = []  # Очередь сущностей на добавление. Нельзя добавлять сущности в словарь во время
        # использования этого же словаря

        self.timer = TimerObject(0)
        self.timer.on_timeout = self.on_timeout

        self.load_images()

        self.tracker = Tracker(self)
        self.transparrent_tracker = TransparrentTracker(self)

    # ======================== Свойства ========================
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

    # ================ Основные внешние методы ===============
    def add_entity(self, entity):
        """ Добвить сущность в поле (на самом деле добавить в очередь) """
        cls = type(entity)

        for c in self._class_priority:
            if issubclass(cls, c):
                cls = c
                break

        self._entities_queue.append((cls, entity))

    def _flush_enitites(self):
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
        from src.game.entities.player import Player
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
        if not self.tile_at(pos).empty:
            return False

        from src.game.entities.bomb import Bomb

        pos = tuple(pos)

        for b in self.get_entities(Bomb):
            if tuple(b.tile) == pos:
                return False

        return True

    def destroy_wall(self, pos, delay):
        """ Запускает анимацию уничтожения клетки pos за delay миллисекунд. """
        BreakingWall(self, pos, delay)
        self.draw_tile(pos[0], pos[1])

    def try_drop_item(self, pos):
        """ Дроп предмета на позиции pos (если рандом) """
        if self._soft_number == 1 and not self._has_door:
            self._has_door = True
            Door(self, pos)
        else:
            r = randint(1, self._soft_number)
            if r <= sum(self._upgrades) + (not self._has_door):
                if not self._has_door and r == 1:
                    self._has_door = True
                    Door(self, pos)
                else:
                    not_empty_i = []
                    for i in range(len(self._upgrades)):
                        if self._upgrades[i]:
                            not_empty_i.append(i)

                    i = choice(not_empty_i)

                    self._upgrades[i] -= 1
                    DROP_LIST[i](self, pos)

    # ================ Методы для самого поля ================
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
        from src.game.entities.player import Player

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

    def _reload_current_stage(self):
        stage = self.current_stage
        self._field_size = stage.field_size
        self._soft_number = stage.soft_wall_number
        self._upgrades = list(stage.upgrades)
        self._enemies = stage.enemies
        self.timer.delay = stage.time * 1000
        self._extra_enemies = stage.enemies_on_timeout
        self._has_door = False
        from src.game.entities.player import Player
        if Player in self._entities:
            for p in self._entities[Player]:
                p.reset(full=False)

    def _reset_entities(self, full_reset_player=False):
        """ Сброс уровня """
        for cls in self._entities:
            from src.game.entities.player import Player
            if cls is not Player:
                for e in self._entities[cls]:
                    e.disable()
                    e.hide()
                self._entities[cls] = []
            else:
                for e in self._entities[cls]:
                    e.reset(full=full_reset_player)

    def _grid_init(self):
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

        self.surface = pygame.Surface(self.real_size)

    def _generate_soft_walls(self):
        """ Случайная генерация ломающихся стен """
        empty_tiles = self._get_empty_tiles_without_buffer()
        if len(empty_tiles) < self._soft_number:
            self._soft_number = len(empty_tiles)

        for _ in range(self._soft_number):
            pos = empty_tiles.pop(randint(0, len(empty_tiles) - 1))
            self.tile_set(pos, Field.TILE_SOFT_WALL)

    def _generate_enemies(self, enemies, pos=None):
        """ Генерация мобов """
        if pos is None:
            empty_tiles = self._get_empty_tiles_without_buffer()

            for e_type, e_number in enumerate(enemies):
                if e_number <= 0: continue
                if not empty_tiles: break
                for _ in range(e_number):
                    ENEMIES[e_type](self, empty_tiles.pop(randint(0, len(empty_tiles) - 1)))
        else:
            for e_type, e_number in enumerate(enemies):
                if e_number <= 0: continue
                for _ in range(e_number):
                    ENEMIES[e_type](self, pos)

    def _play_round_start(self):
        self.game_object.mixer.channels[self.game_object.mixer.BACKGROUND_CHANNEL].stop()
        self.game_object.mixer.channels[self.game_object.mixer.BACKGROUND_CHANNEL].add_sound_to_queue(
            Sounds.Music.round_start.value)

    def _round_init(self, ):
        """ Метод дял Начала игры """
        self._reload_current_stage()
        self._grid_init()
        self._generate_soft_walls()
        self._generate_enemies(self._enemies)

        self.draw_all_tiles()
        self._background_music()

        self.timer.start()

    def _background_music(self):
        bbs = [i.value for i in Sounds.Background]
        shuffle(bbs)
        for bb in bbs * 10:
            self.game_object.mixer.channels['background'].add_sound_to_queue(bb)
        self.game_object.mixer.channels['background'].unmute()

    def _start_stage(self):
        self._save_stage()
        self.game_object.set_scene_with_transition(self.game_object.GAME_SCENE_INDEX, 1500, self.current_stage.name)
        self._round_init()

    def _next_stage(self, x=1):
        """ Переключение на следующий уровень """
        self._current_stage_index += x
        if self._current_stage_index + 1 > len(Field.STAGES):
            self._end_game(win=True)
            return
        self._save_stage()
        self.round_switch()

    def _end_game(self, win=False):
        """ Окончание игры (полный проигрыш или выигрыш) """
        self._current_stage_index = 0
        self._save_score()
        # self._game_start()
        self.game_object.mixer.channels['background'].stop()
        if win:
            self.game_object.mixer.channels['music'].stop()
            self.game_object.mixer.channels['music'].add_sound_to_queue(self.SOUND_GAMEWIN)
        self.game_object.set_scene_with_transition(self.game_object.MENU_SCENE_INDEX, 3000,
                                                   (Field.GAMEOVER_MSG, Field.WIN_MSG)[win])

    def _save_score(self):
        """ Сохранить счёт """
        highscores = get_highscores()
        player = self.main_player

        second_str = strftime('%x %X')

        highscores.append((player.score, second_str))
        highscores.sort(reverse=True)
        highscores = ["{} {}\n".format(c, s) for c, s in highscores]

        save_highscores(highscores)

    def _save_stage(self, on_exit=False):
        """ Сохранить уровень """
        check_dir(Path.SAVE_DIR)
        if on_exit:
            self._load_stage()

        with open(Path.STAGE_SAVE, 'w') as f:
            print(self._current_stage_index, file=f)
            print(self.main_player.to_str(), file=f)

    def _load_stage(self, full=False):
        """ Загрузить уровень """
        check_dir(Path.SAVE_DIR)
        if os.path.exists(Path.STAGE_SAVE):
            with open(Path.STAGE_SAVE, 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    player = self.main_player

                    self._current_stage_index, player_vars = lines
                    self._current_stage_index = int(self._current_stage_index)

                    _lives = player._current_lives
                    player.from_str(player_vars)
                    if not full:
                        player._current_lives = _lives

    def _camera_move(self):
        new_pos = Point()

        for i in range(2):
            new_pos[i] = (-self.main_player.center[i] * self.tile_size[i] + self.game_object.size[i] / 2)
            if self.size[i] * self.tile_size[i] < self.game_object.size[i]:
                new_pos[i] = (self.game_object.size[i] - self.size[i] * self.tile_size[i]) / 2
            else:
                new_pos[i] = min(new_pos[i], 0)
                new_pos[i] = max(new_pos[i], self.game_object.size[i] - self.size[i] * self.tile_size[i])

        self.pos = new_pos

    def on_timeout(self):
        """ Метод, когда время на таймере закончится """
        self.game_object.mixer.channels['effects'].sound_play(self.SOUND_TIMEOUT)
        self._generate_enemies(self._extra_enemies)

    # ===================== Публичные методы ========================
    def new_game(self):
        """ Начинаем новую игру """
        self._reset_entities(full_reset_player=True)
        self._current_stage_index = 0
        self._play_round_start()
        self._start_stage()

    def continue_game(self):
        """ Продолжаем игру """
        self._load_stage(full=True)
        self._reset_entities(full_reset_player=False)
        self._play_round_start()
        self._start_stage()

    def round_switch(self):
        """ Перезагрузка уровня """
        self._load_stage(full=False)
        self._reset_entities(full_reset_player=False)
        self._start_stage()

    def round_win(self):
        """ Выигран уровень """
        self._next_stage()

    def round_lose(self):
        """ Проигрыш (не полный, жизни ещё есть) """
        from src.scenes.game_scene import GameScene
        self.game_object.mixer.channels['background'].mute()
        self.game_object.set_scene(self.game_object.GAME_SCENE_INDEX, state=GameScene.ROUND_SWITCH)

    def door_explosion(self, door_pos):
        self._generate_enemies(self._enemies_on_door, door_pos)

    # ======================== Эвенты ========================
    def additional_event(self, event):
        """ Проверка на выход из игры в меню """
        if event.type == pygame.KEYDOWN:
            if event.key in Field.KEYS_EXIT:
                print("Exit from game to menu")
                self._save_stage(on_exit=True)
                self.game_object.clear_global_timers()
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
        self.tracker.process_logic()
        self.transparrent_tracker.process_logic()
        for cls in self._entities:
            for e in self._entities[cls]:
                e.process_logic()

        self._camera_move()

        self._flush_enitites()

    # ======================= Отрисовка ======================
    def draw_tile(self, x, y):
        tile_real_pos = (x * self.tile_size[0], y * self.tile_size[1])

        rect = *tile_real_pos, *self.tile_size

        tile = self.tile_at(x, y)
        if self.tile_images and tile.image_name and Field._BACKGROUND_TILE.image_name:
            # Если есть спрайты и названия спайтов у клеток, то рисуем текстуры
            self.surface.blit(self.tile_images[Field._BACKGROUND_TILE.image_name], rect)
            if tile is not Field._BACKGROUND_TILE:
                self.surface.blit(self.tile_images[tile.image_name], rect)
        else:  # Иначе запасной план: рисуем квадраты
            pygame.draw.rect(self.surface, tile.color, rect, 0)

        if Field.LINE_WIDTH > 0:
            pygame.draw.rect(self.surface, (0, 0, 0), rect, Field.LINE_WIDTH)

    def draw_all_tiles(self):
        for y in range(self.height):
            for x in range(self.width):
                self.draw_tile(x, y)

    def process_draw_entities(self):
        """ Отрисовка всех сущностей, принадлежащих этому полю """
        other_keys = set(self._entities.keys()).difference(set(self._class_priority))
        for cls in tuple(reversed(self._class_priority)) + tuple(other_keys):
            if cls in self._entities:
                for e in reversed(self._entities[cls]):
                    e.process_draw()

    def process_draw(self):
        self.game_object.screen.blit(self.surface, tuple(self.pos))
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
