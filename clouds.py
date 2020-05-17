import pygame
import sys
import random
import math
from opensimplex import OpenSimplex

filters = 4
timer = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("clowd")
surface = pygame.Surface((400, 400), pygame.SRCALPHA)
seed = OpenSimplex(random.randint(1, 100))
for i in range(400):
    for j in range(100):
        density = max(seed.noise2d(x=i/80, y=j/20) * 250*math.sin(math.pi*j/100), 0)
        pygame.draw.rect(surface, (255, 255, 255, density), pygame.Rect(i, j+100, 1, 1))

screen.blit(surface, (0, 0))
frames = 400
while True:
    surface.scroll(dx = -1)
    pygame.draw.rect(surface, (0, 0, 0, 0), pygame.Rect(399, 0, 1, 400))
    for j in range(100):
        density = max(seed.noise2d(x=frames/80, y=j/20) * 250*math.sin(math.pi*j/100), 0)
        pygame.draw.rect(surface, (255, 255, 255, density), pygame.Rect(399, j+100, 1, 1))
    timer.tick(60)
    frames += 1
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()