import sys

from src.objects.menu.menu import Menu
from src.objects.menu.menu_items.menu_item_button import MenuItemButton
from src.objects.menu.menu_items.menu_item_label import MenuItemLabel
from src.objects.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import FONT_OLD, Color
from src.utils.vector import Point


class MenuScene(Scene):
    def on_switch(self):
        self.game.resize_screen()

    def create_objects(self):
        items = []
        font_size = 25
        font_name = FONT_OLD
        color = Color.WHITE
        color2 = Color.RED
        aa = True

        to = TextObject(self.game, 'BOMBERMAN 2020', font_name, font_size + 20, color=color, antialiasing=aa)
        lbl = MenuItemLabel(self.game, to)
        lbl.interval_after = 100

        items.append(lbl)

        to = TextObject(self.game, 'Start game', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, '-Start game-', color2, self.start))

        to = TextObject(self.game, 'Some useless button', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, '-SoMe uSeLeSs bUtToN-', color2))

        to = TextObject(self.game, 'Exit', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, '-Exit-', color2, self.exit))

        pos = Point(self.game.width / 2, 100)
        self.objects.append(Menu(self.game, pos, items))

    def start(self):
        self.game.set_scene(self.game.GAME_SCENE_INDEX)

    def exit(self):
        sys.exit(0)



