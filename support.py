from csv import reader
import pygame
from os import walk


def csv_load(path):
    terrain = []
    with open(path) as map:
        layout = reader(map, delimiter=',')
        for line in layout:
            terrain.append(list(line))
    return terrain


def load_folder(path):
    surfaces = []
    for _, _, files in walk(path):
        for image in files:
            full_path = path + '/' + image
            surface = pygame.image.load(full_path).convert_alpha()
            surfaces.append(surface)

    return surfaces
