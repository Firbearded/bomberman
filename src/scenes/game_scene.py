from src.objects.player import Player
from src.scenes.base_scene import Scene
from src.objects.field import Field


class GameScene(Scene):
    def create_objects(self):
        f = Field(self.game, (0, 0), (21, 15), (40, 40))
        self.objects.append(f)

        p = Player(f, (1, 1))
        self.objects.append(p)
