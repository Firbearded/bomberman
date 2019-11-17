from src.objects.player import Player
from src.scenes.base_scene import Scene
from src.objects.field import Field


class GameScene(Scene):
    def create_objects(self):
        f = Field(self.game, (0, 0), (21, 15), (40, 40))
        self.objects.append(f)

        p = Player(f, (1, 1))
        self.objects.append(p)

        g = [[0 for i in range(f.width)] for j in range(f.height)]
        f.grid = g

        for i in range(f.height):
            g[i][0] = 1
            g[i][-1] = 1
        for i in range(f.width):
            g[0][i] = 1
            g[-1][i] = 1

        from random import randint
        for i in range(25):
            g[randint(0, f.height - 1)][randint(0, f.width - 1)] = 1
        p.speed_value = .05
        # p.size = (1.2, 1.9)
