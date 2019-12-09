from src.game.menu.menu import Menu
from src.game.menu.menu_items.menu_item_button import MenuItemButton
from src.game.menu.menu_items.menu_item_label import MenuItemLabel
from src.game.supporting.constants import Path, Color
from src.game.supporting.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.vector import Point


class CaptionsScene(Scene):
    """ Сцена титров """

    NAMES = sorted(("Конягин Даниил", "Кильдишев Александр", "Кильдишев Пётр", "Акст Екатерина", "Гулинкин Михаил",
                    "Бахарев Никита", "Емельянова Татьяна", "Кузьмин Василий", "Пономарев Андрей"))

    def create_objects(self):
        items = []
        font_size = 25
        font_name = Path.FONT
        color = Color.WHITE
        color2 = Color.RED
        aa = True
        interval = 40

        to = TextObject(self.game, 'CREATORS:', font_name, font_size + 10, color=color, antialiasing=aa)
        items.append(MenuItemLabel(self.game, to))
        items[-1].interval_after = interval

        for name in CaptionsScene.NAMES:
            to = TextObject(self.game, '{}'.format(name), font_name, font_size, color=color, antialiasing=aa)
            items.append(MenuItemLabel(self.game, to))

        to = TextObject(self.game, '(c) for MSHP PromProg 2019-20', font_name, font_size - 5, color=color, antialiasing=aa)
        items.append(MenuItemLabel(self.game, to))
        items[-1].interval_before = interval / 2

        to = TextObject(self.game, 'Back', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, "<<{}<<", color2, self.back))
        items[-1].interval_before = interval / 2

        pos = Point(self.game.width / 2, interval)
        self.menu = Menu(self.game, pos, items, 10)
        self.objects.append(self.menu)

    def back(self):
        self.game.set_scene(self.game.MENU_SCENE_INDEX, play_sound=False)
