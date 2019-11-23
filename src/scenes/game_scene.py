from src.objects.enemy import Enemy
from src.objects.item import Item
from src.objects.field import Field
from src.objects.player import Player
from src.scenes.base_scene import Scene
from src.utils.vector import Point


class GameScene(Scene):
    def create_objects(self):
        pos = Point(0, 0)
        field_size = 21, 15
        tile_size = 50, 50

        f = Field(self.game, pos, field_size, tile_size)
        self.objects.append(f)
        self.game.resize_screen(Point(field_size) * Point(tile_size))

        p = Player(f, Point(1, 1))
        e = Enemy(f, Point(3, 3))

        item = Item(f, Point(1, 2), (1, 1))

        f.rand_fill(2, 30)
