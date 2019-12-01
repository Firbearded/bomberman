import pygame

from src.objects.menu.menu_items.menu_item_selectable_label import MenuItemSelectableLabel


class MenuItemButton(MenuItemSelectableLabel):
    """
    Класс пункта меню, который кнопка.
    KEYS_PRESS — кнопки, на которые реагирует пункт меню.
    """
    KEYS_PRESS = (pygame.K_SPACE, pygame.K_RETURN)

    def __init__(self, game_object, text_object, selected_text_wrapper="{}", selected_color=None, func=None):
        """
        :param selected_text_wrapper: Обёртка, когда пункт меню выбран
        :param selected_color: Цвет, когда пункт меню выбран
        :param func: Функция, которыя вызывается, когда происходит нажатие на пункт меню
        :type game_object: Game
        :type text_object: TextObject
        :type selected_text_wrapper: str
        :type selected_color: tuple
        :type func: function
        """
        super().__init__(game_object, text_object, selected_text_wrapper, selected_color)

        self.on_press = func

    def press(self):
        if self.on_press:
            self.on_press()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.KEYS_PRESS:
                self.press()
                return
