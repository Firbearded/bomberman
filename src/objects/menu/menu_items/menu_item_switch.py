from src.objects.menu.menu_items.menu_item_button import MenuItemButton


class MenuItemSwitch(MenuItemButton):
    """ Пункт меню, который может переключаться (тоже самое, что кнопка, но ещё + одно состояние) """
    def __init__(self, game_object, text_object, selected_text_wrapper='{}', selected_color=None, func=None,
                 switched_text=""):
        """
        :param func: Функция, которая вызывается, когда переключают этот пункт меню
        :param switched_text: Текст, когда пункт меню переключён
        :type game_object: Game
        :type text_object: TextObject
        :type selected_text_wrapper: str
        :type selected_color: tuple
        :type func: function
        :type switched_text: str
        """
        super().__init__(game_object, text_object, selected_text_wrapper, selected_color, func)

        self.switched_text = switched_text
        self._switched = False
        self._current_stage = self.is_selected, self.is_switched

    @property
    def current_text_object(self):
        if self._current_stage == (self.is_selected, self.is_switched):
            return self._current_text_object

        self._current_stage = self.is_selected, self.is_switched
        self._current_text_object = self.text_object.copy

        if self.is_switched:
            if self.switched_text is not None:
                self._current_text_object.set_text(self.switched_text)

        if self.is_selected:
            if self.selected_text_wrapper is not None:
                self._current_text_object.set_text(self.selected_text_wrapper.format(self._current_text_object.text))
            if self.selected_color is not None:
                self._current_text_object.set_color(self.selected_color)

        return self._current_text_object

    @property
    def is_switched(self):
        return self._switched

    @property
    def is_not_switched(self):
        return not self._switched

    def toggle(self):
        self._switched = not self._switched

    def switch_on(self):
        self._switched = True

    def switch_off(self):
        self._switched = False

    def press(self):
        self.toggle()
        if self.on_press:
            self.on_press()
