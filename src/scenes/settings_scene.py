import os
from configparser import ConfigParser

from src.objects.menu.menu import Menu
from src.objects.menu.menu_items.menu_item_button import MenuItemButton
from src.objects.menu.menu_items.menu_item_label import MenuItemLabel
from src.objects.menu.menu_items.menu_item_slider import MenuItemSlider
from src.objects.supporting.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import Path, Color
from src.utils.vector import Point


class SettingsScene(Scene):
    """ Сцена настроек """

    def create_objects(self):
        items = []
        font_size = 25
        font_name = Path.FONT
        color = Color.WHITE
        color2 = Color.RED
        aa = True
        interval = 40

        to = TextObject(self.game, 'SETTINGS:', font_name, font_size + 10, color=color, antialiasing=aa)
        items.append(MenuItemLabel(self.game, to))
        items[-1].interval_after = interval

        to = TextObject(self.game, 'Music  ', font_name, font_size - 5, color=color, antialiasing=aa)
        music_volume = MenuItemSlider(self.game, to, "-{}-", color2, real_length=25, on_change=self.update_music_volume,
                                      max_value=25, value=5)
        items.append(music_volume)

        to = TextObject(self.game, 'Effects', font_name, font_size - 5, color=color, antialiasing=aa)
        effects_volume = MenuItemSlider(self.game, to, "-{}-", color2, real_length=25,
                                        on_change=self.update_effects_volume, max_value=25, value=5)
        items.append(effects_volume)

        self.items = [music_volume, effects_volume]

        to = TextObject(self.game, 'Back', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, "<<{}<<", color2, self.back))
        items[-1].interval_before = interval / 2

        pos = Point(self.game.width / 2, interval)
        self.menu = Menu(self.game, pos, items, 10)
        self.objects.append(self.menu)

        self.load()

    def back(self):
        self.game.set_scene(self.game.MENU_SCENE_INDEX, play_sound=False)

    def load(self):
        if os.path.exists(Path.SETTINGS_SAVE):
            config = ConfigParser()
            config.read(Path.SETTINGS_SAVE)

            for i in self.items:
                if i._text.strip() in config['settings']:
                    i.value = float(config['settings'][i._text.strip()])
                    i.add(0)

    def save(self):
        if not os.path.exists(Path.SAVE_DIR):
            os.makedirs(Path.SAVE_DIR)

        config = ConfigParser()
        config['settings'] = {}
        for i in self.items:
            config['settings'][i._text.strip()] = str(i.value)

        with open(Path.SETTINGS_SAVE, 'w') as configfile:
            config.write(configfile)

    def update_music_volume(self, value, p):
        self.game.mixer.channels['music'].set_volume(p)
        if hasattr(self, 'items'):
            self.save()

    def update_effects_volume(self, value, p):
        self.game.mixer.channels['effects'].set_volume(p)
        if hasattr(self, 'items'):
            self.save()
