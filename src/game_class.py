import sys
from threading import Thread
from time import time

import pygame

from src.game.supporting.constants import Path
from src.game.supporting.loader import load_textures, load_sounds
from src.game.supporting.sound_mixer import SoundMixer
from src.scenes.captions_scene import CaptionsScene
from src.scenes.game_over_scene import GameoverScene
from src.scenes.game_scene import GameScene
from src.scenes.highscore_scene import HighscoreScene
from src.scenes.loading_scene import LoadingScene
from src.scenes.menu_scene import MenuScene
from src.scenes.settings_scene import SettingsScene
from src.scenes.transition_scene import TransitionScene
from src.utils.decorators import benchmark


class Game:
    MENU_SCENE_INDEX = 0
    GAME_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    HIGHSCORE_SCENE_INDEX = 3
    TRANSITION_SCENE_INDEX = 4
    SETTINGS_SCENE_INDEX = 5
    CAPTIONS_SCENE_INDEX = 6

    @benchmark
    def __init__(self, window_size=(800, 600), title='Bomberman'):
        self.size = self.width, self.height = window_size
        self.title = title

        self.mixer = SoundMixer()

        self.init()

        self.loading = LoadingScene(self)
        loading_thread = Thread(target=self.loading.main_loop)
        loading_thread.start()

        self.load_resources()

        self.loading.running = False
        if self.loading.lock.acquire():
            del self.loading
            del loading_thread

        self.create_scenes()

        self._timers = []
        self.delta_time = 0

    def init(self):
        """ Инициализация библиотек и окна """
        pygame.init()
        pygame.font.init()

        self.resize_screen(self.size)
        pygame.display.set_icon(pygame.image.load(Path.ICON_PATH))
        pygame.display.set_caption(self.title)

    def load_resources(self):
        """ Загрузка ресурсов """
        self.images = load_textures(self)
        self.mixer.init(load_sounds(self))

    def create_scenes(self):
        """ Создание сцен """
        self.scenes = [MenuScene(self), GameScene(self), GameoverScene(self), HighscoreScene(self),
                       TransitionScene(self), SettingsScene(self), CaptionsScene(self)]
        self.current_scene = 0
        self.scenes[self.current_scene].on_switch()

    def resize_screen(self, size=None):
        """ Resize'им окно """
        if size is not None:
            self.size = self.width, self.height = tuple(size)
        self.screen = pygame.display.set_mode(self.size)  # Создание окна (установка размера)

    def display_fps(self, fps):
        """ Показываем FPS в названии окна """
        pygame.display.set_caption("{} — {} FPS".format(self.title, fps))

    def main_loop(self):
        """ Запуск основного цикла программы """
        self.running = True
        fps_start_time = time()  # Для счёта FPS
        fps = 0
        pygame.event.clear()
        while self.running:  # Основной цикл работы программы
            loop_start_time = time()

            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.running = False
            if not self.running:
                break

            self.scenes[self.current_scene].process_frame(eventlist)
            self.mixer.process_logic()
            for t in self._timers:
                t.timer_logic()
                if t.is_timeout:
                    self._timers.remove(t)

            end_time = time()  # Расчёт delta_time
            self.delta_time = (end_time - loop_start_time)

            fps += 1  # Дляя счёта FPS
            if end_time - fps_start_time >= 1:
                self.display_fps(fps)
                fps_start_time = end_time - (end_time - fps_start_time) % 1
                fps = 0

        pygame.quit()
        sys.exit(0)  # Выход из программы

    def set_scene(self, index, *args, **kwargs):
        """ Переключение на другую сцену """
        print("New scene: from {} to {} without delay".format(self.current_scene, index))
        self.current_scene = int(index)
        self.scenes[self.current_scene].on_switch(*args, **kwargs)

    def set_scene_with_transition(self, index, delay, message, *args, **kwargs):
        """
        Переключение на другую сцену через сцену перехода.
        :param index: Индекс сцены
        :param delay: Задержка в ms
        :param message: Сообщение
        :type index: int
        :type delay: int
        :type message: str
        """
        print("New scene: from {} to {} (delay={}; message='{}'".format(self.current_scene, index, delay, message))
        self.current_scene = int(self.TRANSITION_SCENE_INDEX)
        self.scenes[self.current_scene].on_switch()
        self.scenes[self.current_scene].start(index, delay, message, *args, **kwargs)

    def add_global_timer(self, timer):
        """
        Добавить таймер.
        Сюда можно кидать таймеры, тут Game будет сам вызывать у них process_logic
        :type timer: TimerObject
        """
        timer.start()
        self._timers.append(timer)

    def clear_global_timers(self):
        self._timers.clear()
