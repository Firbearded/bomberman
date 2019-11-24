from os.path import exists

from src.objects.menu.menu import Menu
from src.objects.menu.menu_items.menu_item_button import MenuItemButton
from src.objects.menu.menu_items.menu_item_label import MenuItemLabel
from src.objects.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import Path, Color
from src.utils.vector import Point


class HighscoreScene(Scene):
    MAX_HIGHSCORES = 10
    NONE_HIGHSCORE = "-none-"

    def on_switch(self, *args, **kwargs):
        self.update_highscores()
        self.update_labels()

    def create_objects(self):
        self.highscores = []

        items = []
        font_size = 25
        font_name = Path.FONT
        color = Color.WHITE
        color2 = Color.RED
        aa = True
        interval = 40

        to = TextObject(self.game, 'TOP {} HIGHSCORES:'.format(self.MAX_HIGHSCORES), font_name, font_size + 10, color=color, antialiasing=aa)
        lbl = MenuItemLabel(self.game, to)
        lbl.interval_after = interval

        items.append(lbl)

        for i in range(self.MAX_HIGHSCORES):
            to = TextObject(self.game, 'score{} other'.format(i), font_name, font_size, color=color, antialiasing=aa)
            items.append(MenuItemLabel(self.game, to))

        to = TextObject(self.game, 'Back', font_name, font_size, color=color, antialiasing=aa)
        items.append(MenuItemButton(self.game, to, "<<{}<<", color2, self.back))
        items[-1].interval_before = interval / 2

        pos = Point(self.game.width / 2, interval)
        self.menu = Menu(self.game, pos, items, 10)
        self.objects.append(self.menu)

    def back(self):
        self.game.set_scene(self.game.MENU_SCENE_INDEX, play_sound=False)

    def update_highscores(self):
        self.highscores = []
        if exists(Path.HIGHSCORES_SAVE):
            with open(Path.HIGHSCORES_SAVE, 'r') as f:
                for line in f:
                    score, other = line.strip().split(maxsplit=1)
                    score = int(score)
                    self.highscores.append((score, other))

        self.highscores.sort(reverse=True)

    def update_labels(self):
        hc = self.highscores[:5]

        for i in range(len(hc)):
            hc[i] = "{} - {}".format(*hc[i])

        if len(hc) < self.MAX_HIGHSCORES:
            hc += [self.NONE_HIGHSCORE for i in range(self.MAX_HIGHSCORES - len(hc))]

        for i in range(1, self.MAX_HIGHSCORES + 1):
            self.menu.items[i].set_text(hc[i - 1])

        self.menu.update_item_positions()
