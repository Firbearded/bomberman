import pygame
from src.objects.entity import Entity
from src.utils.vector import Vector, Point


class Fire(Entity):
    """
    Класс Fire - огонь, испускаемый бомбой.
    Создается объектом бомбы в field.entities. Нужно удалить извне, когда enabled станет False.
    Висит на поле некоторое время, а потом исчезает.
    """
    DELAY = 2000
    DIR_DELTA = (Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1))
    FIRE_CENTRAL, FIRE_MIDDLE, FIRE_END, FIRE_SMALL = 0, 1, 2, 3

    def __init__(self, bomb_object, pos: Point, power=0, delay=DELAY, fire_type=FIRE_CENTRAL, direction=Vector(0, 0)):
        """
        :param bomb_object: ссылка на объект бомбы (бомба удалится вскоре после испускания огня, но ничего, ведь огонь
            сразу при создании запросит всю нужную информацию)
        :param pos: позиция на игровом поле
        :param power: дальность распространения огня
        :param delay: задержка в миллисекундах (по умолчанию DELAY)
        :param fire_type: тип огненного потока (по умолчанию центральный)
        :param direction: направление распространения (имеет смысл для серединного и конечного типов)
        :type bomb_object: Bomb
        :type pos: Point
        :type power: int
        :type delay: int
        :type fire_type: int
        :type direction: Vector
        """
        super().__init__(bomb_object.field, pos, (1, 1))
        self.bomb_object = bomb_object

        self.pos = Point()
        self.pos.copy_from(pos)
        self.power = power
        self.delay = delay
        self.fire_type = fire_type
        self.direction = direction

        self.enabled = True
        self.start_time = pygame.time.get_ticks()
        self.next_fire()

    def possible_to_spread(self, pos):
        if self.field.grid[pos.y][pos.x] == 0:
            return True
        if self.field.grid[pos.y][pos.x] == 1:
            return False
        # TODO: Добавить в field метод взрыва разрушаемой стены
        # self.field.destroy_wall(pos.x, pos.y)
        return False

    def next_fire(self):
        if self.fire_type == self.FIRE_CENTRAL:
            # Если огонь центральный, пробуем распространиться в стороны
            # Если не получается, меняем тип на маленький
            spreading = False
            if self.power > 0:
                for v in self.DIR_DELTA:
                    new_fire_pos = self.pos + v
                    if self.possible_to_spread(new_fire_pos):
                        spreading = True
                        new_fire = Fire(self.bomb_object, new_fire_pos, self.power - 1, self.delay, self.FIRE_MIDDLE, v)
                        self.field.entities.append(new_fire)
            if not spreading or self.power == 0:
                self.fire_type = self.FIRE_SMALL

        if self.fire_type == self.FIRE_MIDDLE:
            # Если огонь распространяющийся (серединный), пробуем распространиться
            # Если не получается, меняем тип на конечный
            new_fire_pos = self.pos + self.direction
            if self.possible_to_spread(new_fire_pos) and self.power > 0:
                new_fire = Fire(self.bomb_object, new_fire_pos, self.power - 1, self.delay, self.FIRE_MIDDLE, self.direction)
                self.field.entities.append(new_fire)
            else:
                self.fire_type = self.FIRE_END

    def process_logic(self):
        if self.enabled and (pygame.time.get_ticks() - self.start_time >= self.delay):
            self.enabled = False

    def process_draw(self):
        if not self.enabled:
            return
        if self.fire_type == self.FIRE_CENTRAL:
            fire_color = (150, 0, 0)
        elif self.fire_type == self.FIRE_MIDDLE:
            fire_color = (255, 0, 0)
        elif self.fire_type == self.FIRE_END:
            fire_color = (255, 100, 0)
        elif self.fire_type == self.FIRE_SMALL:
            fire_color = (255, 255, 0)
        pygame.draw.rect(self.game_object.screen, fire_color, (self.real_pos, self.real_size), 0)



class Bomb(Entity):
    """
    Класс Bomb - собственно бомба в игре bomberman.
    Должна создаваться объектом игрока в field.entities. Нужно удалить извне, когда enabled станет False.
    Висит на поле некоторое время, а потом взрывается, распространяя огонь.
    """
    DELAY = 2000

    def __init__(self, player_object, pos: Point, power=0, time=DELAY):
        """
        :param player_object: ссылка на объект игрока, установившего бомбу
        :param pos: позиция бомбы на игровом поле
        :param power: радиус распространения огня (сила бомбы; сила 0 - радиус 1 клетка)
        :param time: время в миллисекундах, через которое бомба взорвется (по умолчанию DELAY)
        :type player_object: Player
        :type pos: Point
        :type power: int
        :type time: int
        """
        super().__init__(player_object.field, pos, (1, 1))
        self.player_object = player_object

        self.power = power
        self.time = time

        self.enabled = True
        self.start_time = pygame.time.get_ticks()

    def detonate(self):
        self.field.entities.append(Fire(self, self.pos, self.power))
        self.enabled = False

    def process_logic(self):
        if self.enabled and (pygame.time.get_ticks() - self.start_time >= self.time):
            self.detonate()

    def process_draw(self):
        if not self.enabled:
            return
        center_pos = (round(self.real_pos[0] + self.real_size[0] / 2), round(self.real_pos[1] + self.real_size[0] / 2))
        pygame.draw.circle(self.game_object.screen, (0, 0, 0), center_pos, int(self.real_size[0] / 2))