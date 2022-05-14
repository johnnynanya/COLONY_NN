import random
import numpy as np
import math
import pygame
from NN import *
from Food import *

vec = pygame.math.Vector2


class Ant:
    def __init__(self, brain):
        self.pos = vec(random.randint(0, pygame.display.get_surface().get_size()[0]),
                       random.randint(0, pygame.display.get_surface().get_size()[1]))
        self.speed = 1
        self.brain = brain
        self.body = pygame.Rect(0, 0, 10, 10)
        self.color_eat = (0, 255, 0)
        self.color_return = (0, 0, 255)
        self.start_energy = 2000
        self.energy = self.start_energy
        self.state = 0
        self.food_to_deposit = 0

    def EatFood(self, Food):

        # move to closest food
        distance = [x.pos - self.pos for x in Food]
        distance = [x.length() for x in distance]
        min_dist = min(distance)
        min_index = distance.index(min_dist)
        direction = Food[min_index].pos - self.pos
        if direction.length() != 0:
            self.pos += (direction).normalize() * self.speed

        # keep on screen
        if self.pos.x > pygame.display.get_surface().get_size()[0]:
            self.pos.x = pygame.display.get_surface().get_size()[0]
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > pygame.display.get_surface().get_size()[1]:
            self.pos.y = pygame.display.get_surface().get_size()[1]
        if self.pos.y < 0:
            self.pos.y = 0

        # eat food
        collided = self.body.collidelist([x.body for x in Food])
        if collided != -1:
            self.energy += Food[collided].energy
            Food[collided].Respawn()
            self.food_to_deposit+=1


    def ReturnFood(self, Nest, Food):
        # move towards nest
        direction = Nest.pos - self.pos
        if direction.length() != 0:
            self.pos += (direction).normalize() * self.speed

        # keep on screen
        if self.pos.x > pygame.display.get_surface().get_size()[0]:
            self.pos.x = pygame.display.get_surface().get_size()[0]
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > pygame.display.get_surface().get_size()[1]:
            self.pos.y = pygame.display.get_surface().get_size()[1]
        if self.pos.y < 0:
            self.pos.y = 0

        # deposit food
        if self.body.colliderect(Nest.body) & self.food_to_deposit>0:
            Nest.energy += 100
            self.food_to_deposit=0

    def Decide(self, Nest):
        distance = Nest.pos-self.pos
        distance = distance.length()
        if self.food_to_deposit > 0:
            input = [self.energy / self.start_energy, Nest.energy / Nest.start_energy,
                     distance/1000, 1]
        else:
            input = [self.energy / self.start_energy, Nest.energy / Nest.start_energy,
                     distance/1000, -1]
        decision = self.brain.output(input)
        if decision[0] > decision[1]:
            self.state = 0
        else:
            self.state = 1

    def Move(self, Nest, Food):
        self.energy -= 1
        if self.state == 0:
            self.EatFood(Food)
        elif self.state == 1:
            self.ReturnFood(Nest, Food)


    def Draw(self,screen):
        self.body = pygame.Rect(self.pos.x,self.pos.y, 10, 10)
        if(self.state == 0):
            pygame.draw.rect(screen, self.color_eat, self.body)
        else:
            pygame.draw.rect(screen, self.color_return, self.body)

    def Update(self):
        self.body.update(self.pos.x,self.pos.y, 10, 10)
