import os, random, sys, time
import pygame, pygame.gfxdraw

try:
    import psyco
    psyco.full()
except:
    pass

TILE_WIDTH = 32
TILE_HEIGHT = 32

PIXEL_WIDTH = 800
PIXEL_HEIGHT = 608

GRID_WIDTH = PIXEL_WIDTH / TILE_WIDTH
GRID_HEIGHT = PIXEL_HEIGHT / TILE_HEIGHT

class Mode(object):
    def __init__(self, game):
        self.game = game
    def handle(self, ev):
        pass

class BaseMode(Mode):
    def handle(self, ev):
        if ev.type == pygame.QUIT:
            self.game.done = True
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                self.game.done = True
            else:
                print "unhandled key: %s" % ev.key

class Level(object):
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.rooms = []
        self.map = Map(w, h)

        self.randomize()
        self.build()

    def randomize(self):
        for i in range(10):
            self.random_room()

    def build(self):
        for room in self.rooms:
            room.build(self.map)

    def random_room(self):
        #w = random.randint(5, 13)
        #h = random.randint(5, w)
        w = random.randint(5, 7)
        h = random.randint(5, w)

        squares = list(range(self.width * self.height))
        random.shuffle(squares)

        for i in squares:
            y0 = i / self.width
            x0 = i % self.width
            x1 = x0 + w
            y1 = y0 + h
            if x1 > self.width: continue
            if y1 > self.height: continue

            ok = True
            for room in self.rooms:
                if room.conflicts(x0, y0, x1, y1):
                    ok = False
                    break

            if not ok:
                continue
            self.rooms.append(Room(x0, y0, w, h))
            return
        print "failed to construct %sx%s room" % (w, h)

class Room(object):
    def __init__(self, x, y, w, h):
        self.x0 = x
        self.y0 = y
        self.height = h
        self.width = w
        self.x1 = x + w
        self.y1 = y + h
    def build(self, m):
        for y in xrange(self.y0 + 1, self.y1 - 1):
            span = y * m.width
            for x in xrange(self.x0 + 1, self.x1 - 1):
                m.cells[span + x] = True
    def conflicts(self, x0, y0, x1, y1):
        return (((self.x0 == x0) or (self.x1 == x1) or
                 (self.x0 < x0 and x0 < self.x1) or
                 (self.x0 < x1 and x1 < self.x1) or
                 (x0 < self.x0 and self.x1 < x1)) and
                ((self.y0 == y0) or (self.y1 == y1) or
                 (self.y0 < y0 and y0 < self.y1) or
                 (self.y0 < y1 and y1 < self.y1) or
                 (y0 < self.y0 and self.y1 < y1)))

class Map(object):
    def __init__(self, w, h):
        self.height = h
        self.width = w
        self.cells = [False for i in xrange(h * w)]

class Tiles(object):
    def __init__(self):
        self.wall = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.wall.fill(pygame.Color(100, 70, 80, 255))

        self.open = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.open.fill(pygame.Color(30, 20, 30, 255))

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.modes = []
        self.base = BaseMode(self)
        self.tiles = Tiles()
        self.level = Level(GRID_WIDTH, GRID_HEIGHT)

    def handle(self, ev):
        if self.modes:
            self.modes[-1].handle(ev)
        else:
            self.base.handle(ev)

    def run(self):
        #pygame.mixer.music.load('snd/music.mp3')
        #pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()

        self.draw()
        pygame.display.flip()

        while not self.done:
            self.clock.tick(60)

            for event in pygame.event.get():
                self.handle(event)

            self.draw()
            pygame.display.flip()

        pygame.mixer.fadeout(300)

    def draw(self):
        for y in xrange(GRID_HEIGHT):
            span = y * GRID_WIDTH
            for x in xrange(GRID_WIDTH):
                #if random.randint(0, 1) == 0:
                #    t = self.tiles.wall
                #else:
                #    t = self.tiles.open

                if self.level.map.cells[span + x]:
                    t = self.tiles.open
                else:
                    t = self.tiles.wall
                self.screen.blit(t, (x * TILE_WIDTH, y * TILE_HEIGHT))

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.mixer.init(frequency=44100)

    #flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF

    screen = pygame.display.set_mode((PIXEL_WIDTH, PIXEL_HEIGHT), flags)
    g = Game(screen)
    g.run()
