from game import Game
from level import levels

class GameFacade:
    def __init__(self):
        self.game = Game()

    def start(self, level_index: int = 0):
        self.load_level(level_index)

    def load_level(self, idx: int):
        self.game.load_level(idx)

    def restart(self):
        self.game.restart()

    def undo(self):
        self.game.undo()

    def update(self, dt: float):
        self.game.update(dt)

    def draw(self):
        self.game.draw()

    def is_victory(self) -> bool:
        return self.game.player.level >= len(levels) - 1

    def get_player(self):
        return self.game.player

    def get_game(self):
        return self.game
