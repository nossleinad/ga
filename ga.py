import math
import random
import statistics
import time
from collections import deque

import pygame
from pygame.math import Vector2
from pygame.math import Vector3

pygame.init()

WINDOW_RESOLUTION = Vector2(1200, 600)
margin = 150  # Avstånd mellan området med moths och window
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

#  Black and White
white_counter = 0
black_counter = 0
genotypes = ["BB", "Bw", "wB", "ww"]
genotype_to_fenotype = {genotype: v_black if "B" in genotype else v_white for genotype in genotypes}

#  Statistics
generation_list = deque(maxlen=200)
generation = 0
white_counter_list = deque(maxlen=200)
black_counter_list = deque(maxlen=200)
average_d_prob = deque(maxlen=200)


class PepperMoth:
    def __init__(self, radius, pos, genotype=random.choice(genotypes)):
        global white_counter
        global black_counter
        self.radius = radius
        self.pos = pos
        self.age = 0
        self.genotype = genotype
        self.color = genotype_to_fenotype[genotype]
        white_counter += bool(self.color)
        black_counter += not bool(self.color)

    def __str__(self):
        return str(self.__dict__)

    def reproduce(self, other):
        # Mutations
        m_prob = 0.005
        if m_prob < random.uniform(0, 1):
            genotype = random.choice(self.genotype) + random.choice(other.genotype)
        else:
            genotype = random.choice(genotypes)
        return PepperMoth(self.radius, Vector2(random.randint(margin, int(WINDOW_RESOLUTION[0] - margin)),
                                               random.randint(margin, int(WINDOW_RESOLUTION[1] - margin))), genotype)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)


def make_peppermoths(n, seed=101):
    random.seed(seed)
    return [PepperMoth(5, Vector2(random.randint(margin, int(WINDOW_RESOLUTION[0] - margin)),
                                  random.randint(margin, int(WINDOW_RESOLUTION[1] - margin))), 'ww') for _ in range(n)]


# Other
peppers = make_peppermoths(999)
r_prob = 0.8
angle = 0
buoyancy = 1000
children = 2
surplus = r_prob * children - 1


def mating_partners(r_prob) -> None:
    peppers_len = len(peppers)
    for i in range(peppers_len):
        pepper = peppers[i]
        pepper.age += 1
        if r_prob >= random.uniform(0, 1):
            try:
                mating_index = random.choice([k for k in range(peppers_len) if k != i and peppers[k].age])
            except IndexError:
                continue
            for j in range(children):
                peppers.append(pepper.reproduce(peppers[mating_index]))



def die(alpha=0.10) -> None:  # Alpha är amplituden för hur mycket d_prob svänger mellan det stabila d_prob = r_prob / (1 + r_prob)
    global white_counter
    global black_counter
    i = 0
    while i < len(peppers):
        pepper = peppers[i]
        d_prob = surplus / (1 + surplus) - alpha + abs(pepper.color[0] / 255 - cos_angle) * 2 * alpha
        average_d_prob.append(d_prob)

        if pepper.age >= 1:
            d_prob += 1 - 0.000001 / pepper.age


        if d_prob >= random.uniform(0, 1):
            white_counter -= bool(pepper.color)
            black_counter -= not bool(pepper.color)
            peppers.pop(i)
            continue
        i += 1


while run:

    # Calculate dt
    time_now = time.time()
    dt = time_now - time_prev
    time_prev = time_now

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f'generation list: {generation_list}')
            print(f'white counter list {white_counter_list}')
            print(f'black counter list {black_counter_list}')
            run = False

        # Resize window event
        if event.type == pygame.VIDEORESIZE:
            display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            WINDOW_RESOLUTION = Vector2(event.w, event.h)

        # Keypresses
        # if event.type == pygame.KEYDOWN:
        # if event.key == pygame.K_1:

    #  Background
    cos_angle = math.cos(angle) * 0.5 + 0.5
    background_color = cos_angle * v_white
    angle += 0.2 * dt
    display.fill(background_color)

    for p in peppers:
        p.draw(display)

    #  Buoyancy
    population = white_counter + black_counter
    population2 = len(peppers)
    curr_r_prob = min(max(r_prob + (buoyancy - len(peppers)) / buoyancy, 0.1), 0.95)
    mating_partners(curr_r_prob)
    die()

    #  Statistics blits
    if len(average_d_prob):
        display.blit(font.render(f'Average d_prob: {statistics.mean(average_d_prob):.2%}', True, v_red), (WINDOW_RESOLUTION[0] - 2 * margin, margin // 3))
    display.blit(font.render(f'Population size: {len(peppers)}', True, v_red), (margin, margin // 3))
    display.blit(font.render(f'White population size: {white_counter}', True, v_red), (margin, margin / 2))
    display.blit(font.render(f'Black population size: {black_counter}', True, v_red), (WINDOW_RESOLUTION[0] - 2 * margin, margin / 2))

    show_fps(dt)
    pygame.display.update()

    #  Plotdata
    generation += 1
    generation_list.append(generation)
    white_counter_list.append(white_counter)
    black_counter_list.append(black_counter)

    #  Frequency
    clock.tick(5)
