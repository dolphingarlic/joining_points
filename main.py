'''
Joining Points
Inspired by IOI 2006 Joining Points

Created by Andi Qu
'''

from random import randint

import pygame
from pygame.locals import QUIT

SIZE = (640, 640)
DIAMETER = 10

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

NUM_POINTS = 24


def ccw(A, B, C):
    '''
    Checks if B is counterclockwise from C with origin A
    '''
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    '''
    Determines if the lines (A, B) and (C, D) intersect
    '''
    if (A == C or A == D or B == C or B == D):
        return False
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


component = [i for i in range(NUM_POINTS)]


def find(A):
    '''
    Find of DSU
    '''

    while A != component[A]:
        component[A], A = component[component[A]], component[A]
    return A


def union(A, B):
    '''
    Union of DSU
    '''

    component[find(A)] = component[find(B)]


class Point(pygame.sprite.Sprite):
    '''
    A class representing a point in the game
    '''

    def __init__(self, colour, pos, num):
        super().__init__()

        self.colour = colour
        self.id = num

        self.image = pygame.Surface((DIAMETER, DIAMETER))
        self.image.fill(BLACK)
        pygame.draw.ellipse(self.image, colour, (0, 0, DIAMETER, DIAMETER))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Game():
    '''
    A class representing the actual game and its state
    '''

    def __init__(self):
        self._running = True
        self._drawing = False
        self._clicked_colour = None
        self._clicked_pos = None
        self._clicked = -1
        self._display_surf = None
        self._image_surf = None

        self.points = pygame.sprite.Group()
        self.lines = []

    def on_init(self):
        '''
        Handles initiation of the game
        '''

        pygame.init()
        self._display_surf = pygame.display.set_mode(SIZE, pygame.HWSURFACE)
        self._running = True
        pygame.display.set_caption('Joining Points')

    def on_event(self, event):
        '''
        Handles events
        '''

        if event.type == QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked = [
                point for point in self.points if point.rect.collidepoint(pos)]

            if self._drawing:
                self._drawing = False
                if clicked and clicked[0].rect.center != self._clicked_pos and clicked[0].colour == self._clicked_colour:
                    # Check if the new line intersects any existing lines
                    for line in self.lines:
                        if intersect(line[1], line[2], self._clicked_pos, clicked[0].rect.center):
                            return

                    # Check that the two points you're connecting aren't already connected
                    if find(clicked[0].id) != find(self._clicked):
                        self.lines.append(
                            (self._clicked_colour, self._clicked_pos, clicked[0].rect.center))
                        union(clicked[0].id, self._clicked)
            else:
                if clicked:
                    self._drawing = True
                    self._clicked_colour = clicked[0].colour
                    self._clicked_pos = clicked[0].rect.center
                    self._clicked = clicked[0].id

    def on_loop(self):
        '''
        Handles game logic
        '''

        self.points.update()

    def on_render(self):
        '''
        Renders points and lines
        '''

        self._display_surf.fill(BLACK)
        self.points.draw(self._display_surf)

        for line in self.lines:
            pygame.draw.line(self._display_surf, line[0], line[1], line[2], 2)

        if self._drawing:
            pygame.draw.line(self._display_surf, self._clicked_colour,
                             self._clicked_pos, pygame.mouse.get_pos(), 2)

        pygame.display.flip()

    def on_execute(self):
        '''
        Called when first executing game
        '''

        if self.on_init():
            self._running = False

        self.points.add(Point(GREEN, (10, 10), 0))
        self.points.add(Point(GREEN, (SIZE[0] - 20, 10), 1))
        self.points.add(Point(RED, (10, SIZE[1] - 20), 2))
        self.points.add(Point(RED, (SIZE[0] - 20, SIZE[1] - 20), 3))

        for i in range((NUM_POINTS - 4) // 2):
            self.points.add(
                Point(GREEN, (randint(11, SIZE[0] - 21), randint(11, SIZE[1] - 21)), 4 + 2 * i))
            self.points.add(
                Point(RED, (randint(11, SIZE[0] - 21), randint(11, SIZE[1] - 21)), 5 + 2 * i))

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        pygame.quit()


if __name__ == "__main__":
    GAME = Game()
    GAME.on_execute()
