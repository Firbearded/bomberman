from src.objects.menu.menu_items.base_menu_item import MenuBaseItem


class MenuItemLabel(MenuBaseItem):
    """ Класс пункта меню, который нельзя выбрать, но имеет текст """
    def __init__(self, game_object, text_object):
        """
        :param text_object: объект класса TextObject
        :type game_object: Game
        :type text_object: TextObject
        """
        super().__init__(game_object)

        self.text_object = text_object

    @property
    def size(self):
        """ Реальный размер пункта меню """
        return self.text_object.size

    def set_text(self, text):
        self.text_object.set_text(text)

    def process_draw(self, pos):
        self.text_object.process_draw(pos)
