CATEGORY = "tile_textures"


class Tile:
    color = (0, 0, 0)
    image_name = None
    soft = False  # Можно ли ломать
    walkable = False  # Можно ходить (земля)
    empty = False  # Пусто, но ходить нельзя (вода)


# Tiles:


class TileEmpty(Tile):
    color = (220, 220, 220)
    image_name = "grass"
    walkable = True
    empty = True


class TileWall(Tile):
    color = (120, 120, 120)
    image_name = "wall"


class TileBreakableWall(Tile):
    color = (160, 160, 160)
    image_name = "break_wall"
    soft = True


class TileUnreachableEmpty(TileEmpty):
    walkable = False
    image_name = ""


TILES = (
    TileEmpty, TileWall, TileBreakableWall, TileUnreachableEmpty
)
