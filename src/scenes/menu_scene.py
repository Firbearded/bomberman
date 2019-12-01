import sys

from src.objects.menu.menu import Menu
from src.objects.menu.menu_items.menu_item_button import MenuItemButton
from src.objects.menu.menu_items.menu_item_label import MenuItemLabel
from src.objects.supporting.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import Color, Path, Sounds
from src.utils.vector import Point


class MenuScene(Scene):
    """ Сцена меню """
    def on_switch(self, play_sound=True):
        if play_sound:
            self.game.mixer.channels[self.game.mixer.EFFECTS_CHANNEL].stop()
            self.game.mixer.channels[self.game.mixer.MUSIC_CHANNEL].add_sound_to_queue(Sounds.Music.menu.value, -1)

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
        items[-1].interval_before = 75
        items[-1].interval_after = 50

        to = TextObject(self.game, 'New game', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.start))

        to = TextObject(self.game, 'Continue', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.continue_game))
        items[-1].interval_after = 10

        to = TextObject(self.game, 'Highscores', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.highscores))

        to = TextObject(self.game, 'Settings', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.settings))

        to = TextObject(self.game, 'Captions', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.captions))

        to = TextObject(self.game, 'Exit', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, wrapper, color2, self.exit))
        items[-1].interval_before = 10

        pos = Point(self.game.width / 2, 0)
        self.objects.append(Menu(self.game, pos, items))

    def start(self):
        self.game.mixer.channels[self.game.mixer.MUSIC_CHANNEL].stop()
        self.game.set_scene(self.game.GAME_SCENE_INDEX, new_game=True, restart=False)

    def continue_game(self):
        self.game.mixer.channels[self.game.mixer.MUSIC_CHANNEL].stop()
        self.game.set_scene(self.game.GAME_SCENE_INDEX, new_game=False, restart=False)

    def exit(self):
        sys.exit(0)

    def highscores(self):
        self.game.set_scene(self.game.HIGHSCORE_SCENE_INDEX)

    def settings(self):
        self.game.set_scene(self.game.SETTINGS_SCENE_INDEX)

    def captions(self):
        self.game.set_scene(self.game.CAPTIONS_SCENE_INDEX)
