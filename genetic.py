import neural
from snake import Snake
from algebra import Vector
from world import World
import random
from constants import SNAKE_START_POS
import math

DIRECTIONS = {
    0: Vector(-1, 0),
    1: Vector(0, -1),
    2: Vector(1, 0),
    3: Vector(0, 1)
}


class SnakePopulation:
    def __init__(self, amountPerGeneration, parallelAmount):
        self.parallelAmount = parallelAmount
        self.genetic = GeneticAlgorithm(amountPerGeneration)
        self.runBestSnake = False
        self.showSpecimen = 0
        self.currentSpecimenWorld = None

        # Simulate each world and snake separately
        self.worlds = []
        current = self.genetic.getNext()
        while current and len(self.worlds) < parallelAmount:
            world = World(Snake(8, SNAKE_START_POS, current))
            self.worlds.append(world)
            current = self.genetic.getNext()

    def showTopSpecimen(self, value):
        self.currentSpecimenWorld = None
        if value >= 0 and value < 4:
            print("Show specimen", value)
            self.showSpecimen = value

    def getTopSpecimen(self):
        network = self.genetic.getTopNetwork(self.showSpecimen)
        if network is None:
            return None
        if self.currentSpecimenWorld is None:
            print("Best network", network.fitness)
            self.currentSpecimenWorld = World(Snake(8, SNAKE_START_POS, network))
            return self.currentSpecimenWorld
        if self.currentSpecimenWorld.snake.isDead:
            print("Best network", network.fitness)
            self.currentSpecimenWorld = World(Snake(8, SNAKE_START_POS, network))
            return self.currentSpecimenWorld
        return self.currentSpecimenWorld

    def getGenerationID(self):
        return self.genetic.AIGeneration

    def simulateSnake(self, world):
        world.forward()

        snake = world.snake
        if snake.isDead:
            snake.isDead = True
            fitness = snake.fitness
            print("fitness:", fitness, snake.AI.fitness)

    def simulate(self):
        if self.runBestSnake:
            world = self.getTopSpecimen()
            if world:
                self.simulateSnake(world)
            return

        # If snake dies add to list
        deadWorlds = []
        for world in self.worlds:
            world.forward()

            snake = world.snake
            if snake.isDead:
                snake.AI.fitness = snake.fitness
                # print("fitness:", snake.AI.fitness)
                deadWorlds.append(world)

        for world in deadWorlds:
            self.worlds.remove(world)

        if len(self.worlds) == 0:  # When all snakes are dead create a new generation
            self.genetic.createNewGeneration()

        if len(self.worlds) < self.parallelAmount:
            current = self.genetic.getNext()
            while current and len(self.worlds) < self.parallelAmount:
                self.worlds.append(World(Snake(8, SNAKE_START_POS, current)))
                current = self.genetic.getNext()

    def draw(self, window):
        if self.runBestSnake:
            world = self.getTopSpecimen()
            if world:
                world.draw(window)
        else:
            for world in self.worlds:
                world.draw(window)

    # def setDead(self, snake):
    #     snake.isDead = True
    #     snake.AI.fitness = snake.score * 10 + snake.age

    def getSnakes(self):
        return self.snakes


