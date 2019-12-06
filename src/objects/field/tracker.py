from src.utils.vector import Vector
from src.objects.player import Player
from queue import Queue

class Tracker:
    """
    Класс, рассчитывающий для мобов пути до игрока
    """

    delta = [Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]
    STRAIGHT_VISION_DIST = 10

    def __init__(self, field_object):
        self.field_object = field_object

        # Матрицы путей
        self.parent = []
        self.straight = []

    def can_walk_at(self, tile):
        """ Функция разрешенности клетки """
        return self.field_object.tile_at(tile).walkable

    def init_matrix(self):
        """ Инициализация матриц путей """
        self.parent.clear()
        self.straight.clear()
        for i in range(self.field_object.width):
            self.parent.append([])
            self.straight.append([])
            for j in range(self.field_object.height):
                self.parent[i].append(None)
                self.straight[i].append(False)

    def calculate_ways(self):
        """ Расчет путей до игрока """
        # Обнуление матриц путей
        for i in range(self.field_object.width):
            for j in range(self.field_object.height):
                self.parent[i][j] = None
                self.straight[i][j] = False
        # Расчет путей до игрока обходом в ширину
        player_pos = self.field_object.get_entities(Player)[0].tile
        queue = Queue()
        if self.can_walk_at(player_pos):
            self.parent[player_pos.x][player_pos.y] = player_pos
            queue.put(player_pos)
        while not queue.empty():
            current_pos = queue.get()
            for v in self.delta:
                new_pos = current_pos + v
                if self.can_walk_at(new_pos) and not self.parent[new_pos.x][new_pos.y]:
                    self.parent[new_pos.x][new_pos.y] = current_pos
                    queue.put(new_pos)
        # Расчет прямой видимости игрока из клеток
        self.straight[player_pos.x][player_pos.y] = True
        for v in self.delta:
            current_pos = player_pos
            for i in range(self.STRAIGHT_VISION_DIST):
                current_pos += v
                if not self.can_walk_at(current_pos):
                    break
                self.straight[current_pos.x][current_pos.y] = True

    def get_next_tile(self, tile):
        """ Получение следующей клетки на пути """
        return self.parent[tile.x][tile.y]

    def get_straight_vision(self, tile):
        """ Есть ли прямая видимость игрока из клетки """
        return self.straight[tile.x][tile.y]

    def process_logic(self):
        """ Логика работы Tracker'а - расчет путей """
        # Инициализация матриц, если их размеры не соответствуют размеру поля
        if self.field_object.width != len(self.parent) or self.field_object.height != len(self.parent[0]):
            self.init_matrix()
        # Cобственно расчет
        self.calculate_ways()
