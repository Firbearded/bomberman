import pygame
import sys

from src.objects.base_classes import DrawableObject
from src.objects.text import Text
from src.utils.constants import Color
from src.utils.vector import Point


class MenuItem(DrawableObject):
    def __init__(self, text1, text2 = None, func = None, selectable=True):
        self.text1 = text1
        self.text2 = text2
        self.func = func
        self.selectable = selectable
        self.selected = False
        self.size = text1.size

    def process_draw(self):
        if (self.selected):
            pass
            #print(self.text2.pos)
            self.text2.process_draw()
        else:
            pass
            #print(self.text1.pos)
            self.text1.process_draw()


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

    #функция задания х и у айтемов, а также добавление нужного в массив selectable_items
    def create_items_parameters(self):
        #вычисление интервала таким образом, чтобы в итоге получилось что-то вроде: пустота, текст, пустота, текст, пустота
        self.interval = self.game_object.height / (len(self.items) + 1)
        j = 0
        #х, у - примерные координаты айтемов
        y = self.interval
        x = self.game_object.width / 2
        for i in self.items:
            #w, h - параметры текста
            w, h = i.size
            #real_x, real_y - координаты текущего item
            real_x = x - w / 2
            real_y = y - h / 2
            i.text1.pos = Point(real_x, real_y)
            i.text2.pos = Point(real_x, real_y)
            if (i.selectable):
                self.selectable_items.append(i)
            j += 1
            y += self.interval

        #выделение первой кнопки, счтобы изначально была выделена хотябы одна
        self.selectable_items[0].selected = True

    def process_event(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_w or event.key == pygame.K_UP):
                #selected прошлого выделенного объекта ставим в 0
                self.selectable_items[self.selected].selected = False
                self.selected += 1
                if (self.selected >= len(self.items)):
                    self.selected = 0
                # selected нового выделенного объекта ставим в 1
                self.selectable_items[self.selected].selected = True

            if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                # selected прошлого выделенного объекта ставим в 0
                self.selectable_items[self.selected].selected = False
                self.selected -= 1
                if (self.selected < 0):
                    self.selected = len(self.items) - 1
                # selected нового выделенного объекта ставим в 1
                self.selectable_items[self.selected].selected = True

            if (event.key == pygame.K_SPACE):
                self.selectable_items[self.selected].func()

    def process_logic(self):
        pass

    def process_draw(self):
        for i in self.items:
             i.process_draw()



