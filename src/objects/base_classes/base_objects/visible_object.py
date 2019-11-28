class VisibleObject(object):
    def __init__(self, visible=False):
        self._visible = visible

    @property
    def is_visible(self):
        """
        :rtype: bool
        """
        return self._visible

    @property
    def is_invisible(self):
        """
        :rtype: bool
        """
        return not self._visible

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    def toggle(self):
        self._visible = not self._visible

    def set_visible(self, b):
        self._visible = bool(b)
