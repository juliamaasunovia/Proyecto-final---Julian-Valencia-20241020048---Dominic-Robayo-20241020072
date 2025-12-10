class NormalMovement:
    def transform(self, dx, dy, player):
        return dx, dy

class SlowMovement:
    def __init__(self, factor=0.5):
        self.factor = factor
    def transform(self, dx, dy, player):
        return dx * self.factor, dy * self.factor

class InvertedMovement:
    def transform(self, dx, dy, player):
        return -dx, -dy
