class Tile:   # TODO: добавить текстуры
    color = (0, 0, 0)


class TileEmpty:
    color = (220, 220, 220)


class TileWall(Tile):
    color = (120, 120, 120)


TILES = [
    TileEmpty, TileWall,
]
