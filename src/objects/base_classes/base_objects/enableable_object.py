class EnableableObject(object):
    def __init__(self, enabled=False):
        self._enabled = enabled

    @property
    def is_enabled(self):
        """
        :rtype: bool
        """
        return self._enabled

    @property
    def is_disabled(self):
        """
        :rtype: bool
        """
        return not self._enabled

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def toggle(self):
        self._enabled = not self._enabled

    def set_enabled(self, b):
        self._enabled = bool(b)
