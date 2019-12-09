CATEGORY = "tile_textures"


class Tile:
    color = (0, 0, 0)  # Запасной цвет
    image_name = None  # Название спрайта клетки
    soft = False  # Можно ли ломать
    walkable = False  # Можно ходить (земля)
    empty = False  # Пусто, но ходить нельзя (вода)
    wallpass = False  # Можно ли ходить тем, кто может через стены проходить (призраци)

    # Огонь может распространяться по пустым (empty), но мобы могут ходить только где можно (walkable)
    @classmethod
    def is_walkable_for_player(cls, player_object):
        return cls.walkable


# Tiles:


class TileEmpty(Tile):
    color = (220, 220, 220)
    image_name = "grass"
    walkable = True
    empty = True
    wallpass = True


class TileWall(Tile):
    color = (120, 120, 120)
    image_name = "wall"


class TileBreakableWall(Tile):
    color = (160, 160, 160)
    image_name = "c_wall"
    soft = True
    wallpass = True

    @classmethod
    def is_walkable_for_player(cls, player_object):
        return player_object.has_wallpass


class TileUnreachableEmpty(TileEmpty):
    walkable = False
    wallpass = False

    @classmethod
    def is_walkable_for_player(cls, player_object):
        return player_object.has_bombpass


TILES = (
    TileEmpty, TileWall, TileBreakableWall, TileUnreachableEmpty
)
