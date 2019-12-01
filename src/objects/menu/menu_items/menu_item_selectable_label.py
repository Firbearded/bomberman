from src.objects.menu.menu_items.base_menu_item import MenuBaseSelectableItem
from src.objects.menu.menu_items.menu_item_label import MenuItemLabel


class MenuItemSelectableLabel(MenuItemLabel, MenuBaseSelectableItem):
    """
    Класс пункта меню, который может быть выбран и имеет текст.
    При выборе этого пунта меню можно изменить цвет и обёртку текста.
    """
    def __init__(self, game_object, text_object, selected_text_wrapper="{}", selected_color=None):
        """
        :param selected_text_wrapper: Обёртка для текста, когда пункт меню будет выбран
        :param selected_color: Цвет пункта меню, когда он будет выбрать
        :type game_object: Game
        :type text_object: TextObject
        :type selected_text_wrapper: str
        :type selected_color: tuple
        """
        MenuBaseSelectableItem.__init__(self, game_object)
        MenuItemLabel.__init__(self, game_object, text_object)

        self.selected_text_wrapper = selected_text_wrapper
        self.selected_color = selected_color

        self._current_stage = self.is_selected
        self._current_text_object = self.text_object

    @property
    def current_text_object(self):
        """ Получить текущий объект текста (зависит от выбранности) """
        if self._current_stage == self.is_selected:
            return self._current_text_object

        self._force_update()

        return self._current_text_object

    def _force_update(self):
        """ Обновить текущий объект текста """
        self._current_stage = self.is_selected
        self._current_text_object = self.text_object.copy

        if self.is_selected:
            if self.selected_text_wrapper is not None:
                self._current_text_object.set_text(self.selected_text_wrapper.format(self._current_text_object.text))
            if self.selected_color is not None:
                self._current_text_object.set_color(self.selected_color)

    @property
    def size(self):
        return self.current_text_object.size

    def process_draw(self, pos):
        self.current_text_object.process_draw(pos)

    def press(self):
        pass
