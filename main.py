from Nest import *
import random
import numpy as np
import math
import pygame
import time

# initialize screen
screen = pygame.display.set_mode((1400, 800))
background = (100, 100, 100)
pygame.font.init()
my_font = pygame.font.SysFont('arial', 30)

# Parameters
Instances = 15
muatationRate = 0.3

# initialize Nests
Nests = []
for i in range(Instances):
    Nests.append(Nest())

DeadNests = []

# Graph data
gen = 0
points = []
points.append((0, 0))

while True:
    screen.fill(background)
    Nest_energy = my_font.render(str(Nests[0].energy), False, (0, 0, 0))
    gen_disp = my_font.render(str(gen), False, (0, 0, 0))
    screen.blit(Nest_energy, (0, 0))
    screen.blit(gen_disp, (0, 40))
    # if gen % 5 == 0:
    for i in range(len(Nests)):
        if i == 1:
            Nests[i].Turn_draw(screen)
        else:
            Nests[i].Turn()  # Nests[i].Turn_draw(screen)
        if len(Nests[i].Ants_alive) == 0:
            DeadNests.append(Nests[i])
            Nests.pop(i)
            break

    if (len(Nests)) == 0:
        gen += 1
        DeadNests.sort(key=lambda x: x.turns)
        scores = [x.turns for x in DeadNests]
        print(scores)
        max_score = max(scores)
        print(max_score)
        min_score = min(scores)
        max_idx = scores.index(max_score)
        points.append((gen * 10, max_score / 10))
        if (len(points) > 100):
            points.pop(0)
            for i in range(len(points)):
                points[i] = (points[i][0] - points[0][0], points[i][1])
        # print(points)
        new_brain = DeadNests[len(DeadNests) - 1].brain
        for i in range(Instances):
            temp_Nest = Nest()
            temp_Nest.brain = new_brain
            temp_Nest.brain.mutate(muatationRate)
            Nests.append(temp_Nest)
        # for i in range(len(Nests)):
        # Nests[i].brain.mutate(muatationRate)
        DeadNests.clear()
    if len(points) >= 2:
        pygame.draw.lines(screen, (0, 0, 0), False, points)

    pygame.display.flip()

# score_lim = random.randint(min_score, max_score)
#           for i in range(len(DeadNests)):
#                if (DeadNests[i].turns >= score_lim):
#                    new_brain = DeadNests[i].brain


'''
    else:
        for i in range(len(Nests)):
            Nests[i].Turn()  # Nests[i].Turn_draw(screen)
            if len(Nests[i].Ants_alive) == 0:
                DeadNests.append(Nests[i])
                Nests.pop(i)
                break
'''
