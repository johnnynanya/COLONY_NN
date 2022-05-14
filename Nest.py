import random
import numpy as np
import math
import pygame
from NN import *
from Ant import *
from Food import *

vec = pygame.math.Vector2


class Nest:
    def __init__(self):
        self.pos = vec(pygame.display.get_surface().get_size()[0] / 2, pygame.display.get_surface().get_size()[1] / 2)
        self.numAnts = 20
        self.Ants_alive = []
        self.Ants_dead = []
        self.body = pygame.Rect(0, 0, 40, 40)
        self.color = (0, 255, 0)
        self.start_energy = 5000
        self.energy = self.start_energy
        self.turns = 0
        self.brain = Network(4, 1, 3, 2)

        # initialize Food
        self.Foods = []
        self.FoodNum = 300
        for i in range(self.FoodNum):
            self.Foods.append(Food())

        for i in range(self.numAnts):
            self.Ants_alive.append(Ant(self.brain))

    def Turn_draw(self, screen):
        for i in range(len(self.Ants_alive)):
            if self.turns % 100 == 0:
                self.Ants_alive[i].Decide(self)
            self.Ants_alive[i].Move(self, self.Foods)

            if self.Ants_alive[i].energy <= 0:
                self.Ants_dead.append(self.Ants_alive[i])
                self.Ants_alive.pop(i)
                break

            self.Ants_alive[i].Draw(screen)
        if self.energy <= 0:
            self.Ants_dead.append(x for x in self.Ants_alive)
            self.Ants_alive.clear()
        self.energy -= 5

        for i in range(len(self.Foods)):
            self.Foods[i].Draw(screen)

        self.Draw(screen)
        self.turns += 1

    def Turn(self):
        for i in range(len(self.Ants_alive)):
            if self.turns % 100 == 0:
                self.Ants_alive[i].Decide(self)
            self.Ants_alive[i].Move(self, self.Foods)

            if self.Ants_alive[i].energy <= 0:
                self.Ants_dead.append(self.Ants_alive[i])
                self.Ants_alive.pop(i)
                break

            self.Ants_alive[i].Update()
        if self.energy <= 0:
            self.Ants_dead.append(x for x in self.Ants_alive)
            self.Ants_alive.clear()
        self.energy -= 5

        for i in range(len(self.Foods)):
            self.Foods[i].Update()
        self.Update()
        self.turns += 1

    def Draw(self, screen):
        self.body = pygame.Rect(self.pos.x, self.pos.y, 40, 40)
        pygame.draw.rect(screen, self.color, self.body)

    def Update(self):
        self.body.update(self.pos.x, self.pos.y, 40, 40)

    def Mutate(self, mutationRate):
        self.brain.mutate(mutationRate)
        for i in self.Ants_alive:
            i.brain = self.brain



