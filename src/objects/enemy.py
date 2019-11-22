import random
from src.objects.entity import Entity
from src.utils.vector import Vector, Point


class Enemy(Entity):

    def __init__(self, field, pos: Point = (0, 0), size: tuple = (1, 1)):
        super().__init__ (field, pos, size)
        self.speed_vector = self.new_target_direction()
        self.is_stable = True  #Показывает, заперт ли enemy в 4 стенах, изначально True на случай, если заперт сразу
        self.dist_from_center = 0 #Дистанция до центра ближайшей клетки
        self.growing = 1 #Растёт ли дистанция до центра клетки или убывает

    def new_target_direction(self):
        d_x = -1, 0, 1, 0
        d_y = 0, -1, 0, 1
        possible_directions = []
        target_direction = Vector()
        tile_x, tile_y = self.tile
        for i in range(4):
            if (self.field.grid[d_y[i] + tile_y][d_x[i] + tile_x] == 0):
                d = Vector(d_x[i], d_y[i])
                possible_directions.append(d)

        if len(possible_directions) == 0:
            self.is_stable = True
            return target_direction

        direction_number = random.randint(1, len(possible_directions)) - 1 #Получение случайного направления из
        target_direction = possible_directions[direction_number]           #массива возможных направлений
        self.is_stable = False
        return target_direction

    def center_checking(self, normalized_speed_vector, past_tile): #Проверка, в центре ли клетки enemy и вызов new_target_direction
        self.dist_from_center += normalized_speed_vector.length * self.growing      #При прибавлении может быть погрешность в 10^(-17), но она потом сама исчезает
        if (self.dist_from_center > -0.000001) and (self.dist_from_center < 0.000001):
            self.speed_vector = self.new_target_direction ()
        if self.tile != past_tile: #Проверка на переход в новую клетку
            self.dist_from_center -= normalized_speed_vector.length * self.growing  #Так как при переходе в новую клетку происходит прибавление
            self.growing *= -1                                                      #в dist_from_center до 0.52, 0.2 надо вычесть

    def process_logic(self):
        self.death()
        past_tile = self.tile # Клетка, в которой мы либо остаёмся, либо из которой выходим
        if not self.is_stable:
            normalized_speed_vector = self.speed_vector.normalized * self.speed_value
            self.pos = self.pos + normalized_speed_vector
            self.center_checking(normalized_speed_vector, past_tile)
        else:                                               #Если enemy заперт,
            self.speed_vector = self.new_target_direction() #он ищет путь выхода

    def death(self):
        pass







