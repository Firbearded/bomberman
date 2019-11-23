from src.objects.menu.menu_items.base_menu_item import MenuBaseItemSelectable


class MenuItemSelectableLabel(MenuBaseItemSelectable):
    def __init__(self, game_object, text_object, text2=None, color2=None):
        super().__init__(game_object)

        self.text_object = text_object

        self.selected_text_object = self.text_object.copy

        if text2 is not None:
            self.selected_text_object.set_text(text2)
        if color2 is not None:
            self.selected_text_object.set_color(color2)

    @property
    def size(self):
        if self.not_selected:
            return self.text_object.size
        return self.selected_text_object.size

    def process_draw(self, pos):
        if self.is_selected:
            self.selected_text_object.process_draw(pos)
        else:
            self.text_object.process_draw(pos)

    def press(self):
        pass
