import sys
import pygame

from src.scenes.game_over_scene import GameoverScene
from src.scenes.game_scene import GameScene
from src.scenes.highscore_scene import HighscoreScene
from src.scenes.menu_scene import MenuScene
from src.utils.loader import load_textures


class Game:
    MENU_SCENE_INDEX = 0
    GAME_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    HIGHSCORE_SCENE_INDEX = 3

    def __init__(self, window_size=(800, 600), title='pygame window'):
        self.width, self.height = window_size
        self.title = title

        self.init()

        self.scenes = [MenuScene(self), GameScene(self), GameoverScene(self), HighscoreScene(self)]
        self.current_scene = 0
        self.game_over = False
        self.delta_time = 0

    @property
    def size(self):
        return self.width, self.height

    def init(self):
        pygame.init()  # Инициализация библиотеки
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)  # Создание окна (установка размера)
        pygame.display.set_caption(self.title)
        self.images = load_textures()

    def resize_screen(self, size):
        self.width, self.height = size
        self.screen = pygame.display.set_mode(self.size)

    def _update_title(self, fps):  # TODO
        pygame.display.set_caption("{} — {} FPS".format(self.title, fps))

    def main_loop(self):
        fps_start_time = pygame.time.get_ticks()
        fps = 0
        while not self.game_over:  # Основной цикл работы программы
            start_time = pygame.time.get_ticks()
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.game_over = True
            if self.game_over:
                break

            self.scenes[self.current_scene].process_frame(eventlist)
            end_time = pygame.time.get_ticks()
            self.delta_time = (end_time - start_time) / 1000
            fps += 1
            if end_time - fps_start_time >= 1000:
                fps_start_time = end_time - (end_time - fps_start_time) % 1000
                self._update_title(fps)
                fps = 0

        sys.exit(0)  # Выход из программы

    def set_scene(self, index):
        print("New scene: from {} to {}".format(self.current_scene, index))
        self.current_scene = index
