import random
import numpy as np
import math
#import matplotlib.pyplot as plt

'''
outputG1 = []
outputG2 = []
gen = 0
genG = []
'''


class Layer():
    def __init__(self, weights, nodes):  # number of nodes on previous layer, number of nodes
        self.nodes = nodes
        self.connections = weights
        self.biases = []
        self.weights = np.empty([nodes, weights])
        for n in range(nodes):
            self.biases.append(random.randint(-10, 10) / 10)

        for n in range(nodes):
            for i in range(weights):
                self.weights[n - 1, i - 1] = random.randint(-10, 10) / 10

    def output(self, input):
        self.outputs = np.matmul(self.weights, input)
        self.outputs = self.outputs + self.biases
        #for n in range(len(self.outputs)):
            #self.outputs[n - 1] = math.tanh(self.outputs[n - 1])

        return self.outputs

    def mutate(self, mutationRate):

        for n in range(len(self.biases)):
            for i in range(len(self.weights)):
                if random.randint(0, 10) / 10 < mutationRate:
                    self.weights[n - 1, i - 1] = self.weights[n - 1, i - 1] + random.randint(-100, 100) / 1000
            if random.randint(0, 10) / 10 < mutationRate:
                self.biases[n - 1] = self.biases[n - 1] + random.randint(-100, 100) / 1000

    def crossover(self, Partner, mutationRate):
        child = Layer(self.connections, self.nodes)
        for n in range(self.nodes):
            for i in range(self.connections):
                if random.choice((0, 1)) == 0:
                    child.weights[n - 1, i - 1] = self.weights[n - 1, i - 1]
                else:
                    child.weights[n - 1, i - 1] = Partner.weights[n - 1, i - 1]
            if random.choice((0, 1)) == 0:
                child.biases[n-1] = self.biases[n-1]
            else:
                child.biases[n-1] = Partner.biases[n-1]
        child.mutate(mutationRate)
        return child


class Network:
    def __init__(self, inputNodes, hiddenLayer, hiddenNodes, outputNodes):
        self.inputNodes = inputNodes
        self.hiddenLayer = hiddenLayer
        self.hiddenNodes = hiddenNodes
        self.outputNodes = outputNodes
        self.hiddenLayers = []
        if hiddenLayer == 0:
            self.directLayer = Layer(inputNodes, outputNodes)
        else:
            self.firstLayer = Layer(inputNodes, hiddenNodes)
            for n in range(hiddenLayer):
                self.hiddenLayers.append(Layer(hiddenNodes, hiddenNodes))
            self.lastLayer = Layer(hiddenNodes, outputNodes)

    def output(self, input):
        self.input = input
        if len(self.hiddenLayers) == 0:
            return self.directLayer.output(self.input)
        else:
            self.input = self.firstLayer.output(self.input)
            for n in range(len(self.hiddenLayers) - 1):
                self.input = self.hiddenLayers[n - 1].output(self.input)
            return self.lastLayer.output(self.input)

    def mutate(self, mutationRate):
        if len(self.hiddenLayers) == 0:
            self.directLayer.mutate(mutationRate)
        else:
            self.firstLayer.mutate(mutationRate)
            for n in range(len(self.hiddenLayers) - 1):
                self.hiddenLayers[n - 1].mutate(mutationRate)
            self.lastLayer.mutate(mutationRate)

    def crossover(self, Partner, mutationRate):
        child = Network(self.inputNodes, self.hiddenLayer, self.hiddenNodes, self.outputNodes)
        if len(self.hiddenLayers) == 0:
            child.directLayer = self.directLayer.crossover(Partner.directLayer, mutationRate)
        else:
            child.firstLayer = self.firstLayer.crossover(Partner.firstLayer, mutationRate)
            for n in range(len(self.hiddenLayers) - 1):
                child.hiddenLayers[n-1] = self.hiddenLayers[n - 1].crossover(Partner.hiddenLayers[n - 1], mutationRate)
            child.lastLayer = self.lastLayer.crossover(Partner.lastLayer, mutationRate)
        return child


'''network = Network(3, 0, 0, 1)
input = [1, 2, 3]
print(network.output(input))
for i in range(10000):
    network.mutate(0.5)
    genG.append(gen)
    gen += 1
    outputG1.append(network.output(input)[0])
    print(network.output(input))'''

'''
plt.plot(genG, outputG1, label="line1")
plt.title('output')
plt.xlabel('generation')
plt.ylabel('output')
plt.grid()
plt.show()
'''
