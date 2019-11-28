from time import time

import pygame

from src.utils.constants import Color


class Scene:
    """
    Базовый класс сцены.
    Сцены нужны для разделения объктов, которые сейчас активны.
    BG_COLOR — Цвет заднего фона
    MAX_FPS — Максимальный FPS, если 0 <=, то без ограничения
    """
    BG_COLOR = Color.BLACK
    MAX_FPS = 120

    def __init__(self, game_object):
        self.game = game_object

        self.objects = []  # Объекты сцены
        self.create_objects()
        self._delta_time = 0

    def create_objects(self):
        """ Тут надо создавать объекты """
        pass

    def on_switch(self, *args, **kwargs):
        """ Метод, который вызываем, когда переключаемся на эту сцену"""
        pass

    def process_frame(self, eventlist):
        """ Главный метод обработки """
        if self.MAX_FPS > 0:
            start_time = time()

        self.process_all_events(eventlist)
        self.process_all_logic()
        self.process_all_draw()

        if self.MAX_FPS > 0:  # Тут раситываем delta_time, чтобы ограничивать FPS
            self._delta_time = time() - start_time

    def process_all_events(self, eventlist):
        if eventlist is not None:
            for event in eventlist:
                self.process_current_event(event)

    def process_current_event(self, event):
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def process_all_logic(self):
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def process_all_draw(self):
        self.game.screen.fill(self.BG_COLOR)
        for item in self.objects:
            item.process_draw()
        self.additional_draw()
        pygame.display.flip()  # double buffering

        if self.MAX_FPS > 0:  # Если есть ограничения FPS, то немного ждём
            if self._delta_time:
                if 1 / self._delta_time > self.MAX_FPS:
                    pygame.time.wait(min(100, int(1000/((1 / self._delta_time) - self.MAX_FPS))))

    def additional_event_check(self, event):
        pass

    def additional_logic(self):
        pass

    def additional_draw(self):
        pass

    # def set_next_scene(self, index):
    #    self.game.current_scene = index
