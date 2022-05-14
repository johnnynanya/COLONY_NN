import random
import pygame

vec = pygame.math.Vector2


class Food:
    def __init__(self):
        self.pos = vec(random.randint(0, pygame.display.get_surface().get_size()[0]),
                       random.randint(0, pygame.display.get_surface().get_size()[1]))
        self.body = pygame.Rect(0, 0, 5, 5)
        self.color = (100, 100, 0)
        self.energy = 150

    def Respawn(self):
        self.pos = vec(random.randint(0, pygame.display.get_surface().get_size()[0]),
                       random.randint(0, pygame.display.get_surface().get_size()[1]))

    def Draw(self, screen):
        self.body = pygame.Rect(self.pos.x, self.pos.y, 5, 5)
        pygame.draw.rect(screen, self.color, self.body)

    def Update(self):
        self.body.update(self.pos.x, self.pos.y, 5, 5)
