from src.objects.menu.menu_items.menu_item_selectable_label import MenuItemSelectableLabel


class MenuItemButton(MenuItemSelectableLabel):
    def __init__(self, game_object, text_object, text2=None, color2=None, func=None):
        super().__init__(game_object, text_object, text2, color2)

        self.func = func

    def press(self):
        if self.func:
            self.func()
