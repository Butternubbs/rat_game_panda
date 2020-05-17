import pygame
import sys
import random
import math
from opensimplex import OpenSimplex

filters = 4
timer = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("mowntan")
surface = pygame.Surface((400, 400), pygame.SRCALPHA)
surface2 = pygame.Surface((400, 400), pygame.SRCALPHA)
seed = OpenSimplex(random.randint(1, 100))
seed2 = OpenSimplex(random.randint(1, 100))
sun = pygame.sprite.Sprite()
sun.image = pygame.image.load("sum.png")

for i in range(400):
    pygame.draw.rect(surface2, (40, 100, 180 + 10*math.sin(i/100)), pygame.Rect(i, 0, 1, 400))
for i in range(400):
    height = seed.noise2d(x=i/100, y=0)
    for f in range(filters):
        fac = math.pow(2, f+1)
        height += seed.noise2d(x=i/(100/fac), y=0)/fac
    height = height * 25 + 150
    pygame.draw.rect(surface, (50, 80 + 10*math.sin(i/100), 30), pygame.Rect(i, 400-height, 1, height))
    height2 = seed2.noise2d(x=i/200, y=0)
    for f in range(filters):
        fac = math.pow(2, f+1)
        height2 += seed2.noise2d(x=i/(200/fac), y=0)/fac
    height2 = height2 * 50 + 200

    pygame.draw.rect(surface2, (40 + 10*math.sin(i/50), 70, 90 + 10*math.sin(i/80)), pygame.Rect(i, 400-height2, 1, height2))
    pygame.draw.rect(surface2, (230,230,255), pygame.Rect(i, 400-height2-math.pow((height2/100), 5), 1, math.pow(height2/100, 5)))
    for j in range(150):
        density = max(seed.noise2d(x=i/80, y=j/8) * 250*math.sin(math.pi*j/150), 0)
        pygame.draw.rect(surface, (255, 255, 255, density), pygame.Rect(i, j, 1, 1))

screen.blit(surface2, (0, 0))
screen.blit(surface, (0, 0))
frames = 400
while True:
    surface.scroll(dx = -1)
    height = seed.noise2d(x=frames/100, y=0)
    for f in range(filters):
        fac = math.pow(2, f+1)
        height += seed.noise2d(x=frames/(100/fac), y=0)/fac
    height = height * 25 + 150
    pygame.draw.rect(surface, (0, 0, 0, 0), pygame.Rect(399, 0, 1, 400))
    pygame.draw.rect(surface, (50, 80 + 10*math.sin((frames)/100), 30), pygame.Rect(399, 400-height, 1, height))
    for j in range(150):
        density = max(seed.noise2d(x=frames/80, y=j/8) * 250*math.sin(math.pi*j/150), 0)
        pygame.draw.rect(surface, (255, 255, 255, density), pygame.Rect(399, j, 1, 1))
    if frames %2 == 0:
        surface2.scroll(dx = -1)
    height2 = seed2.noise2d(x=frames/200, y=0)
    for f in range(filters):
        fac = math.pow(2, f+1)
        height2 += seed2.noise2d(x=frames/(200/fac), y=0)/fac
    height2 = height2 * 50 + 200
    pygame.draw.rect(surface2, (40, 100, 180 + 10*math.sin(frames/100)), pygame.Rect(399, 0, 1, 400))
    pygame.draw.rect(surface2, (40 + 10*math.sin(frames/50), 70, 90 + 10*math.sin(frames/80)), pygame.Rect(399, 400-height2, 1, height2))
    pygame.draw.rect(surface2, (230,230,255), pygame.Rect(399, 400-height2-math.pow((height2/100), 5), 1, math.pow(height2/100, 5)))
    timer.tick(60)
    frames += 1
    screen.blit(surface2, (0, 0))
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