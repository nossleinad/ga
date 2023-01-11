import math
import random
from collections import deque

from pygame.math import Vector3

import matplotlib.pyplot as plt
import numpy as np

#  Driver Part

# Colors
v_black = Vector3(0, 0, 0)
v_white = Vector3(255, 255, 255)
v_red = Vector3(255, 0, 0)
v_yellow = Vector3(255, 255, 0)
v_green = Vector3(0, 255, 0)
v_cyan = Vector3(0, 255, 255)
v_blue = Vector3(0, 0, 255)

angle = 0

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
    def __init__(self, genotype=random.choice(genotypes)):
        global white_counter
        global black_counter
        self.genotype = genotype
        self.color = genotype_to_fenotype[genotype]
        self.age = 0
        white_counter += bool(self.color)
        black_counter += not bool(self.color)

    def __str__(self):
        return str(self.__dict__)

    def reproduce(self, other):
        # Mutations
        m_prob = 0.02
        if m_prob < random.uniform(0, 1):
            genotype = random.choice(self.genotype) + random.choice(other.genotype)
        else:
            genotype = random.choice(genotypes)
        return PepperMoth(genotype)


def make_peppermoths(n, seed=96):
    random.seed(seed)
    return [PepperMoth() for _ in range(n)]


peppers = make_peppermoths(999)
r_prob = 0.3


def mating_partners(r_prob) -> None:
    peppers_len = len(peppers)
    for i in range(peppers_len):
        pepper = peppers[i]
        pepper.age += 1
        if r_prob >= random.uniform(0, 1):
            try:
                peppers.append(pepper.reproduce(peppers[random.choice([k for k in range(peppers_len) if k != i and peppers[k].age])]))
            except IndexError:
                continue


def die(alpha=0.05) -> None:  # Alpha är amplituden för hur mycket d_prob svänger mellan det stabila d_prob = r_prob / (1 + r_prob)
    global white_counter
    global black_counter
    i = 0
    while i < len(peppers):
        pepper = peppers[i]
        d_prob = r_prob / (1 + r_prob) - alpha + abs(pepper.color[0] / 255 - cos_angle) * 2 * alpha

        if pepper.age >= 10:
            d_prob = 1

        average_d_prob.append(d_prob)
        if d_prob >= random.uniform(0, 1):
            white_counter -= bool(pepper.color)
            black_counter -= not bool(pepper.color)
            peppers.pop(i)
            continue
        i += 1


black_counter_lists = []
white_counter_lists = []
x = np.arange(0, 200)
batch_size = 100

for _ in range(batch_size):
    run = True
    while run:
        #  Background
        cos_angle = math.cos(angle) * 0.5 + 0.5
        background_color = cos_angle * v_white
        angle += 0.1

        if 1 < len(peppers) < 1000:  # Buoyancy
            mating_partners(r_prob)
        die()

        #  Plotdata
        generation += 1
        generation_list.append(generation)
        white_counter_list.append(white_counter)
        black_counter_list.append(black_counter)

        if generation >= 200:
            run = False

    black_counter_list = np.array(black_counter_list)
    white_counter_list = np.array(white_counter_list) + black_counter_list
    black_counter_lists.append(black_counter_list)
    white_counter_lists.append(white_counter_list)

    #  Black and White
    white_counter = 0
    black_counter = 0

    #  Reset
    peppers = make_peppermoths(100)
    angle = 0

    #  Statistics
    generation_list = deque(maxlen=200)
    generation = 0
    white_counter_list = deque(maxlen=200)
    black_counter_list = deque(maxlen=200)
    average_d_prob = deque(maxlen=200)

#  Plot-part

#  Individual sims
for i in range(batch_size):
    plt.plot(x, black_counter_lists[i], color='k', linewidth=1, alpha=0.8)
    plt.plot(x, white_counter_lists[i], color='k', linewidth=1, alpha=0.8)
#  Averages
avg_black = np.mean(np.array(black_counter_lists), axis=0)
avg_white = np.mean(np.array(white_counter_lists), axis=0)
plt.plot(x, avg_black, color='k', linewidth=2, alpha=1)
plt.plot(x, avg_white, color='k', linewidth=2, alpha=1)

plt.fill_between(x, avg_black, avg_white, color=(0.9, 0.9, 0.9, 1))
plt.fill_between(x, avg_black, color=(0.1, 0.1, 0.1, 0.7))

plt.show()
