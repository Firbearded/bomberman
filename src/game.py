import sys
from threading import Thread

import pygame

from src.scenes.game_over_scene import GameoverScene
from src.scenes.game_scene import GameScene
from src.scenes.highscore_scene import HighscoreScene
from src.scenes.loading_scene import LoadingScene
from src.scenes.menu_scene import MenuScene
from src.utils.decorators import timetest
from src.utils.loader import load_textures, load_sounds


class Game:
    MENU_SCENE_INDEX = 0
    GAME_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    HIGHSCORE_SCENE_INDEX = 3

    @timetest
    def __init__(self, window_size=(800, 600), title='pygame window'):
        self.size = self.width, self.height = window_size
        self.title = title

        self.init()

        self.loading = LoadingScene(self)
        loading_thread = Thread(target=self.loading.main_loop)
        loading_thread.start()

        self.load_resurces()

        self.loading.running = False
        del self.loading
        del loading_thread

        self.create_scenes()

        self.running = False
        self.delta_time = 0

    def init(self):
        pygame.init()  # Инициализация библиотеки
        pygame.font.init()

        self.resize_screen(self.size)
        pygame.display.set_caption(self.title)

    def load_resurces(self):
        self.images = load_textures(self)
        self.sounds = load_sounds(self)

    def create_scenes(self):
        self.scenes = [MenuScene(self), GameScene(self), GameoverScene(self), HighscoreScene(self)]
        self.current_scene = 0

    def resize_screen(self, size):
        self.size = self.width, self.height = tuple(size)
        self.screen = pygame.display.set_mode(self.size)  # Создание окна (установка размера)

    def display_fps(self, fps):
        pygame.display.set_caption("{} — {} FPS".format(self.title, fps))

    def main_loop(self):
        self.running = True
        fps_start_time = pygame.time.get_ticks()
        fps = 0
        while self.running:  # Основной цикл работы программы
            loop_start_time = pygame.time.get_ticks()
            
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.running = False
            if not self.running:
                break

            self.scenes[self.current_scene].process_frame(eventlist)

            end_time = pygame.time.get_ticks()
            self.delta_time = (end_time - loop_start_time) / 1000

            fps += 1
            if end_time - fps_start_time >= 1000:
                self.display_fps(fps)
                fps_start_time = end_time - (end_time - fps_start_time) % 1000
                fps = 0

        sys.exit(0)  # Выход из программы

    def set_scene(self, index):
        print("New scene: from {} to {}".format(self.current_scene, index))
        self.current_scene = int(index)
