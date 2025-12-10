class Command:
    def execute(self):
        raise NotImplementedError
    def undo(self):
        raise NotImplementedError

class MoveCommand(Command):
    def __init__(self, player, dx, dy):
        self.player = player
        self.dx, self.dy = dx, dy
        self.prev_pos = (player.x, player.y)

    def execute(self):
        self.player.move(self.dx, self.dy)

    def undo(self):
        self.player.x, self.player.y = self.prev_pos
        if hasattr(self.player, "update_rect"):
            self.player.update_rect()

class RestartCommand(Command):
    def __init__(self, caretaker):
        self.caretaker = caretaker
        self.previous = caretaker.get_memento()

    def execute(self):
        self.caretaker.restore()

    def undo(self):
        if self.previous:
            self.caretaker.restore(self.previous)
