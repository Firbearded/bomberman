class Tuple:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    @property
    def tuple(self):
        return (self.w, self.h)