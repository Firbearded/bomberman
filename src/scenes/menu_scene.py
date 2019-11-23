import sys

from src.scenes.base_scene import Scene
from src.objects.menu import MenuItem
from src.objects.menu import Menu
from src.objects.text import Text
from src.utils.constants import Color


class MenuScene(Scene):

    def create_objects(self):
        items = []

        #создание MenuItem - start
        text1 = Text(self.game, (0,0), 'Start', None, 50, Color.WHITE, True)
        text2 = Text(self.game, (0,0), 'Start', None, 50, Color.RED, True)
        items.append(MenuItem(text1, text2, self.Start))
        #создание MenuItem - Exit
        text1 = Text(self.game,(0,0), 'Exit', None, 50, Color.WHITE, True)
        text2 = Text(self.game,(0,0), 'Exit', None, 50, Color.RED, True)
        items.append(MenuItem(text1, text2, self.Exit))

        #добавляем меню. Координаты menu нигде не используются на данный момент
        self.objects.append(Menu(self.game, (0, 0), items))

    #функция для кнопки Start
    def Start(self):
        self.game.set_scene (self.game.GAME_SCENE_INDEX)

    # функция для кнопки Exit
    def Exit(self):
        sys.exit(0)



