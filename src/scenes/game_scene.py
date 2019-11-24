import pygame

from src.objects.field import Field
from src.objects.player import Player
from src.objects.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import Color, Path
from src.utils.vector import Point


class GameScene(Scene):
    MAX_FPS = 0

    def on_switch(self, reset=False, try_to_continue=False):
        for i in self.objects:
            from src.objects.base_classes.entity import Entity
            if issubclass(type(i), Entity) or type(i) is Field:
                i.reload_animations()
        if reset:
            self.game.sounds['effect']['start'].play()
            self.field.reset_stage(load=try_to_continue)
        # self.game.resize_screen(self.field.real_size)

    def create_objects(self):
        pos = Point(0, 0)
        tile_size = (40, 40)
        self.field = Field(self.game, pos, tile_size)
        self.objects.append(self.field)

        font_size = 20
        self.timer_object = TextObject(self.game, "0:00", Path.FONT, font_size, color=Color.WHITE, antialiasing=True)
        self.score_object = TextObject(self.game, "Score: 0", Path.FONT, font_size, color=Color.WHITE, antialiasing=True)
        self.lives_object = TextObject(self.game, "Lives: 0", Path.FONT, font_size, color=Color.WHITE, antialiasing=True)

        self.objects.append(self.timer_object)
        self.objects.append(self.score_object)
        self.objects.append(self.lives_object)

        p = Player(self.field, Point(1, self.field.height - 2))

    def additional_logic(self):
        self.update_gui()

    def update_gui(self):
        t = self.field.time - (pygame.time.get_ticks() - self.field.start_time) // 1000
        if t < 0:
            t = 0
            self.timer_object.set_color(Color.RED)
        else:
            self.timer_object.set_color(Color.WHITE)

        min, sec = t // 60, t % 60

        self.score_object.set_text("Score: {}".format(self.field.players[0].score))
        pos = Point(0, 0)
        self.score_object.pos = pos

        self.timer_object.set_text("{}:{:02d}".format(min, sec))
        pos = Point((self.game.width - self.timer_object.size[0]) / 2, 0)
        self.timer_object.pos = pos

        self.lives_object.set_text("Lives: {}".format(self.field.players[0].lives))
        pos = Point((self.game.width - self.score_object.size[0], 0))
        self.lives_object.pos = pos
