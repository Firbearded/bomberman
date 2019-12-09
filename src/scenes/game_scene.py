from src.game.entities.player import Player
from src.game.field.field_class import Field
from src.game.supporting.constants import Color, Path
from src.game.supporting.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.vector import Point


class GameScene(Scene):
    """ Игровая сцена """
    MAX_FPS = 0

    STATES = NOTHING, NEW_GAME, CONTINUE_GAME, ROUND_SWITCH = 0, 1, 2, 3

    def on_switch(self, state=NOTHING):
        if state == GameScene.NEW_GAME:
            self.field.new_game()
        elif state == GameScene.CONTINUE_GAME:
            self.field.continue_game()
        elif state == GameScene.ROUND_SWITCH:
            self.field.round_switch()
        elif state == GameScene.NOTHING:
            pass  # self.field.round_switch()
        else:
            raise ValueError

    def create_objects(self):
        tile_size = (40, 40)

        self.field = Field(self.game, tile_size)
        Player(self.field)
        self.field._flush_enitites()
        self.objects.append(self.field)

        font_size = 20
        self.timer_object = TextObject(self.game, "0:00", Path.FONT, font_size, color=Color.WHITE, antialiasing=True)
        self.score_object = TextObject(self.game, "Score: 0", Path.FONT, font_size, color=Color.WHITE, antialiasing=True)
        self.lives_object = TextObject(self.game, "Lives: 0", Path.FONT, font_size, color=Color.WHITE, antialiasing=True)

        self.objects.append(self.timer_object)
        self.objects.append(self.score_object)
        self.objects.append(self.lives_object)

    def additional_logic(self):
        self.update_gui()

    def update_gui(self):
        dx, dy = 10, 10

        t = int((self.field.timer._delay - self.field.timer.remaining) / 1000)
        if t <= 0:
            t = 0
            self.timer_object.set_color(Color.RED)
        else:
            self.timer_object.set_color(Color.WHITE)

        min, sec = t // 60, t % 60

        self.score_object.set_text("Score: {}".format(self.field.main_player.score))
        pos = Point(dx, dy)
        self.score_object.pos = pos

        self.timer_object.set_text("{}:{:02d}".format(min, sec))
        pos = Point((self.game.width - self.timer_object.size[0]) / 2, dy)
        self.timer_object.pos = pos

        self.lives_object.set_text("Lives: {}".format(self.field.main_player.current_lives))
        pos = Point((self.game.width - self.lives_object.size[0] - dx, dy))
        self.lives_object.pos = pos
