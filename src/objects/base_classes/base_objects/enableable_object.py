class EnableableObject(object):
    """ Класс объекта, который может быть включеным или выключеным. """

    def __init__(self, enabled=False):
        self._enabled = enabled

    @property
    def is_enabled(self):
        """
        Активен ли этот объект
        :rtype: bool
        """
        return self._enabled

    @property
    def is_disabled(self):
        """
        Не активен ли этот объект
        :rtype: bool
        """
        return not self._enabled

    def enable(self):
        """ Активировать объект """
        self._enabled = True

    def disable(self):
        """ Деактивировать объект """
        self._enabled = False

    def toggle(self):
        """ Переключить состояние объекта """
        self._enabled = not self._enabled

    def set_enabled(self, b):
        """
        :type b: bool
        """
        self._enabled = bool(b)
