from src.objects.base_classes.base_objects.pygame_object import PygameObject


class MenuBaseItem(PygameObject):
    def __init__(self, game_object):
        super().__init__(game_object)
        self._selectable = False
        self.interval_before = 0
        self.interval_after = 0

    @property
    def is_selectable(self):
        return self._selectable

    def process_draw(self, pos):
        pass


class MenuBaseSelectableItem(MenuBaseItem):
    def __init__(self, game_object):
        super().__init__(game_object)
        self._selectable = True
        self._selected = False

    @property
    def is_selected(self):
        return self._selected

    @property
    def not_selected(self):
        return not self._selected

    def select(self):
        self._selected = True

    def unselect(self):
        self._selected = False

    def toggle(self):
        self._selected = not self._selected

    def set_selected(self, b):
        self._selected = bool(b)
