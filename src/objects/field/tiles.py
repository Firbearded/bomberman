CATEGORY = "tile_textures"


class Tile:
    color = (0, 0, 0)  # Запасной цвет
    image_name = None  # Название спрайта клетки
    soft = False  # Можно ли ломать
    walkable = False  # Можно ходить (земля)
    empty = False  # Пусто, но ходить нельзя (вода)
    # Огонь может распространяться по пустым (empty), но мобы могут ходить только где можно (walkable)


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


TILES = (
    TileEmpty, TileWall, TileBreakableWall, TileUnreachableEmpty
)
