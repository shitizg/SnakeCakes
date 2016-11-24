from game import SnakeCakes


class Singleplayer(SnakeCakes):
    def __init__(self, parent, names, callback):
        """Initialize single-player SnakeCakes Game"""
        SnakeCakes.__init__(self, parent, 1, names, callback)
