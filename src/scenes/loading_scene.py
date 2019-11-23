import pygame

from src.objects.progress_bar import ProgressBar
from src.objects.textobject import TextObject
from src.scenes.base_scene import Scene
from src.utils.constants import Color, FONT_OLD
from src.utils.decorators import protect
from src.utils.loader import TOTAL_NUMBER
from src.utils.vector import Point


class LoadingScene(Scene):
    BG_COLOR = Color.WHITE

    def create_objects(self):
        self.running = True
        stage = "init"
        mx = TOTAL_NUMBER

        w, h = 500, 50
        pos = Point((self.game.width - w) / 2, (self.game.height - h) / 2)
        self.pb = ProgressBar(self.game, pos, (w, h), Color.WHITE, Color.ORANGE, mx=mx)

        pos[1] += h + 10
        self.text = TextObject(self.game, stage, font_name=FONT_OLD, pos=pos)

        self.objects.append(self.pb)
        self.objects.append(self.text)

    def next(self):
        self.pb.add_value(1)

    def set_stage(self, stage):
        self.text.set_text(stage)

    def additional_logic(self):
        if self.pb.is_full:
            self.running = False

    @protect
    def main_loop(self):
        while self.running:
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.running = False
                    break
            if not self.running:
                break
            self.process_frame(eventlist)
