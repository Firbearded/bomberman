from queue import Queue

from src.utils.vector import Vector


class Tracker:
    """
    Класс, рассчитывающий для мобов пути до игрока
    """

    delta = [Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]

    def __init__(self, field_object):
        self.field_object = field_object
        self.player = None

        # Матрицы путей
        self.parent = []
        self.parent_wallpass = []

        self._player_last_pos = None

    def can_walk_at(self, tile):
        """ Функция разрешенности клетки для обычного моба """
        return self.field_object.tile_at(tile).walkable

    def can_walk_at_wallpass(self, tile):
        """ Функция разрешенности клетки для моба, который ходит через стены """
        return self.field_object.tile_at(tile).wallpass

    def init_matrix(self, parent):
        """ Инициализация матрицы путей """
        parent.clear()
        for i in range(self.field_object.width):
            parent.append([])
            for j in range(self.field_object.height):
                parent[i].append(None)

    def calculate_ways(self, parent, walkable):
        """ Расчет путей до игрока """
        # Обнуление матрицы путей
        for i in range(self.field_object.width):
            for j in range(self.field_object.height):
                parent[i][j] = None
        # Расчет путей до игрока обходом в ширину
        player_pos = self.player.tile
        self._player_last_pos = player_pos
        queue = Queue()
        if walkable(player_pos):
            parent[player_pos.x][player_pos.y] = player_pos
            queue.put(player_pos)
        while not queue.empty():
            current_pos = queue.get()
            for v in self.delta:
                new_pos = current_pos + v
                if walkable(new_pos) and not parent[new_pos.x][new_pos.y]:
                    parent[new_pos.x][new_pos.y] = current_pos
                    queue.put(new_pos)

    def get_next_tile(self, tile):
        """ Получение следующей клетки на пути для обычного моба """
        return self.parent[tile.x][tile.y]

    def get_next_tile_wallpass(self, tile):
        """ Получение следующей клетки на пути для моба, который ходит через стены """
        return self.parent_wallpass[tile.x][tile.y]

    def _update_player(self):
        self.player = self.field_object.main_player

    def process_logic(self):
        """ Логика работы Tracker'а - расчет путей """
        # Инициализация матриц, если их размеры не соответствуют размеру поля
        if self.field_object.width != len(self.parent) or self.field_object.height != len(self.parent[0]):
            self.init_matrix(self.parent)
            self.init_matrix(self.parent_wallpass)
        if not self.player:
            self._update_player()
        # Cобственно расчет
        if not self._player_last_pos or self._player_last_pos != self.player.tile:
            self.calculate_ways(self.parent, self.can_walk_at)
            self.calculate_ways(self.parent_wallpass, self.can_walk_at_wallpass)
