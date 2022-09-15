import pygame
import time
import random
import math


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
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_yellow = (255, 255, 0)
color_green = (0, 255, 0)
color_cyan = (0, 255, 255)
color_blue = (0, 0, 255)

# Text
pygame.font.init()
font = pygame.font.SysFont(None, WINDOW_RESOLUTION[0] // 32)


def show_fps(delta_time, text_color=(0, 255, 0), outline_color=(0, 0, 0)):
    fps_text = font.render(f"FPS: {int(1 / delta_time)}", True, text_color)
    fps_outline = font.render(f"FPS: {int(1 / delta_time)}", True, outline_color)
    display.blit(fps_outline, (-1, -1))
    display.blit(fps_outline, (-1, 1))
    display.blit(fps_outline, (1, -1))
    display.blit(fps_outline, (1, 1))
    display.blit(fps_text, (0, 0))


color_list = [color_white, color_white, color_white, color_white, color_white, color_white, color_black]
angle = math.pi


def color_choice(v):
    return color_list[v]


class PepperMoths:
    def __init__(self, radius, pos, color):
        self.radius = radius
        self.pos = pos
        self.color = color_list[random.randint(0, len(color_list) - 1)]


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)


    def color_update(self):
        self.color = color_list[random.randint(0, len(color_list) - 1)]


def make_PepperMoths(n, seed=4):
    random.seed(seed)
    peppers = []
    for i in range(n):
        peppers.append(PepperMoths(20, [random.randint(150, 1050), random.randint(150, 750)], color_list[random.randint(0, len(color_list) - 1)]))
    return peppers


pepper = make_PepperMoths(10)

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

    rgb_value = ((math.sin(angle) + 1) / 2 * 255, (math.sin(angle) + 1) / 2 * 255, (math.sin(angle) + 1) / 2 * 255)
    angle += 0.1 * dt
    display.fill(rgb_value)


    for p in pepper:
        p.color_update()
        p.draw(display)

    # manipulate probability list depending on the color of the background

    show_fps(dt)
    pygame.display.update()
    clock.tick(5)
