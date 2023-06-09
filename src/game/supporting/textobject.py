import pygame

from src.game.base_classes.pygame_object import PygameObject
from src.game.supporting.constants import Color
from src.utils.vector import Point


class TextObject(PygameObject):
    """
    Класс для обработки и отрисовки текста

    (5 points (размер шрифта) ≈ 6 pixels (по вертикали))
    """

    @staticmethod
    def points_to_pixels(points):
        """
        Перевод размера шрифта в примерную высоту текста
        :param points: float
        :rtype: float
        """
        return points * 6 / 5

    @staticmethod
    def pixels_to_points(pixels):
        """
        Перевод высоты текста в примерный размер шрифта
        :param pixels: float
        :rtype: float
        """
        return pixels * 5 / 6

    def __init__(self, game_object, text, font_name=None, font_size=12, pos=Point(0, 0), color=Color.BLACK,
                 antialiasing=False):
        """

        :param game_object: Объект класса Game
        :param text: Сам текст
        :param pos: Координаты левой верхней точки
        :param font_name: Имя шрифта (None => стандартный
        :param font_size: Размер шрифта
        :param color: Цвет (R, G, B)
        :param antialiasing: Сглаживание
        :type game_object: Game
        :type text: str
        :type pos: Point, tuple
        :type font_name: str
        :type font_size: int
        :type color: tuple из (0..255, 0..255, 0..255)
        :type antialiasing: bool
        """
        super().__init__(game_object)
        self.pos = Point(pos)
        self.text = str(text)
        self.antialiasing = bool(antialiasing)
        self.color = color

        self.font_name = font_name

        self.update_font(font_name, font_size)

    # Методы setter'ы
    def set_fontname(self, name):
        self.update_font(name=name)

    def set_fontsize(self, size):
        self.update_font(size=size)

    def set_text(self, text):
        self.text = str(text)
        self.update_surface()

    def set_antialiasing(self, aa):
        self.antialiasing = bool(aa)
        self.update_surface()

    def set_color(self, color):
        self.color = color
        self.update_surface()

    @property
    def size(self):
        """
        Размер получившегося текста.
        :return: (w, h)
        :rtype: tuple
        """
        return self.textsurface.get_size()

    @property
    def copy(self):
        return TextObject(self.game_object, self.text, self.font_name, self.font_size,
                          self.pos, self.color, self.antialiasing)

    def update_font(self, name=None, size=None):
        """
        Исменение шрифта
        :param name: Имя шрифта
        :param size: Размер шрифта
        :type name: str
        :type size: float
        """
        if name: self.font_name = name
        if size: self.font_size = size

        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.update_surface()

    def update_surface(self):
        """
        Обновление поверхности текста.
        (self.textsurface тут примерно как объект изображения, но не совсем)
        """
        self.textsurface = self.font.render(self.text, self.antialiasing, self.color)

    def process_draw(self, pos=None):
        """
        Отрисовка текста.
        :param pos: Позиция левого верхнего угла текста
        :param color: Цвет
        :type pos: Point
        """
        if not pos:
            pos = self.pos

        self.game_object.screen.blit(self.textsurface, tuple(pos))
