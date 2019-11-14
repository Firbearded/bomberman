class Tile:
    pass
    # Код (ход) гения

class EmptyTile:
    line_width = 2

class WallTile(Tile):
    line_width = 0

TILES = [
    EmptyTile, WallTile
]