class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def tuple(self):
        return (self.x, self.y)