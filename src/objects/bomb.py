import pygame

from src.objects.base_classes.base_objects.timer_object import TimerObject
from src.objects.base_classes.entity import Entity
from src.objects.base_classes.item import Item
from src.objects.supporting.animation import SimpleAnimation
from src.utils.constants import Color
from src.utils.decorators import protect
from src.utils.vector import Vector, Point


class Fire(Entity, TimerObject):
    """
    Класс Fire - огонь, испускаемый бомбой.
    Создается объектом бомбы.
    Висит на поле некоторое время, а потом исчезает.
    """
    DELAY = 500  # Задержка перед исчезновением
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

    COLOR = ((150, 0, 0), (255, 0, 0), (255, 100, 0), (255, 255, 0))  # Запасные цвета

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
        Entity.__init__(self, bomb_object.field_object, round(pos))
        TimerObject.__init__(self, delay)

        self.bomb_object = bomb_object

        self._fire_type = fire_type
        self._direction = Vector(direction)
        self._power = power

        self.on_timeout = self.destroy
        self.start()
        if start_time is not None:
            self._start_time = start_time

        self.generate_next_fire()
        
        self.animation = self.create_animation()

    def is_possible_to_spread(self, pos):
        """ Можем ли мы распространяться на позицию pos """
        return self.field_object.tile_at(pos).empty

    def try_to_break(self, pos):
        """ Пытаемся сломать стену на позиции pos """
        if self.field_object.tile_at(pos).soft:
            self.field_object.destroy_wall(pos, self.delay)

    def generate_next_fire(self):
        """ Генерируем огонь """
        i = Vector(1, 0)
        j = Vector(0, 1)
        all_directions = (i, j, -i, -j)
        if self._fire_type == Fire.FIRE_CENTRAL:
            # Если огонь центральный, пробуем распространиться в стороны
            # Если не получается, меняем тип на маленький
            spreading = False
            if self._power > 1:
                for direction in all_directions:
                    new_pos = self.pos + direction
                    if self.is_possible_to_spread(new_pos):
                        spreading = True
                        Fire(self.bomb_object, new_pos, self._power - 1, self.delay, Fire.FIRE_MIDDLE, direction,
                             self._start_time)
                    else:
                        self.try_to_break(new_pos)

            if not spreading or self._power == 1:
                self._fire_type = Fire.FIRE_SMALL

        if self._fire_type == Fire.FIRE_MIDDLE:
            # Если огонь распространяющийся (промежуточный (не центральный)), пробуем распространиться
            # Если не получается, меняем тип на конечный
            new_pos = self.pos + self._direction
            if self.is_possible_to_spread(new_pos) and self._power > 1:
                Fire(self.bomb_object, new_pos, self._power - 1, self.delay, Fire.FIRE_MIDDLE, self._direction)
            else:
                if self._power > 1:
                    self.try_to_break(new_pos)
                self._fire_type = Fire.FIRE_END

    def additional_logic(self):
        from src.objects.player import Player
        from src.objects.base_classes.enemy import Enemy

        self.timer_logic()

        for e in self.field_object.get_entities(Bomb):  # Проверка на коллизии с бомбами
            if e.is_enabled:
                if e.tile == self.tile:
                    e.on_timeout()
        for cls in (Player, Enemy):
            for e in self.field_object.get_entities(cls):  # Проверка на коллизии с игроками и врагами
                if e.is_enabled:
                    if self.tile == e.tile:
                        e.hurt(self)
        for e in self.field_object.get_entities(Item):  # Проверка на коллизии с предметами
            if e.is_enabled:
                if self.tile == e.tile:
                    e.hurt(self)

    @protect
    def create_animation(self):
        """ Создание анимаций """
        if not self.game_object.images: return

        sprites = [pygame.transform.scale(self.game_object.images[self.SPRITE_CATEGORY][i], self.real_size) for i in
                   self.SPRITE_NAMES[self._fire_type]]

        if self._fire_type in (1, 2):
            angle = {(1, 0): 0, (0, 1): 270, (-1, 0): 180, (0, -1): 90}[tuple(self._direction)]
            sprites = [pygame.transform.rotate(i, angle) for i in sprites]

        animation_delay = self.SPRITE_DELAY
        animation_dict = {'standard': (animation_delay, sprites)}

        return SimpleAnimation(animation_dict, 'standard')

    def process_draw_reserve(self):
        pygame.draw.rect(self.game_object.screen, self.COLOR[self._fire_type], self.real_rect, 0)


class Bomb(Entity, TimerObject):
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

    SOUND_BOOM = 'explosion'

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
        Entity.__init__(self, player_object.field_object, round(pos))
        TimerObject.__init__(self, delay)

        self.player_object = player_object
        self.player_object.inc_active_bombs_number()
        self.power = power
        self.animation = self.create_animation()
        self.field_object.tile_set(self.pos, self.field_object.TILE_UNREACHABLE_EMPTY)
        # ставим под себя невидимую стену
        self.start()

    def additional_logic(self):
        self.timer_logic()

    def on_timeout(self):
        self.game_object.mixer.channels['effects'].sound_play(self.SOUND_BOOM)
        Fire(self, self.pos, self.power)  # Когда таймер заканчивается, то создаём огонь
        self.player_object.dec_active_bombs_number()  # Уменьшаем число активных бомб у игрока
        self.field_object.tile_set(self.pos, self.field_object.TILE_EMPTY)  # Ставим под себя пустую клетку
        self.destroy()  # И уничтожаемся


class BombRemote(Bomb):
    def __init__(self, player_object, pos: Point, power=Bomb.POWER):
        Entity.__init__(self, player_object.field_object, round(pos))
        self.player_object = player_object
        self.player_object.inc_active_bombs_number()
        self.power = power
        self.animation = self.create_animation()
        self.field_object.tile_set(self.pos, self.field_object.TILE_UNREACHABLE_EMPTY)

    def additional_logic(self):
        pass

    def on_timeout(self):
        if self in self.player_object._bombs_remote:
            self.player_object._bombs_remote.remove(self)
        Bomb.on_timeout(self)
