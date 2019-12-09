import pygame

from src.game.menu.menu_items.menu_item_selectable_label import MenuItemSelectableLabel


# def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
#     """
#     Call in a loop to create terminal progress bar
#     @params:
#         iteration   - Required  : current iteration (Int)
#         total       - Required  : total iterations (Int)
#         prefix      - Optional  : prefix string (Str)
#         suffix      - Optional  : suffix string (Str)
#         decimals    - Optional  : positive number of decimals in percent complete (Int)
#         length      - Optional  : character length of bar (Int)
#         fill        - Optional  : bar fill character (Str)
#         printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
#     """
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     filledLength = int(length * iteration // total)
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
#     # Print New Line on Complete
#     if iteration == total:
#         print()


class MenuItemSlider(MenuItemSelectableLabel):
    """
    Класс пункта меню, который слайдер (такая штука, которую можно двигать туда-сюда).
    KEYS_CONTROL — кнопки контроля
    REAL_LENGTH — стандартная длина слайдера
    """
    KEYS_CONTROL = {
        'positive': (pygame.K_RIGHT, pygame.K_d),
        'negative': (pygame.K_LEFT, pygame.K_a),
    }
    REAL_LENGTH = 10

    def __init__(self, game_object, text_object, selected_text_wrapper="{}", selected_color=None, real_length=10,
                 min_value=0, max_value=100, value=0, decimals=1, fill=':', unfill='.', on_change=None):
        """
        :param real_length: Реальная длина слайдера (количество символов)
        :param min_value: Минимальное значение
        :param max_value: Максимальные значение
        :param value: Значение
        :param decimals: Еденица значения
        :param fill: Символ, когда заполнено
        :param unfill: Символ, когда не заполнено
        :param on_change: Функция, которая вызывается, когда значение изменяется
        :type game_object: Game
        :type text_object: TextObject
        :type selected_text_wrapper: str
        :type selected_color: tuple
        :type real_length: int
        :type min_value: float
        :type max_value: float
        :type value: float
        :type decimals: float
        :type fill: str
        :type unfill: str
        :type on_change: function
        """
        super().__init__(game_object, text_object, selected_text_wrapper, selected_color)

        self._text = self.text_object.text
        self.real_length = real_length
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.decimals = decimals
        self.fill = fill
        self.unfill = unfill
        self.on_change_value = on_change

        self.add(0)
        self.set_text(self._text)

    def add(self, x=1):
        """ Изменить значение """
        self.value = max(self.min_value, min((self.value + self.decimals * x), self.max_value))
        self.change_value(self.value)

    def change_value(self, value):
        self.set_text(self._text)
        if self.on_change_value:
            percent = value / (self.max_value - self.min_value)
            self.on_change_value(value, percent)

    def to_str(self):
        """ Генерация строки слайдера """
        filled = int(self.real_length * self.value // self.max_value)
        return filled * self.fill + (self.real_length - filled) * self.unfill

    def set_text(self, text):
        """ Изменение текста """
        self._text = text
        self.text_object.set_text("{}: [{}]".format(self._text, self.to_str()))
        self._force_update()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.KEYS_CONTROL['positive']:
                self.add(1)
            if event.key in self.KEYS_CONTROL['negative']:
                self.add(-1)
