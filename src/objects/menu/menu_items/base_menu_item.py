from src.objects.base_classes.base_objects.pygame_object import PygameObject


class MenuBaseItem(PygameObject):
    """ Базовый класс пункта меню, который нельзя выбирать """
    def __init__(self, game_object):
        """
        :type game_object: Game
        selectable — можно ли выбирать этот пункт меню
        interval_before — доп. переменная на интервал перед этим пунктом меню
        interval_after — доп. переменная на интервал после этого пункта меню
        """
        super().__init__(game_object)
        self._selectable = False
        self.interval_before = 0
        self.interval_after = 0

    @property
    def is_selectable(self):
        """ Может ли быть выбран этот пункт предмет """
        return self._selectable

    def process_draw(self, pos):
        pass


class MenuBaseSelectableItem(MenuBaseItem):
    """ Базовый класс пункта меню, который можно выбрать """
    def __init__(self, game_object):
        """
        :type game_object: Game
        selected — выбран ли этот пункт меню
        """
        super().__init__(game_object)
        self._selectable = True
        self._selected = False

    @property
    def is_selected(self):
        """
        Выбран ли этот пункт меню
        :rtype: bool
        """
        return self._selected

    @property
    def not_selected(self):
        """
        Не выбран ли этот пункт меню
        :rtype: bool
        """
        return not self._selected

    def select(self):
        """ Выбрать этот пункт меню """
        self._selected = True

    def unselect(self):
        """ Убрать выбор этого пунта меню """
        self._selected = False

    def toggle(self):
        self._selected = not self._selected

    def set_selected(self, b):
        """
        :type b: bool
        """
        self._selected = bool(b)
