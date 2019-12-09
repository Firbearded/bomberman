import pygame

from src.game.base_classes.pygame_object import PygameObject
from src.utils.vector import Point


class Menu(PygameObject):
    """
    Класс меню, в котором хранятся пункты меню.
    Ещё тут обрабатываются отрисовка и изменение индекса выбранного пункта меню
    KEYS — кнопки, по которым переключаем выбранный пункт меню
    INTERVAL — стандартное расстояние между всеми объектами
    """
    KEYS = {
        'down':
            (pygame.K_DOWN, pygame.K_s),
        'up':
            (pygame.K_UP, pygame.K_w),
    }
    INTERVAL = 20

    def __init__(self, game_object, pos=(0, 0), items=None, interval=INTERVAL):
        """
        :type game_object: Game
        :type pos: Point
        :type items: list(MenuItems)
        :type interval: int
        """
        super().__init__(game_object)

        if items is None:
            items = []

        self.pos = pos
        self.items = items
        self.interval = interval

        self.update_selectable_item_indexes()
        self.update_item_positions(self.interval)

    def update_item_positions(self, interval=None):
        """ Обновление позиций для пунктов текста """
        if interval is None:
            interval = self.interval
        self._items_positions = []
        for index in range(len(self.items)):
            x = self.pos[0] - self.items[index].size[0] // 2
            if index == 0:
                y = self.pos[1] + self.items[index].interval_before
            else:
                y = self._items_positions[index - 1][1] + self.items[index - 1].size[1] + interval + \
                    self.items[index - 1].interval_after + self.items[index].interval_before
            self._items_positions.append(Point(x, y))

    def update_selectable_item_indexes(self):
        """ Обновление индексов у пунктов меню, которые можно выбирать """
        self._selectable_item_indexes = []

        for index in range(len(self.items)):
            if self.items[index].is_selectable:
                self._selectable_item_indexes.append(index)

        if len(self._selectable_item_indexes):
            self.selected_index = 0
            self.selected_item.select()

    @property
    def selected_item(self):
        """ Выбранные пункт меню """
        if self.has_selectable_items:
            return self.items[self._selectable_item_indexes[self.selected_index]]
        return None

    @property
    def has_selectable_items(self):
        """ Есть ли пункты меню, которые можно выбрать """
        return self.selected_index is not None

    @property
    def selectable_count(self):
        """ Количество пунктов меню, которые можно выбрать """
        return len(self._selectable_item_indexes)

    def add_selected_index(self, d):
        """ + к selected_index """
        self.selected_item.unselect()
        self.selected_index = (self.selected_index + d) % self.selectable_count
        self.selected_item.select()
        self.update_item_positions(self.interval)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.KEYS['down']:
                self.add_selected_index(1)

            if event.key in self.KEYS['up']:
                self.add_selected_index(-1)

        self.selected_item.process_event(event)

        self.update_item_positions(self.interval)

    def process_draw(self):
        self.update_item_positions(self.interval)
        for index in range(len(self.items)):
            self.items[index].process_draw(self._items_positions[index])
