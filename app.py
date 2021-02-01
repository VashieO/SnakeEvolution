import pygame
import pygame.freetype
import world
import genetic
from constants import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_WIDTH,
    CELL_HEIGHT,
    SNAKES_PER_GENERATION,
    SNAKES_PARALLEL)


class App:
    def __init__(self):
        self._running = True
        self.window = None
        self.size = self.weight, self.height = 800, 600
        self.board = world.Board(BOARD_WIDTH, BOARD_HEIGHT, CELL_WIDTH, CELL_HEIGHT, pygame.Color(255, 255, 255))
        self.population = genetic.SnakePopulation(SNAKES_PER_GENERATION, SNAKES_PARALLEL)
        # self.world = World()
        self.lastUpdated = 0
        self.step = False
        self.nextStep = False

    def on_init(self):
        pygame.init()
        self.font = pygame.freetype.SysFont("Arial", 24)
        self.window = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_LEFT:
            #     if self.world.snake.direction != Vector(1, 0):
            #         self.world.snake.direction = Vector(-1, 0)
            # if event.key == pygame.K_RIGHT:
            #     if self.world.snake.direction != Vector(-1, 0):
            #         self.world.snake.direction = Vector(1, 0)
            # if event.key == pygame.K_UP:
            #     if self.world.snake.direction != Vector(0, 1):
            #         self.world.snake.direction = Vector(0, -1)
            # if event.key == pygame.K_DOWN:
            #     if self.world.snake.direction != Vector(0, -1):
            #         self.world.snake.direction = Vector(0, 1)
            if event.key == pygame.K_1:
                self.population.showTopSpecimen(0)
                self.population.runBestSnake = True
            if event.key == pygame.K_2:
                self.population.showTopSpecimen(1)
                self.population.runBestSnake = True
            if event.key == pygame.K_3:
                self.population.showTopSpecimen(2)
                self.population.runBestSnake = True
            if event.key == pygame.K_4:
                self.population.showTopSpecimen(3)
                self.population.runBestSnake = True
            if event.key == pygame.K_p:
                self.step = not self.step
            if event.key == pygame.K_SPACE:
                self.nextStep = True
            if event.key == pygame.K_t:
                self.population.runBestSnake = not self.population.runBestSnake

    def on_loop(self):
        timer = pygame.time.get_ticks()
        dt = pygame.time.get_ticks() - self.lastUpdated

        GAME_SPEED = 50
        if (not self.step and dt > GAME_SPEED) or (self.step and self.nextStep):
            self.nextStep = False
            self.population.simulate()
            self.lastUpdated = timer // GAME_SPEED * GAME_SPEED

    def on_render(self):
        self.window.fill((25, 25, 25))
        self.board.draw(self.window)
        self.population.draw(self.window)

        # self.font.render_to(self.window, (50, 10), "Score: %s" % self.world.score, (255, 255, 255))
        # self.font.render_to(self.window, (250, 10), "Hunger: %s" % self.world.hunger, (255, 255, 255))
        # self.font.render_to(self.window, (450, 10), "AI: %s" % self.world.genetic.currentIndex, (255, 255, 255))
        self.font.render_to(self.window, (600, 10), "Generation: %s" % self.population.getGenerationID(), (255, 255, 255))

        # if self.world.isDead:
        #     self.font.render_to(self.window, (330, 300), "Game Over", (255, 255, 255))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
