from src.objects.field.field_class import Field
from src.objects.player import Player
from src.objects.supporting.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import Color, Path, Sounds
from src.utils.vector import Point


class GameScene(Scene):
    """ Игровая сцена """
    MAX_FPS = 0

    def on_switch(self, new_game=False, restart=True):
        if new_game:
            self.game.mixer.channels[self.game.mixer.MUSIC_CHANNEL].add_sound_to_queue(Sounds.Music.round_start.value)
        self.field.start_game(new_game, restart)

    def create_objects(self):
        tile_size = (40, 40)

        self.field = Field(self.game, tile_size)
        Player(self.field, Point(1, 1))
        self.field.flush_enitites()
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
        t = int((self.field.timer._delay - self.field.timer.remaining) / 1000)
        if t < 0:
            t = 0
            self.timer_object.set_color(Color.RED)
        else:
            self.timer_object.set_color(Color.WHITE)

        min, sec = t // 60, t % 60

        self.score_object.set_text("Score: {}".format(self.field.main_player.score))
        pos = Point(0, 0)
        self.score_object.pos = pos

        self.timer_object.set_text("{}:{:02d}".format(min, sec))
        pos = Point((self.game.width - self.timer_object.size[0]) / 2, 0)
        self.timer_object.pos = pos

        self.lives_object.set_text("Lives: {}".format(self.field.main_player.lives))
        pos = Point((self.game.width - self.lives_object.size[0], 0))
        self.lives_object.pos = pos
