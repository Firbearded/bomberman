import sys

from src.objects.menu.menu import Menu
from src.objects.menu.menu_items.menu_item_button import MenuItemButton
from src.objects.menu.menu_items.menu_item_label import MenuItemLabel
from src.objects.menu.menu_items.menu_item_switch import MenuItemSwitch
from src.objects.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import Color, Path
from src.utils.vector import Point


class MenuScene(Scene):
    def on_switch(self, play_sound=True):
        self.game.resize_screen()
        if play_sound:
            self.game.sounds['effect']['menu'].play(loops=9999)

    def create_objects(self):
        items = []
        font_size = 25
        font_name = Path.FONT
        color = Color.WHITE
        color2 = Color.RED
        aa = True
        wrapper = '-{}-'

        to = TextObject(self.game, 'BOMBERMAN 2020', font_name, font_size + 20, color=color, antialiasing=aa)
        items.append(MenuItemLabel(self.game, to))
        items[-1].interval_after = 75

        to = TextObject(self.game, 'Start new game', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.start))

        to = TextObject(self.game, 'Continue', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.continue_game))

        to = TextObject(self.game, 'Minimalistic mode: off', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemSwitch(self.game, to, wrapper, color2, self.game.toggle_minimalistic_mode, 'Minimalistic mode: on'))

        to = TextObject(self.game, 'Highscores', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.highscores))

        to = TextObject(self.game, 'Exit', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.exit))

        pos = Point(self.game.width / 2, 100)
        self.objects.append(Menu(self.game, pos, items))

    def start(self):
        self.game.set_scene(self.game.GAME_SCENE_INDEX, reset=True)
        self.game.sounds['effect']['menu'].stop()

    def continue_game(self):
        self.game.set_scene(self.game.GAME_SCENE_INDEX, reset=True, try_to_continue=True)
        self.game.sounds['effect']['menu'].stop()

    def exit(self):
        sys.exit(0)

    def highscores(self):
        self.game.set_scene(self.game.HIGHSCORE_SCENE_INDEX)
