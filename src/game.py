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

    def __init__(self, window_size=(50 * 21, 50 * 15), title='pygame window'):
        self.width, self.height = window_size
        self.title = title

        self.init()

        self.scenes = [MenuScene(self), GameScene(self), GameoverScene(self), HighscoreScene(self)]
        self.current_scene = 0
        self.images = None

    @property
    def size(self):
        return self.width, self.height

    def init(self):
        pygame.init()  # Инициализация библиотеки
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)  # Создание окна (установка размера)
        pygame.display.set_caption(self.title)
        self.images = load_textures()

    def main_loop(self):
        self.game_over = False
        while not self.game_over:  # Основной цикл работы программы
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.game_over = True
            if self.game_over:
                break

            self.scenes[self.current_scene].process_frame(eventlist)
        sys.exit(0)  # Выход из программы

    def set_scene(self, index):
        print("New scene: from {} to {}".format(self.current_scene, index))
        self.current_scene = index
