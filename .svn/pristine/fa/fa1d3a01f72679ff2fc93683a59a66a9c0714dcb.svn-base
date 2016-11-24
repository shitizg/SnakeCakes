from unittest import TestCase

from snake import Snake
from cake import Cake


class TestSnake(TestCase):

    def test_snake(self):
        snake = Snake()
        snake.health = 20
        cake = Cake("Tasty")
        snake.eat_cake(cake)

        self.assertEquals(snake.health == 35, True)
        self.assertEquals(cake.eaten == 1, True)
        self.assertEquals(snake.score == 1, True)

        cake2 = Cake("Lie")
        snake.eat_cake(cake2)

        self.assertEquals(snake.health == 10, True)
        self.assertEquals(cake2.eaten == 1, True)
        self.assertEquals(snake.score == 2, True)

        pass
