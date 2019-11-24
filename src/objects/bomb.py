import pygame

from src.objects.base_classes.entity import Entity
from src.objects.tiles import TILES
from src.utils.animation import SimpleAnimation
from src.utils.constants import Color
from src.utils.decorators import protect
from src.utils.intersections import is_collide_rect
from src.utils.vector import Vector, Point


class Fire(Entity):
    """
    Класс Fire - огонь, испускаемый бомбой.
    Создается объектом бомбы.
    Висит на поле некоторое время, а потом исчезает.
    """
    DELAY = 500
    FIRE_CENTRAL = 0
    FIRE_MIDDLE = 1
    FIRE_END = 2
    FIRE_SMALL = 3

    SPRITE_CATEGORY = "fire_sprites"
    SPRITE_NAMES = (
        ('fire_wave_start',),
        ('fire_wave', 'fire_wave1'),
        ('fire_wave_end',),
        ('points',)
    )
    SPRITE_DELAY = 100

    COLOR = ((150, 0, 0), (255, 0, 0), (255, 100, 0), (255, 255, 0))

    def __init__(self, bomb_object, pos: Point, power=0, delay=DELAY, fire_type=FIRE_CENTRAL, direction=Vector(0, 0),
                 start_time=None):
        """
        :param bomb_object: ссылка на объект бомбы (бомба удалится вскоре после испускания огня, но ничего, ведь огонь
            сразу при создании запросит всю нужную информацию)
        :param pos: позиция на игровом поле
        :param power: дальность распространения огня
        :param delay: задержка в миллисекундах (по умолчанию DELAY)
        :param fire_type: тип огненного потока (по умолчанию FIRE_CENTRAL)
        :param direction: направление распространения (имеет смысл для серединного и конечного типов)
        :type bomb_object: Bomb
        :type pos: Point
        :type power: int
        :type delay: int
        :type fire_type: int
        :type direction: Vector
        """
        if power <= 0:
            return
        self.fire_type = fire_type
        self.direction = Vector(direction)
        super().__init__(bomb_object.field_object, pos)
        self.bomb_object = bomb_object

        self.pos = Point(pos)
        self.power = power
        self.delay = delay

        self.start_time = start_time
        if start_time is None:
            self.start_time = pygame.time.get_ticks()

        self.next_fire()

    def is_possible_to_spread(self, pos):
        tile_type = self.field_object.grid[pos.y][pos.x]
        if TILES[tile_type].walkable:
            return True
        return False

    def try_to_break(self, pos):
        if TILES[self.field_object.grid[pos.y][pos.x]].soft:
            self.field_object.destroy_wall(pos.x, pos.y, self.delay)

    def next_fire(self):
        i = Vector(1, 0)
        j = Vector(0, 1)
        all_directions = (i, j, -i, -j)
        if self.fire_type == self.FIRE_CENTRAL:
            # Если огонь центральный, пробуем распространиться в стороны
            # Если не получается, меняем тип на маленький
            spreading = False
            if self.power > 1:
                for direction in all_directions:
                    new_pos = self.pos + direction
                    if self.is_possible_to_spread(new_pos):
                        spreading = True
                        Fire(self.bomb_object, new_pos, self.power - 1, self.delay, self.FIRE_MIDDLE, direction,
                             self.start_time)
                    else:
                        self.try_to_break(new_pos)

            if not spreading or self.power == 1:
                self.fire_type = self.FIRE_SMALL

        if self.fire_type == self.FIRE_MIDDLE:
            # Если огонь распространяющийся (серединный (не центральный)), пробуем распространиться
            # Если не получается, меняем тип на конечный
            new_pos = self.pos + self.direction
            if self.is_possible_to_spread(new_pos) and self.power > 1:
                Fire(self.bomb_object, new_pos, self.power - 1, self.delay, self.FIRE_MIDDLE, self.direction)
            else:
                if self.power > 1:
                    self.try_to_break(new_pos)
                self.fire_type = self.FIRE_END

        self.reload_animations()

    def additional_logic(self):
        from src.objects.player import Player
        from src.objects.base_classes.enemy import Enemy
        if pygame.time.get_ticks() - self.start_time >= self.delay:
            self.destroy()

        for e in self.field_object.entities:  # Проверка на коллизии с бомбами и игроками
            if e.is_enabled:
                if type(e) is Bomb:
                    if is_collide_rect(self.pos, self.size, e.pos, e.size):
                        e.on_timeout()
                elif type(e) is Player:
                    if self.tile == e.tile:
                        e.on_hurt(self)
                elif issubclass(type(e), Enemy):
                    if self.tile == e.tile:
                        e.on_hurt(self)

    @protect
    def create_animation(self):
        if not self.game_object.images: return

        sprites = [pygame.transform.scale(self.game_object.images[self.SPRITE_CATEGORY][i], self.real_size) for i in
                   self.SPRITE_NAMES[self.fire_type]]
        if self.fire_type in (1, 2):
            angle = {(1, 0): 0, (0, 1): 270, (-1, 0): 180, (0, -1): 90}[tuple(self.direction)]
            sprites = [pygame.transform.rotate(i, angle) for i in sprites]
        animation_delay = self.SPRITE_DELAY
        animation_dict = {'burning': (animation_delay, sprites)}
        return SimpleAnimation(animation_dict, 'burning')

    def process_draw_reserve(self):
        pygame.draw.rect(self.game_object.screen, self.COLOR[self.fire_type], (self.real_pos, self.real_size), 0)


class Bomb(Entity):
    """
    Класс Bomb - собственно бомба в игре bomberman.
    Должна создаваться объектом игрока.
    Висит на поле некоторое время, а потом взрывается, распространяя огонь.
    """
    DELAY = 2000
    POWER = 2

    SPRITE_CATEGORY = "bomb_sprites"
    SPRITE_NAMES = ('bomb', 'bomb1', 'bomb2')
    SPRITE_DELAY = 100

    SOUND_BOMB = 'explosion'

    COLOR = Color.GREEN

    def __init__(self, player_object, pos: Point, power=POWER, delay=DELAY):
        """
        :param player_object: ссылка на объект игрока, установившего бомбу
        :param pos: позиция бомбы на игровом поле
        :param power: радиус распространения огня (сила бомбы; сила 0 - радиус 1 клетка)
        :param delay: время в миллисекундах, через которое бомба взорвется (по умолчанию DELAY)
        :type player_object: Player
        :type pos: Point
        :type power: int
        :type delay: int
        """
        super().__init__(player_object.field_object, pos)
        self.player_object = player_object

        self.power = power
        self.delay = delay

        self.start_time = pygame.time.get_ticks()
        x, y = self.pos
        self.field_object.grid[y][x] = self.field_object.TILE_UNREACHABLE_EMPTY

    def on_timeout(self):
        Fire(self, self.pos, self.power)
        self.player_object.bombs_number -= 1
        x, y = self.tile
        self.field_object.grid[y][x] = self.field_object.TILE_EMPTY
        self.destroy()

    def additional_logic(self):
        if pygame.time.get_ticks() - self.start_time >= self.delay:
            self.on_timeout()
