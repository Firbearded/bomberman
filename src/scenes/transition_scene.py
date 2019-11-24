import pygame

from src.objects.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import FONT, Color


class TransitionScene(Scene):
    def create_objects(self):
        font_name = FONT
        font_size = 50
        color = Color.WHITE
        aa = True
        pos = self.game.width / 2, self.game.height / 2

        self.text_object = TextObject(self.game, "init", font_name, font_size, pos, color, aa)

        self.objects.append(self.text_object)

    def start(self, next_scene, delay, message):
        self.next_scene = next_scene
        self.delay = delay
        self.text_object.set_text(message)
        w, h = self.text_object.size
        pos = (self.game.width - w) / 2, (self.game.height - h) / 3
        self.text_object.pos = pos
        self.start_time = pygame.time.get_ticks()

    def process_all_logic(self):
        if pygame.time.get_ticks() - self.start_time >= self.delay:
            self.game.set_scene(self.next_scene, 0)
