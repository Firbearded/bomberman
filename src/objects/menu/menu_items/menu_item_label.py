from src.objects.menu.menu_items.base_menu_item import MenuBaseItemUnselectable


class MenuItemLabel(MenuBaseItemUnselectable):
    def __init__(self, game_object, text_object):
        super().__init__(game_object)

        self.text_object = text_object

    @property
    def size(self):
        return self.text_object.size

    def process_draw(self, pos):
        self.text_object.process_draw(pos)
