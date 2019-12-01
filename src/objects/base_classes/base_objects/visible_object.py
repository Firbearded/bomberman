class VisibleObject(object):
    """ Класс объекта, который может быть виден или нет """
    def __init__(self, visible=False):
        self._visible = visible

    @property
    def is_visible(self):
        """
        Виден ли объект
        :rtype: bool
        """
        return self._visible

    @property
    def is_invisible(self):
        """
        Не виден ли объект
        :rtype: bool
        """
        return not self._visible

    def show(self):
        """ Показать объект """
        self._visible = True

    def hide(self):
        """ Спрятать объект """
        self._visible = False

    def toggle(self):
        """ Переключить видимость объекта """
        self._visible = not self._visible

    def set_visible(self, b):
        """
        :type b: bool
        """
        self._visible = bool(b)
