from src.objects.menu.menu_items.base_menu_item import MenuBaseItemSelectable


class MenuItemSelectableLabel(MenuBaseItemSelectable):
    def __init__(self, game_object, text_object, selected_text_wrapper="{}", selected_color=None):
        super().__init__(game_object)

        self.text_object = text_object

        self.selected_text_wrapper = selected_text_wrapper
        self.selected_color = selected_color

        self._current_stage = self.is_selected
        self._current_text_object = self.text_object

    @property
    def current_text_object(self):
        if self._current_stage == self.is_selected:
            return self._current_text_object

        self._current_stage = self.is_selected
        self._current_text_object = self.text_object.copy

        if self.is_selected:
            if self.selected_text_wrapper is not None:
                self._current_text_object.set_text(self.selected_text_wrapper.format(self._current_text_object.text))
            if self.selected_color is not None:
                self._current_text_object.set_color(self.selected_color)

        return self._current_text_object

    @property
    def size(self):
        return self.current_text_object.size

    def process_draw(self, pos):
        self.current_text_object.process_draw(pos)

    def press(self):
        pass
