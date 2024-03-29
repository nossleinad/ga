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

#  Black and White
white_counter = 0
black_counter = 0
genotypes = ["BB", "Bw", "wB", "ww"]
genotype_to_fenotype = {genotype: v_black if "B" in genotype else v_white for genotype in genotypes}

#  Statistics
generation = 0
white_counter_list = deque(maxlen=200)
black_counter_list = deque(maxlen=200)


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
        m_prob = 0.01
        if m_prob < random.uniform(0, 1):
            genotype = random.choice(self.genotype) + random.choice(other.genotype)
        else:
            genotype = random.choice(genotypes)
        return PepperMoth(genotype)


def make_peppermoths(n, seed=500):
    random.seed(seed)
    return [PepperMoth("ww") for _ in range(n)]


# Other
peppers = make_peppermoths(1000)
r_prob = 0.8
angle = np.pi - (80 * 2 * np.pi / 200)
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


def die(alpha=0.1) -> None:  # Alpha är amplituden för hur mycket d_prob svänger omkring det stabila d_prob = r_prob / (1 + r_prob)
    global white_counter
    global black_counter
    i = 0
    while i < len(peppers):
        pepper = peppers[i]
        d_prob = surplus / (1 + surplus) - alpha + abs(pepper.color[0] / 255 - cos_angle) * 2 * alpha

        if pepper.age >= 1:
            d_prob += 1 - 0.000001 / pepper.age

        if d_prob >= random.uniform(0, 1):
            white_counter -= bool(pepper.color)
            black_counter -= not bool(pepper.color)
            peppers.pop(i)
            continue
        i += 1


black_counter_lists = []
white_counter_lists = []
x = np.arange(1800, 1960)
batch_size = 100

for sim in range(batch_size):
    run = True
    while run:
        #  Plotdata
        white_counter_list.append(white_counter)
        black_counter_list.append(black_counter)
        generation += 1

        #  Background
        cos_angle = math.cos(angle) * 0.5 + 0.5
        background_color = cos_angle * v_white
        angle += 2 * np.pi / 200

        curr_r_prob = min(max(r_prob + (buoyancy - len(peppers)) / (3 * buoyancy), 0.1), 0.95)
        mating_partners(curr_r_prob)
        die()

        if generation >= 160:
            run = False

    black_counter_list = np.array(black_counter_list)
    white_counter_list = np.array(white_counter_list)
    black_counter_lists.append(black_counter_list)
    white_counter_lists.append(white_counter_list)

    #  Black and White
    white_counter = 0
    black_counter = 0

    #  Reset
    peppers = make_peppermoths(1000, sim)
    angle = np.pi - (80 * 2 * np.pi / 200)
    generation = 0
    white_counter_list = deque(maxlen=200)
    black_counter_list = deque(maxlen=200)

#  Plot-part

#  Individual sims
#  Fixing labels
plt.plot(x, black_counter_lists[0], color='b', linewidth=1, alpha=0.15, label='Svart population från en enskild simulering')
plt.plot(x, white_counter_lists[0], color='r', linewidth=1, alpha=0.15, linestyle=(0, (5, 3)), label='Vit population från en enskild simulering')
for indx in range(1, batch_size):
    plt.plot(x, black_counter_lists[indx], color='b', linewidth=1, alpha=0.15)
    plt.plot(x, white_counter_lists[indx], color='r', linewidth=1, alpha=0.15, linestyle=(0, (5, 3)))
#  Averages
avg_black = np.mean(np.array(black_counter_lists), axis=0)
avg_white = np.mean(np.array(white_counter_lists), axis=0)
plt.plot(x, avg_black, color='k', linewidth=2, alpha=1, label='Medelvärde svart population')
plt.plot(x, avg_white, color='k', linewidth=2, alpha=1, linestyle='dashed', label='Medelvärde vit population')

plt.legend(loc='upper right', prop={'size': 16})
plt.ylabel('Populationsstorlek', fontsize=20)
plt.xlabel('År', fontsize=20)
plt.tick_params(labelsize=20)
plt.show()
