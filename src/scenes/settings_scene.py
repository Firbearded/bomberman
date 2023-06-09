import os
from configparser import ConfigParser

from src.game.menu.menu import Menu
from src.game.menu.menu_items.menu_item_button import MenuItemButton
from src.game.menu.menu_items.menu_item_label import MenuItemLabel
from src.game.menu.menu_items.menu_item_slider import MenuItemSlider
from src.game.supporting.constants import Path, Color
from src.game.supporting.textobject import TextObject
from src.scenes.base_scene import Scene
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

        rl = 24
        mx = 24
        default = 10

        sliders = []

        to = TextObject(self.game, '-General--', font_name, font_size - 5, color=color, antialiasing=aa)
        _volume = MenuItemSlider(self.game, to, "-{}-", color2, real_length=rl, on_change=self.update_general_volume,
                                 max_value=mx, value=default)
        items.append(_volume)
        sliders.append(_volume)
        _volume.interval_after = 15

        to = TextObject(self.game, 'Background', font_name, font_size - 5, color=color, antialiasing=aa)
        bb_volume = MenuItemSlider(self.game, to, "-{}-", color2, real_length=rl, on_change=self.update_bb_volume,
                                   max_value=mx, value=default)
        items.append(bb_volume)
        sliders.append(bb_volume)

        to = TextObject(self.game, '-Effects--', font_name, font_size - 5, color=color, antialiasing=aa)
        effects_volume = MenuItemSlider(self.game, to, "-{}-", color2, real_length=rl,
                                        on_change=self.update_effects_volume, max_value=mx, value=default)
        items.append(effects_volume)
        sliders.append(effects_volume)

        to = TextObject(self.game, '--Other---', font_name, font_size - 5, color=color, antialiasing=aa)
        music_volume = MenuItemSlider(self.game, to, "-{}-", color2, real_length=rl,
                                      on_change=self.update_music_volume, max_value=mx, value=default)
        items.append(music_volume)
        sliders.append(music_volume)
        self.items = sliders

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

    def update_bb_volume(self, value, p):
        self.game.mixer.channels['background'].set_volume(p)
        if hasattr(self, 'items'):
            self.save()

    def update_general_volume(self, value, p):
        self.game.mixer.set_volume(p)
        if hasattr(self, 'items'):
            self.save()
