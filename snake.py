import pygame
import pygame.freetype
from algebra import Vector
from constants import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_WIDTH,
    CELL_HEIGHT,
    HEIGHT_OFFSET,
    MAX_HUNGER)
import random

# Good seed for food
# random.seed(6)
DIRECTIONS = {
    Vector(1, 0): 0,
    Vector(-1, 0): 1,
    Vector(0, 1): 2,
    Vector(0, -1): 3
}


class Snake:
    def __init__(self, length, position, AI):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.color = pygame.Color(r, g, b)
        self.AI = AI
        self.direction = Vector(1, 0)
        self.age = 0
        self.hunger = MAX_HUNGER
        self.score = 0
        self.isDead = False
        self.body = []  # Index 0 is the head
        for i in range(length):
            self.body.append(position - Vector(i, 0))

        # Remember all the directions the snake has gone
        # for the fitness score
        self.fitnessDirs = {
            0: False,
            1: False,
            2: False,
            3: False
        }

    def setDirection(self, direction):
        if self.direction == direction:
            return
        val = DIRECTIONS[direction]
        self.fitnessDirs[val] = True
        self.direction = direction

    @property
    def fitness(self):
        directionScore = 0
        count = 1
        for i in self.fitnessDirs:
            if self.fitnessDirs[i]:
                # directionScore += 4 * 2**count
                count += 1
        foodScore = int((20*self.score)**(1/1.1))
        # print(directionScore, foodScore)
        return self.age + foodScore + directionScore

    def getHeadPosition(self):
        return self.body[0]

    def forward(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0] += self.direction

    def eat(self, length):
        self.hunger += 100
        self.score += 2
        lastIdx = len(self.body) - 1

        for i in range(length):
            self.body.append(Vector(self.body[lastIdx].x, self.body[lastIdx].y))

    def vision(self, world):
        vision = []
        # Left
        direction = Vector(-1, 0)
        w1, t1 = self.findObstacles(direction, world)
        # Up left
        direction = Vector(-1, -1)
        w2, t2 = self.findObstacles(direction, world)
        # Up
        direction = Vector(0, -1)
        w3, t3 = self.findObstacles(direction, world)
        # Up right
        direction = Vector(1, -1)
        w4, t4 = self.findObstacles(direction, world)
        # Right
        direction = Vector(1, 0)
        w5, t5 = self.findObstacles(direction, world)
        # Down right
        direction = Vector(1, 1)
        w6, t6 = self.findObstacles(direction, world)
        # Down
        direction = Vector(0, 1)
        w7, t7 = self.findObstacles(direction, world)
        # Down left
        direction = Vector(-1, 1)
        w8, t8 = self.findObstacles(direction, world)

        foodVision = self.foodVision(world)

        vision.extend([w1, w2, w3, w4, w5, w6, w7, w8])
        vision.extend([t1, t2, t3, t4, t5, t6, t7, t8])
        vision.extend(foodVision)
        return vision

    def foodVision(self, world):
        head = self.body[0]
        pos = world.foods[0].position

        # left, upperLeft, up, upperRight,
        # right, lowerRight, down, lowerLeft
        directions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if pos.y == head.y and pos.x < head.x:
            directions[0] = 1.0
            return directions
        elif pos.y == head.y and pos.x > head.x:
            directions[4] = 1.0
            return directions
        elif pos.x == head.x and pos.y < head.x:
            directions[2] = 1.0
            return directions
        elif pos.x == head.x and pos.y > head.y:
            directions[6] = 1.0
            return directions
        elif pos.x < head.x and pos.y < head.y:
            directions[1] = 1.0
            return directions
        elif pos.x > head.x and pos.y < head.y:
            directions[3] = 1.0
            return directions
        elif pos.x > head.x and pos.y > head.y:
            directions[5] = 1.0
            return directions
        elif pos.x < head.x and pos.y > head.y:
            directions[7] = 1.0
            return directions
        return directions


    def findObstacles(self, direction, world):
        head = self.body[0]
        distance = 0
        pos = head.copy()

        tailDistance = 0
        tailFound = False
        while (pos.x >= 0 and pos.y >= 0 and pos.x < BOARD_WIDTH and pos.y < BOARD_HEIGHT):
            pos = pos + direction
            distance += 1

            if not tailFound and self.checkCollision(pos):
                tailDistance = 1 / distance
                tailFound = True

        wallDistance = 1 / distance
        if not tailFound:
            tailDistance = wallDistance

        return wallDistance, tailDistance

    def checkSelfCollision(self):
        head = self.body[0]
        for i in range(1, len(self.body)):
            if head == self.body[i]:
                return True
        return False

    def checkCollision(self, position):
        for bodyPart in self.body:
            if position == bodyPart:
                return True
        return False

    def draw(self, window):
        head = self.body[0]
        x = head.x * CELL_WIDTH
        y = head.y * CELL_HEIGHT + HEIGHT_OFFSET
        pygame.draw.rect(
                window,
                (130, 130, 130),
                (x, y, CELL_WIDTH, CELL_HEIGHT))

        for i in range(1, len(self.body)):
            part = self.body[i]
            x = part.x * CELL_WIDTH
            y = part.y * CELL_HEIGHT + HEIGHT_OFFSET

            pygame.draw.rect(
                window,
                self.color,
                (x, y, CELL_WIDTH, CELL_HEIGHT))