class GeneticAlgorithm:
    def __init__(self, amountPerGeneration):
        self.amountPerGeneration = amountPerGeneration
        self.AIGeneration = 1
        self.currentIndex = 0
        self.IDcounter = 0
        self.currentBestNetwork = None
        self.topNetworks = []
        self.neuralNetworks = self._generate(amountPerGeneration)
        for i in range(min(4, len(self.neuralNetworks))):
            self.topNetworks.append(self.neuralNetworks[i])

    def _generate(self, amount):
        " Create a set of random neural networks "
        networks = []
        for i in range(amount):
            networks.append(neural.SnakeAI(self.IDcounter))
            self.IDcounter += 1
        return networks

    def getNext(self):
        if self.currentIndex >= len(self.neuralNetworks):
            return None

        network = self.neuralNetworks[self.currentIndex]
        self.currentIndex += 1
        return network

    def getTopNetwork(self, index):
        if index >= 0 and index < len(self.topNetworks):
            return self.topNetworks[index]
        return None

    def naturalSelection(self, networks, amount, fromCount):
        fitnessSum = 0
        temp = []
        for i in range(fromCount):
            fitnessSum += networks[i].fitness
            temp.append(networks[i])

        weights = [item.fitness/fitnessSum for item in temp]
        print(temp, weights)
        return random.choices(temp, cum_weights=weights, k=amount)

    def createNewGeneration(self):
        self.AIGeneration += 1
        self.currentIndex = 0

        topPerforming = self.sortByFitness()
        print("Set current best network", topPerforming[0].fitness)

        # choices = self.naturalSelection(topPerforming, 4, 10)
        # print(choices)
        self.topNetworks.clear()
        for i in range(4):
            self.topNetworks.append(topPerforming[i])

        # Choose the top and breed with top 10%
        # breedCount = int(len(topPerforming) / 10 + 1)

        self.neuralNetworks.clear()
        # Have a low rate of mutation on the top ones but still enough mutate
        # into something better.

        LIMIT = 5
        for i in range(LIMIT):
            # self.neuralNetworks.append(topPerforming[i])
            self.neuralNetworks.append(self.mutate(topPerforming[i].copy(), 10, 0.2))

            print("Breeding: ", topPerforming[i].fitness)
            for j in range(1, len(topPerforming) // (LIMIT + 1)):
                new = self.breedUniform(topPerforming[i], topPerforming[j])
                self.mutate(new, 20 + 10 * i, 0.1 + 0.05 * i)
                self.neuralNetworks.append(new)

        print("Length:", len(self.neuralNetworks))
        if len(self.neuralNetworks) < self.amountPerGeneration:
            amount = self.amountPerGeneration - len(self.neuralNetworks)
            print("Adding:", amount)
            self.neuralNetworks.extend(self._generate(amount))

        # counter = 1
        # for i in range(3, len(self.neuralNetworks)):
        #     self.mutate(self.neuralNetworks[i], 40, 0.2)
        #     counter += 1

    def sortByFitness(self):
        return sorted(self.neuralNetworks, key=lambda x: x.fitness, reverse=True)

    def breedOnepoint(self, network1, network2):
        new = neural.SnakeAI()
        self.uniformCross(new.layer1, network1.layer1, network2.layer1)
        self.uniformCross(new.layer2, network1.layer2, network2.layer2)
        # self.uniformCross(new.layer3, network1.layer3, network2.layer3)
        self.uniformCross(new.outLayer, network1.outLayer, network2.outLayer)
        return new

    def crossOnepoint(self, newLayer, layer1, layer2):
        newLayer.weights = layer1.weights.copy()
        newWeights = newLayer.weights
        weights2 = layer2.weights
        for i in range(weights2.shape[0]):
            for j in range(weights2.shape[1]):
                choice = random.choices((newWeights[i][j], weights2[i][j]), cum_weights=(0.5, 1.0))[0]
                newWeights[i][j] = choice

    def breedUniform(self, network1, network2):
        new = neural.SnakeAI()
        self.uniformCross(new.layer1, network1.layer1, network2.layer1)
        self.uniformCross(new.layer2, network1.layer2, network2.layer2)
        # self.uniformCross(new.layer3, network1.layer3, network2.layer3)
        self.uniformCross(new.outLayer, network1.outLayer, network2.outLayer)
        return new

    def uniformCross(self, newLayer, layer1, layer2):
        newLayer.weights = layer1.weights.copy()
        newWeights = newLayer.weights
        weights2 = layer2.weights
        for i in range(weights2.shape[0]):
            for j in range(weights2.shape[1]):
                choice = random.choices((newWeights[i][j], weights2[i][j]), cum_weights=(0.5, 1.0))[0]
                newWeights[i][j] = choice

        newLayer.biases = layer1.biases.copy()
        row = newLayer.biases[0]
        for i in range(len(row)):
            choice = random.choices((row[i], layer2.biases[0][i]), cum_weights=(0.5, 1.0))[0]
            row[i] = choice

    def mutate(self, network, chance, rate):
        self.mutateLayer(network.layer1, chance, rate)
        self.mutateLayer(network.layer2, chance, rate)
        # self.mutateLayer(network.layer3, chance, rate)
        self.mutateLayer(network.outLayer, chance, rate)
        return network

    def mutateLayer(self, layer, chance, rate):
        weights = layer.weights
        for i in range(weights.shape[0]):
            for j in range(weights.shape[1]):
                if random.randint(0, 100) < chance:
                    weight = weights[i][j] + (2 * random.random() - 1) * rate
                    weights[i][j] = min(max(weight, -1), 1)

        row = layer.biases[0]
        for i in range(len(row)):
            if random.randint(0, 100) < chance:
                bias = row[i] + (2 * random.random() - 1) * rate
                row[i] = min(max(bias, -1), 1)
