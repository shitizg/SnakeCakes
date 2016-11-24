from random import randint


class Cake:
    def __init__(self, type, color):
        self.position = []
        self.type = type
        self.eaten = 0
        self.color = color
        x, y = randint(0, 50), randint(0, 50)
        self.position.append((x, y))

