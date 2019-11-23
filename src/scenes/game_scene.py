from src.objects.enemies import Onil, Ballom
from src.objects.field import Field
from src.objects.items import ItemPowerUp, ItemLifeUp
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

        Ballom(f, Point(5, 5))
        Onil(f, Point(5, 5))

        ItemPowerUp(f, Point(1, 3), (.5, .5))
        ItemLifeUp(f, Point(3, 1), (.5, .5))

        f.rand_fill(2, 30)
