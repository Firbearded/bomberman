class PygameObject(object):
    def __init__(self, game_object):
        """
        :type game_object: Game
        """
        self._game_object = game_object

    @property
    def game_object(self):
        return self._game_object

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self):
        pass
