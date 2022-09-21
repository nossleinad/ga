import pygame
import time
import random
from pygame.math import Vector3
from pygame.math import Vector2
import math
import statistics

pygame.init()

WINDOW_RESOLUTION = (1200, 900)
image_resolution = [1200, 900]
transform_resolution = (WINDOW_RESOLUTION[0] / image_resolution[0], WINDOW_RESOLUTION[1] / image_resolution[1])
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
font = pygame.font.SysFont('leelawadeeuisemilight', WINDOW_RESOLUTION[0] // 32)


def show_fps(delta_time, text_color=(0, 255, 0), outline_color=(0, 0, 0)):
    fps_text = font.render(f"FPS: {int(1 / delta_time)}", True, text_color)
    fps_outline = font.render(f"FPS: {int(1 / delta_time)}", True, outline_color)
    display.blit(fps_outline, (-1, -1))
    display.blit(fps_outline, (-1, 1))
    display.blit(fps_outline, (1, -1))
    display.blit(fps_outline, (1, 1))
    display.blit(fps_text, (0, 0))


angle = math.pi

threshold_min = 0.02
threshold_max = 0.98

reproduce_counter = 0
death_counter = 0
average = []

class PepperMoths:
    def __init__(self, radius, pos, color=None):
        self.radius = radius
        self.pos = pos
        self.color = random.choice((v_white, v_black))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)



def make_peppermoths(n, seed=112):
    random.seed(seed)
    return [PepperMoths(10, [random.randint(150, 1050), random.randint(150, 750)]) for _ in range(n)]


peppers = make_peppermoths(100)


def reproduce(r_prob: float = 0.05) -> None:
    global peppers
    global reproduce_counter
    for i in range(len(peppers)):
        x = random.uniform(0, 1)
        if r_prob >= x:
            peppers.insert(i, PepperMoths(peppers[i].radius, [random.randint(150, 1050), random.randint(150, 750)], peppers[i].color))
            reproduce_counter += 1


def die():
    global peppers
    global death_counter
    global average
    i = 0
    while i < len(peppers):
        d_prob = 0.028 + abs(peppers[i].color[0] / 255 - sin_angle) / 20
        average.append(d_prob)
        if d_prob >= random.uniform(0, 1):
            peppers.pop(i)
            death_counter += 1
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
            run = False

        # Resize window event
        if event.type == pygame.VIDEORESIZE:
            display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Keypresses
        # if event.type == pygame.KEYDOWN:
        # if event.key == pygame.K_1:
    sin_angle = math.sin(angle) * 0.5 + 0.5
    background_color = sin_angle * v_white
    angle += 0.1 * dt
    display.fill(background_color)

    for p in peppers:
        p.draw(display)

    reproduce()
    die()
    display.blit(font.render(f'Reproduce counter: {reproduce_counter}', True, v_red), (130, 0))
    display.blit(font.render(f'Death counter: {death_counter}', True, v_red), (600, 0))
    display.blit(font.render(f'Average d_prob: {statistics.mean(average):.2%}', True, v_red), (600, 40))
    display.blit(font.render(f'Population size: {len(peppers)}', True, v_red), (130, 40))
    show_fps(dt)
    pygame.display.update()
    clock.tick(60)
