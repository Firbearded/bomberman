CATEGORY = "tile_textures"


class Tile:
    color = (0, 0, 0)
    image_name = None
    breakable = False
    walkable = False


# Tiles:


class TileEmpty(Tile):
    color = (220, 220, 220)
    image_name = "grass"
    walkable = True


class TileWall(Tile):
    color = (120, 120, 120)
    image_name = "wall"


class TileBreakableWall(Tile):
    color = (160, 160, 160)
    image_name = "break_wall"
    breakable = True


class TileUnreachableEmpty(TileEmpty):
    walkable = False

# TODO: удалить
# class TileBomb(Tile):
#     color = (0, 160, 0)
#     image_name = "bomb"
#
#
# class TilePoints(Tile):
#     color = (160, 160, 0)
#     image_name = "point"
#
#
# class TileFirewave(Tile):
#     color = (160, 0, 0)
#     image_name = "fire_wall"


TILES = [
    TileEmpty, TileWall, TileBreakableWall, TileUnreachableEmpty  # TileBomb, TilePoints, TileFirewave
]
