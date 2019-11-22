from src.objects.base_classes import DrawableObject
from src.objects.text import Text
from src.utils.constants import Color
import pygame


class MenuItem:
    def __init__(self, text1, text2 = None, func = None, selectable=True):
        self.text1 = text1
        self.text2 = text2
        self.func = func
        self.selectable = selectable
        self.selected = False


class Menu(DrawableObject):
    def __init__(self, game_object, pos=(0, 0), items=[], interval=50):
        self.game_object = game_object
        self.pos = pos
        self.items = items
        self.selectable_items = []
        self.interval = interval
        self.selected = 0
        self.items_pos = []
        self.create_items_parameters()
        self.selectable_items_indexes = []

    # задание х и у, а также добавление в массивы selectable_items и массив индексов
    def create_items_parameters(self):
        self.interval = self.game_object.height / self.items
        j = 0
        for i in self.items:
            x, y = i.text1.size()
            x = self.game_object.width / 2 - x / 2
            y = self.interval * j + self.interval / 2 - y / 2
            i.text1.pos = (x, y)
            i.text2.pos = (x, y)
            if (i.selectable):
                self.selectable_items.append(i)
                self.selectable_items_indexes.append(j)
            j += 1

    def process_event(self, event):
        if (event == pygame.K_UP or event == pygame.K_w):
            self.selected += 1
            if (self.selected >= len(self.items)):
                self.selected = 0
        if (event == pygame.K_DOWN or event == pygame.K_s):
            self.selected -= 1
            if (self.selected < 0):
                self.selected = len(self.items) - 1
        if (event == pygame.K_SPACE):
            pass
            #self.selectable_items[self.selected].func()
            #пока что выбор ничего не делает

    def process_logic(self):
        pass

    def process_draw(self):
        #это самый тупой путь отрисовки, даже без массиова индексов
        #сначала рисуем все selectable_items, включая тот, что selected
        for i in range (len(self.selectable_items)):
            if (i == self.selected):
                self.selectable_items[i].text2.process_draw()
            else:
                self.selectable_items[i].text1.process_draw ()
        #затем рисуем всё остальное. медленнее, но глупее и экономнее в теории
        for i in range(len(self.items)):
            if (not self.items[i].selectable):
                self.items[i].text1.process_draw()


