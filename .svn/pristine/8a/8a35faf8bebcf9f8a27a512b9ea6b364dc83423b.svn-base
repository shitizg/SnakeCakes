class Snake:
    def __init__(self, player, name, color):
        if player == "player1":
            self.coords = [(20, 20)]
            self.direction = (1, 0)
        else:
            self.coords = [(3, 20)]
            self.direction = (1, 0)
        self.health = 100
        self.score = 0
        self.player = player
        self.color = color
        self.name = name
        self.controls = "normal"

    def eat_cake(self, cake):
        """Invoked when the Snake's head is on a cake."""

        cake.eaten = 1  # Cake is now eaten, (cannot be undone).
        # Snake eats a tasty Cake and gains 15 health.
        if cake.type == "Tasty":
            self.score += 50
            if self.health + 15 >= 100:
                self.health = 100
            else:
                self.health += 1

        # The Cake was a lie, and the Snake loses 15 heealth.
        if cake.type == "Lie":
            self.score += 1
            self.health -= 25

        if cake.type == "Chaos":
            self.score += 50
            self.controls = "inverted"
            self.health -= 50
