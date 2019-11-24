from src.objects.field import Field
from src.objects.player import Player
from src.scenes.base_scene import Scene
from src.utils.vector import Point


class GameScene(Scene):
    def on_switch(self, *args, **kwargs):
        if 'reset' in kwargs:
            if kwargs['reset']:
                self.game.sounds['effect']['start'].play()
                self.field.reset_stage()
        # self.game.resize_screen(self.field.real_size)

    def create_objects(self):
        pos = Point(0, 0)
        tile_size = (40, 40)
        self.field = Field(self.game, pos, tile_size)
        self.objects.append(self.field)

        p = Player(self.field, Point(1, self.field.height - 2))

