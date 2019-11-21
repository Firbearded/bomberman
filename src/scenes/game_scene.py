from src.objects.player import Player
from src.scenes.base_scene import Scene
from src.objects.field import Field


class GameScene(Scene):
    def create_objects(self):
        f = Field(self.game, (0, 0), (21, 15), (50, 50))
        self.objects.append(f)
        self.game.resize_screen((21 * 50, 50 * 15))

        p = Player(f, (1, 1))
        p.speed_value = 2
        f.rand_fill(2, 30)
