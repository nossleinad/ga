import math
import random
import statistics
import time
from collections import deque

import pygame
from pygame.math import Vector2
from pygame.math import Vector3

pygame.init()

WINDOW_RESOLUTION = Vector2(1200, 900)
margin = 150  # avstånd mellan området med moths och window
display = pygame.display.set_mode(WINDOW_RESOLUTION, pygame.RESIZABLE)
pygame.display.set_caption(__file__.split("\\")[-1])

run = True
time_prev = time.time()
clock = pygame.time.Clock()

# Colors
v_black = Vector3(0, 0, 0)
v_white = Vector3(255, 255, 255)
v_red = Vector3(255, 0, 0)
v_yellow = Vector3(255, 255, 0)
v_green = Vector3(0, 255, 0)
v_cyan = Vector3(0, 255, 255)
v_blue = Vector3(0, 0, 255)

# Text
pygame.font.init()
font = pygame.font.SysFont('leelawadeeuisemilight', 16)


def show_fps(delta_time, text_color=(0, 255, 0), outline_color=(0, 0, 0)):
    fps_text = font.render(f"FPS: {int(1 / delta_time)}", True, text_color)
    fps_outline = font.render(f"FPS: {int(1 / delta_time)}", True, outline_color)
    display.blit(fps_outline, (-1, -1))
    display.blit(fps_outline, (-1, 1))
    display.blit(fps_outline, (1, -1))
    display.blit(fps_outline, (1, 1))
    display.blit(fps_text, (0, 0))


angle = math.pi / 2

white_counter = 0
black_counter = 0
genotypes = ["BB", "Bw", "wB", "ww"]
genotype_to_fenotype = {genotype: v_black if "B" in genotype else v_white for genotype in genotypes}

average = deque(maxlen=200)


class PepperMoth:
    def __init__(self, radius, pos, genotype=random.choice(genotypes)):
        global white_counter
        global black_counter
        self.radius = radius
        self.pos = pos
        self.genotype = genotype
        self.color = genotype_to_fenotype[genotype]
        white_counter += bool(self.color)
        black_counter += not bool(self.color)

    def __str__(self):
        return str(self.__dict__)

    def reproduce(self, other):
        # mutations
        m_prob = 0.02
        if m_prob < random.uniform(0, 1):
            genotype = random.choice(self.genotype) + random.choice(other.genotype)
        else:
            genotype = random.choice(genotypes)
        return PepperMoth(self.radius, Vector2(random.randint(margin, int(WINDOW_RESOLUTION[0] - margin)),
                                               random.randint(margin, int(WINDOW_RESOLUTION[1] - margin))), genotype)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)


def make_peppermoths(n, seed=100):
    random.seed(seed)
    return [PepperMoth(5, Vector2(random.randint(margin, int(WINDOW_RESOLUTION[0] - margin)),
                                  random.randint(margin, int(WINDOW_RESOLUTION[1] - margin)))) for _ in range(n)]


peppers = make_peppermoths(100)
r_prob = 0.3


def reproduce(r_prob) -> None:
    for i in range(len(peppers)):
        if r_prob >= random.uniform(0, 1):
            peppers.append(peppers[i].reproduce(random.choice(peppers)))


def die(alpha=0.05) -> None:  # alpha är amplituden för hur mycket d_prob svänger mellan det stabila d_prob = r_prob / (1 + r_prob)
    global white_counter
    global black_counter
    i = 0
    while i < len(peppers):
        d_prob = r_prob / (1 + r_prob) - alpha + abs(peppers[i].color[0] / 255 - sin_angle) * 2 * alpha
        average.append(d_prob)
        if d_prob >= random.uniform(0, 1):
            white_counter -= bool(peppers[i].color)
            black_counter -= not bool(peppers[i].color)
            peppers.pop(i)
            continue
        i += 1


# man kan inte ha samma prob för die och reproduce. Med d_prob=r_prob=0.5 får man genomsnittligt en sekvens: * 1.5 / 2 * 1.5 / 2
# alltså minskar i genomsnitt populationen per uppdatering med faktor 3/4. För att inte få en dynamisk population kan man sätta d_prob = r_prob / (1 + r_prob)


while run:

    # Calculate dt
    time_now = time.time()
    dt = time_now - time_prev
    time_prev = time_now

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Resize window event
        if event.type == pygame.VIDEORESIZE:
            display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            WINDOW_RESOLUTION = Vector2(event.w, event.h)

        # Keypresses
        # if event.type == pygame.KEYDOWN:
        # if event.key == pygame.K_1:
    sin_angle = math.sin(angle) * 0.5 + 0.5
    background_color = sin_angle * v_white
    angle += 0.1 * dt
    display.fill(background_color)

    for p in peppers:
        p.draw(display)

    if len(peppers) < 1000:  # bärkraft
        reproduce(r_prob)
    die()

    display.blit(font.render(f'Average d_prob: {statistics.mean(average):.2%}', True, v_red), (600, 40))
    display.blit(font.render(f'Population size: {len(peppers)}', True, v_red), (130, 40))
    display.blit(font.render(f'White population size: {white_counter}', True, v_red), (130, 80))
    display.blit(font.render(f'Black population size: {black_counter}', True, v_red), (600, 80))

    show_fps(dt)
    pygame.display.update()
    clock.tick(10)
