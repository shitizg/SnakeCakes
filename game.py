from OpenGL.GL import *
from OpenGL.GLUT import *
from random import randint

from wx.glcanvas import GLCanvas
import wx

from cake import Cake
from snake import Snake
from high_scores import highscores


def vec_add(x1_y1, x2_y2, limitx, limity):
    """Vector Additon"""
    x1, y1 = x1_y1
    x2, y2 = x2_y2
    newx = x1 + x2
    newy = y1 + y2
    if newx > limitx:
        newx -= limitx
    if newy > limity:
        newy -= limity
    if newx < 0:
        newx += limitx
    if newy < 0:
        newy += limity
    return newx, newy


class SnakeCakes(GLCanvas):
    def __init__(self, parent, numplayers, names, callback):
        """Initialize Game window w/ settings."""
        GLCanvas.__init__(self, parent, -1)
        self.init = True
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self, 1)
        self.timer.Start(200)
        self.callback = callback

        self.snakes = []
        self.isPaused = False

        """Set Initial Game Globals"""
        # window = 0
        self.numtasty = 0
        self.numbad = 0
        self.width, self.height = 500, 500

        self.field_width, self.field_height = 50, 50
        for i in range(numplayers):
            mystring = "player" + str(i)
            self.snakes.append(Snake(mystring, names[i], (randint(0, 10)/10, 1, randint(0, 10)/10)))
        self.cakes = []
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)  # create a window
        glutInitWindowPosition(0, 0)
        self.size = None
        self.window = glutCreateWindow("~Snake Cakes~")  # create window with title

        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutTimerFunc(200, self.update, 0)  # trigger update every 200ms
        glutKeyboardFunc(self.keyboard)
        freeglut.glutCloseFunc(self.callback)
        glutMainLoop()

    def OnPaint(self, event):
        """Paints the game onto the GLCanvas."""
        dc = wx.PaintDC(self)
        # self.SetCurrent()
        self.draw()

    def OnSize(self, event):
        """Re-sizes screen to match wx Menu window."""
        pass

    def glut2dview(self, width, height, internal_width, internal_height):
        """Tells Glut to work in 2d. Source: http://noobtuts.com/python/opengl-introduction"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, internal_width, 0.0, internal_height, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_rect(self, x, y, width, height):
        """Draws a simple rectangle in window. Source; http://noobtuts.com/python/opengl-introduction"""
        glBegin(GL_QUADS)  # start drawing a rectangle
        glVertex2f(x, y)  # bottom left point
        glVertex2f(x + width, y)  # bottom right point
        glVertex2f(x + width, y + height)  # top right point
        glVertex2f(x, y + height)  # top left point
        glEnd()  # done drawing a rectangle

    def draw_snake(self, snake):
        """Draws the Snake as a white rectangle pixel in OpenGL."""
        glColor3f(snake.color[0], snake.color[1], snake.color[2])
        for x, y in snake.coords:
            self.draw_rect(x, y, 1, 1)

    def draw_cakes(self, list_cakes):
        """Draws the Cakes as a rectangle in OpenGL."""
        for cake in list_cakes:
            glColor3f(cake.color[0], cake.color[1], cake.color[2])
            for x, y in cake.position:
                self.draw_rect(x, y, 1, 1)

    def draw_score(self):
        glColor3f(1, .2, .4)
        self.glut_print(10, 10, GLUT.GLUT_BITMAP_9_BY_15, "HELLO World", 1.0, 1.0, 1.0, 1.0)

    def glut_print(self,x, y, font, text, r, g, b, a):

        blending = False
        if glIsEnabled(GL_BLEND):
            blending = True

        glColor3f(r, g, b)
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

        if not blending:
            glDisable(GL_BLEND)

    def draw(self):
        """Draws the Game Scene for Snake Cakes"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.glut2dview(self.width, self.height, self.field_width, self.field_height)
        for snake in self.snakes:
            self.draw_snake(snake)
        self.draw_cakes(self.cakes)
        #self.draw_score()
        glFlush()
        glutSwapBuffers()

    def update(self, args):
        """Callback function for updating game (Moves the Snake and Spawns the Cakes)"""
        if not self.isPaused:
            for snake in self.snakes:
                snake.coords.insert(0, vec_add(snake.coords[0], snake.direction, self.field_width, self.field_height))
                snake.coords.pop()

            glutPostRedisplay()
            # spawn cakes after some time.
            spawn = randint(0, 20)
            if spawn < 2 and self.numtasty < 5:
                self.cakes.append(Cake("Tasty", (1, 1, 0)))  # Spawn a tasty cake for snake
                self.numtasty += 1
            if spawn == 15 and self.numbad < 20:
                self.cakes.append(Cake("Lie", (1, 1, randint(0, 1))))  # The cake is a lie. (Snake loses hp by eating this type)
                self.numbad += 1
            if spawn == 10 and self.numbad < 20:
                self.cakes.append(Cake("Chaos", (1, 1, randint(0, 1))))  # The cake creates chaos and inverts opponents controls.
                self.numbad += 1

            for snake in self.snakes:
                # handle event in which snake eats a cake
                snake_x, snake_y = snake.coords[0]
                for cake in self.cakes:
                    if cake.type == "Tasty":
                        self.numtasty -= 1
                    else:
                        self.numbad -= 1
                    for x, y in cake.position:
                        if snake_x == x and snake_y == y:
                            snake.eat_cake(cake)
                            snake.coords.append((x, y))
                            self.cakes.remove(cake)

            for snake in self.snakes:
                # end game and display score
                if snake.health <= 0:
                    if len(self.snakes) > 1:
                        if self.snakes[0].score > self.snakes[1].score:
                            print("%s wins with score: %d" % (self.snakes[0].name,self.snakes[0].score))
                            scores = highscores("high-score.txt")
                            scores.savenewscore(self.snakes[0].name, self.snakes[0].score)
                        else:
                            print("%s wins with score: %d" % (self.snakes[1].name, self.snakes[1].score))
                            scores = highscores("high-score.txt")
                            scores.savenewscore(self.snakes[0].name, self.snakes[0].score)
                    else:
                        scores = highscores("high-score.txt")
                        scores.savenewscore(self.snakes[0].name, self.snakes[0].score)
                        print("Game Over! %s had score: %d" % (self.snakes[0].name, self.snakes[0].score))

                    freeglut.glutLeaveMainLoop()

        glutTimerFunc(200, self.update, 0)

    def keyboard(self, key, x, y):
        """Keyboard inputs to control what happens as user pushes buttons."""

        # handle the snake movement
        if key == b'w':
            self.snakes[0].direction = (0, 1)  # up
        if key == b's':
            self.snakes[0].direction = (0, -1)  # down
        if key == b'a':
            self.snakes[0].direction = (-1, 0)  # left
        if key == b'd':
            self.snakes[0].direction = (1, 0)  # right

        if key == b'p':
            if self.isPaused:
                self.isPaused = False
            else:
                self.isPaused = True

        glutPostRedisplay()

        # quit out of the game
        if key == b'q':
            freeglut.glutLeaveMainLoop()
