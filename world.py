import pygame
import pygame.freetype
import random
from algebra import Vector
from constants import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_WIDTH,
    CELL_HEIGHT,
    HEIGHT_OFFSET,
    FOOD_COLOR)

DIRECTIONS = {
    0: Vector(-1, 0),
    1: Vector(0, -1),
    2: Vector(1, 0),
    3: Vector(0, 1)
}


class Cell:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Board:
    def __init__(self, cellsX, cellsY, cellWidth, cellHeight, color):
        self.cellsX = cellsX
        self.cellsY = cellsY
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.color = color

        self.cells = []
        for y in range(cellsY):
            for x in range(cellsX):
                self.cells.append(Cell(x * cellWidth, y * cellHeight, cellWidth, cellHeight))

    def draw(self, window):
        pygame.draw.rect(
                window,
                self.color,
                (0, 0 + HEIGHT_OFFSET, BOARD_WIDTH * CELL_WIDTH, BOARD_HEIGHT * CELL_HEIGHT),
                width=1)
        # for cell in self.cells:
        #     pygame.draw.rect(
        #         window,
        #         self.color,
        #         (cell.x, cell.y + HEIGHT_OFFSET, cell.width, cell.height),
        #         width=1)


class Food:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self, window):
        x = self.position.x * CELL_WIDTH
        y = self.position.y * CELL_HEIGHT
        pygame.draw.rect(
            window,
            self.color,
            (x, y + HEIGHT_OFFSET, CELL_WIDTH, CELL_HEIGHT))


class World:
    def __init__(self, snake):
        self.snake = snake
        self.MAX_FOOD = 1
        self.foods = []
        for i in range(self.MAX_FOOD):
            self.foods.append(Food(self.randomFoodLocation(), FOOD_COLOR))
        # self.population = genetic.SnakePopulation(SNAKES_PER_GENERATION, SNAKES_PARALLEL)
        self.testBestSnake = False

    def randomFoodLocation(self):
        foodX = random.randint(0, BOARD_WIDTH - 1)
        foodY = random.randint(0, BOARD_HEIGHT - 1)
        return Vector(foodX, foodY)

    def randomFood(self, food):
        food.position = self.randomFoodLocation()

    def forward(self):
        if self.snake.isDead:
            return
        inputs = self.snake.vision(self)
        output = self.snake.AI.prediction(inputs)
        maxDirection = max(output)

        self.snake.setDirection(DIRECTIONS[maxDirection[1]])

        self.snake.hunger -= 1
        self.snake.age += 1
        self.snake.forward()

        food = self.foodCollision(self.snake.body[0])
        if food:
            print("Hit food")
            self.randomFood(food)
            self.snake.eat(2)

        isDead = False
        if self.snake.hunger == 0 or self.snake.checkSelfCollision():
            isDead = True
        if self.checkBorderCollision(self.snake.getHeadPosition()):
            isDead = True

        if isDead:
            self.snake.isDead = True

        # if self.testBestSnake:
        #     snake = self.population.getBestSnake()
        #     self.population.simulateSnake(snake, self)
        # else:
        #     self.population.simulate(self)

    def draw(self, window):
        self.snake.draw(window)
        # if self.testBestSnake:
        #     snake = self.population.getBestSnake()
        #     snake.draw(window)
        # else:
        #     for snake in self.population.getSnakes():
        #         snake.draw(window)
        for food in self.foods:
            food.draw(window)

    def checkBorderCollision(self, position):
        if (position.x < 0 or position.x > BOARD_WIDTH - 1 or
                position.y < 0 or position.y > BOARD_HEIGHT - 1):
            return True
        return False

    def foodCollision(self, position):
        for food in self.foods:
            if food.position == position:
                return food
        return None
