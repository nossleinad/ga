import pygame
import time
import random
import math
import statistics
from pygame.math import Vector3
from pygame.math import Vector2
from collections import deque

pygame.init()

WINDOW_RESOLUTION = Vector2(1200, 900)
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

reproduce_counter = 0
death_counter = 0
white_counter = 0
black_counter = 0

average = deque(maxlen=200)


class PepperMoth:
    def __init__(self, radius, pos, color=None):
        global white_counter
        global black_counter
        self.radius = radius
        self.pos = pos
        self.color = color if color is not None else random.choice((v_white, v_black))
        white_counter += bool(self.color)
        black_counter += not bool(self.color)

    def __str__(self):
        return str(self.__dict__)

    def reproduce(self):
        m_prob = 0.02
        if m_prob < random.uniform(0, 1):
            color = self.color
        else:
            color = Vector3(255, 255, 255) - self.color
        return PepperMoth(self.radius, [random.randint(150, WINDOW_RESOLUTION[0] - 150),
                                        random.randint(150, WINDOW_RESOLUTION[1] - 150)], color)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)


def make_peppermoths(n, seed=1000):
    random.seed(seed)
    return [PepperMoth(3, [random.randint(150, WINDOW_RESOLUTION[0] - 150),
                           random.randint(150, WINDOW_RESOLUTION[1] - 150)]) for _ in range(n)]


peppers = make_peppermoths(100)


def reproduce(r_prob: float = 0.3) -> None:
    global peppers
    global reproduce_counter
    for i in range(len(peppers)):
        if r_prob >= random.uniform(0, 1):
            peppers.append(peppers[i].reproduce())
            reproduce_counter += 1


def die(alpha=0.05):  # alpha är amplituden för hur mycket d_prob svänger mellan det stabila d_prob = r_prob / (1 + r_prob)
    global peppers
    global death_counter
    global average
    global white_counter
    global black_counter
    i = 0
    while i < len(peppers):
        d_prob = 0.3 / 1.3 - alpha + abs(peppers[i].color[0] / 255 - sin_angle) * 2 * alpha
        average.append(d_prob)
        if d_prob >= random.uniform(0, 1):
            white_counter -= bool(peppers[i].color)
            black_counter -= not bool(peppers[i].color)
            peppers.pop(i)
            death_counter += 1
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
        reproduce()
    die()

    display.blit(font.render(f'Reproduce counter: {reproduce_counter}', True, v_red), (130, 0))
    display.blit(font.render(f'Death counter: {death_counter}', True, v_red), (600, 0))
    display.blit(font.render(f'Average d_prob: {statistics.mean(average):.2%}', True, v_red), (600, 40))
    display.blit(font.render(f'Population size: {len(peppers)}', True, v_red), (130, 40))
    display.blit(font.render(f'White population size: {white_counter}', True, v_red), (130, 80))
    display.blit(font.render(f'Black population size: {black_counter}', True, v_red), (600, 80))

    show_fps(dt)
    pygame.display.update()
    clock.tick(10)
