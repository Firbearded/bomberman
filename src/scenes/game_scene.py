from src.scenes.base_scene import Scene
from src.objects.field import Field
from src.objects.enemy import Enemy


class GameScene(Scene):
    def create_objects(self):
        f = Field(self.game, (0, 0), (21, 15), (40, 40))
        self.objects.append(f)

        e = Enemy(f, (1, 1))
        self.objects.append(e)