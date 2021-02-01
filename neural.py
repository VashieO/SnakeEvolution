import numpy as np
from nnfs.datasets import spiral_data

# np.random.seed(0)


class LayerDense:
    def __init__(self, inputCount, neuronCount, basedOnLayer=None):
        if basedOnLayer is not None:
            self.weights = np.array(basedOnLayer.weights)
            self.biases = np.array(basedOnLayer.biases)
            return

        self.inputCount = inputCount
        self.neuronCount = neuronCount
        self.weights = (2 * np.random.random((inputCount, neuronCount)) - 1) * 0.8
        self.biases = (2 * np.random.random((1, neuronCount)) - 1) * 0.8
        # self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
        # self.biases = 0.1 * np.random.randn(1, n_neurons)
        # self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

    def copy(self):
        layer = LayerDense(self.inputCount, self.neuronCount)
        layer.weights = self.weights.copy()
        layer.biases = self.biases.copy()
        return layer

    # def __str__(self):
    #     return str(self.weights) + "\n" + str(self.biases)


class ActivationReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
        return self.output


class ActivationSoftMax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        self.output = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        return self.output


class ActivationSigmoid:
    def forward(self, inputs):
        self.output = 1 / (1 + np.exp(-inputs))
        return self.output


class Loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        return np.mean(sample_losses)


class LossCategoricalCrossEntropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

        if len(y_true.shape) == 1:
            correct_confindences = y_pred_clipped[range(samples), y_true]
        elif len(y_pred.shape) == 2:
            correct_confindences = np.sum(y_pred_clipped * y_true, axis=1)
        negative_log_likelihoods = -np.log(correct_confindences)
        return negative_log_likelihoods


class SnakeAI:
    """
    --Snake inputs--
    Distance left wall
    Distance right wall
    Distance top wall
    Distance bottom wall
    Distance to food X
    Distance to food Y

    -- Output --
    1. Go left
    2. Go up
    3. Go right
    4. Go down
    """

    def __init__(self, ID=None):
        self.ID = ID
        self.layer1 = LayerDense(24, 16)
        self.activation1 = ActivationSigmoid()

        self.layer2 = LayerDense(16, 16)
        self.activation2 = ActivationSigmoid()

        # self.layer3 = LayerDense(14, 10)
        # self.activation3 = ActivationSigmoid()

        self.outLayer = LayerDense(16, 4)
        self.outActivation = ActivationSigmoid()
        # self.outActivation = ActivationSoftMax()

        self.fitness = 0

    def copy(self):
        copy = SnakeAI()
        copy.layer1 = self.layer1.copy()
        copy.layer2 = self.layer2.copy()
        copy.outLayer = self.outLayer.copy()
        return copy

    def prediction(self, inputs):
        self.layer1.forward(inputs)
        self.activation1.forward(self.layer1.output)
        self.layer2.forward(self.activation1.output)
        self.activation2.forward(self.layer2.output)
        # self.layer3.forward(self.activation2.output)
        # self.activation3.forward(self.layer3.output)
        self.outLayer.forward(self.activation2.output)
        self.outActivation.forward(self.outLayer.output)

        output = self.outActivation.output[0]
        return list(zip(output, range(len(output))))

    # def __str__(self):
    #     return str(self.fitness)

    # def __repr__(self):
    #     return str(self.fitness)

# X, y = spiral_data(samples=100, classes=3)

# dense1 = LayerDense(2, 3)
# activation1 = ActivationReLU()

# dense2 = LayerDense(3, 3)
# activation2 = ActivationSoftMax()

# loss_function = LossCategoricalCrossEntropy()

# dense1.forward(X)
# activation1.forward(dense1.output)

# dense2.forward(activation1.output)
# activation2.forward(dense2.output)

# print(activation2.output[:5])

# print(y)
# loss = loss_function.calculate(activation2.output, y)

# print(loss)
