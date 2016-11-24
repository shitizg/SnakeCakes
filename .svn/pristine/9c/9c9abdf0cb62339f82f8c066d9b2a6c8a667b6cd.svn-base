from OpenGL.raw.GLUT import glutPostRedisplay

from game import SnakeCakes, sys


class Multiplayer(SnakeCakes):
    def __init__(self, parent, names, callback):
        """Initialize single-player SnakeCakes Game"""
        SnakeCakes.__init__(self, parent, 2, names, callback)

    def keyboard(self, key, x, y):
        """Keyboard inputs to control what happens as user pushes buttons."""

        # handle Player1 movement
        if key == b'w':
            self.snakes[0].direction = (0, 1)  # up
        if key == b's':
            self.snakes[0].direction = (0, -1)  # down
        if key == b'a':
            self.snakes[0].direction = (-1, 0)  # left
        if key == b'd':
            self.snakes[0].direction = (1, 0)  # right

        # handle Player2 movement
        if key == b'i':
            self.snakes[1].direction = (0, 1)  # up
        if key == b'k':
            self.snakes[1].direction = (0, -1)  # down
        if key == b'j':
            self.snakes[1].direction = (-1, 0)  # left
        if key == b'l':
            self.snakes[1].direction = (1, 0)

        if key == b'p':
            if self.isPaused:
                self.isPaused = False
            else:
                self.isPaused = True

        glutPostRedisplay()

        # quit out of the game
        if key == b'q':
            sys.exit(0)
