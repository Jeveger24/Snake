from operator import gt
from random import randint
from pygame.locals import *

import pygame
import time


def color():
    red = randint(0, 255)
    blue = randint(0, 255)
    green = randint(0, 255)
    mix = (red, blue, green)
    return mix


class Apple:
    x = 0
    y = 0
    step = randint(0, 778)

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Player:
    x = [100]
    y = [100]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial position, no collision. Do not really no the point of this
        self.x[1] = 1*44
        self.x[2] = 2*44

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

             # update previous position
            for i in range(self.length-1, 0, -1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Game:
    def is_collision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


class App:
    window_width = 20
    window_height = 20
    player = 0
    apple = 0
    snake_image = 40
    apple_image = 20

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3)
        self.apple = Apple(1, 1)


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width * self.snake_image, self.window_height * self.snake_image), pygame.HWSURFACE)
        pygame.display.set_caption('Snake')
        self._running = True
        self._image_surf = pygame.Surface((self.snake_image, self.snake_image), pygame.SRCALPHA)
        pygame.draw.rect(self._image_surf, color(), (10, 10, self.snake_image, self.snake_image))
        self._apple_surf = pygame.Surface((self.apple_image, self.apple_image), pygame.SRCALPHA)
        pygame.draw.rect(self._apple_surf, color(), (0, 0, self.apple_image, self.apple_image))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # does snake eat apple?
        for i in range(0, self.player.length):
            if self.game.is_collision(self.apple.x, self.apple.y, self.player.x[i], self.player.y[i], 40):
                self.apple.x = randint(1, 780)
                self.apple.y = randint(1, 779)
                self.player.length = self.player.length + 1

        # does snake collide?
        for i in range(2, self.player.length):
            if self.game.is_collision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 40):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)

        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.player.move_right()

            if keys[K_LEFT]:
                self.player.move_left()

            if keys[K_UP]:
                self.player.move_up()

            if keys[K_DOWN]:
                self.player.move_down()

            if keys[K_ESCAPE]:
                self._running = False

            self.on_loop()
            self.on_render()
            time.sleep(50.0 / 1000.0);
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

