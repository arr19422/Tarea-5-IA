import pygame
import math
from tqdm import tqdm
import numpy as np
from smashing import smashing_food

def show_snake(snake_place, show):
    for place in snake_place:
        pygame.draw.rect(show, (138,43,226), pygame.Rect(place[0], place[1], 10, 10))


def show_food(food_place, show):
    pygame.draw.rect(show, (0,255,255), pygame.Rect(food_place[0], food_place[1], 10, 10))


def starting_places():
    starting_point = [50, 50]
    snake_place = [[50, 50], [60,50]]
    food_place = [180,240]
    result = 1

    return starting_point, snake_place, food_place, result


def food_lenght_from_snake(food_place, snake_place):
    return np.linalg.norm(np.array(food_place) - np.array(snake_place[0]))


def make_snake(starting_point, snake_place, food_place, controller, result):
    if controller == 1:
        starting_point[0] += 10
    elif controller == 0:
        starting_point[0] -= 10
    elif controller == 2:
        starting_point[1] += 10
    else:
        starting_point[1] -= 10

    if starting_point == food_place:
        food_place, result = smashing_food(food_place, result)
        snake_place.insert(0, list(starting_point))

    else:
        snake_place.insert(0, list(starting_point))
        snake_place.pop()

    return snake_place, food_place, result


def play_game(starting_point, snake_place, food_place, controller, result, show, clock):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        show.fill((139,139,131))

        show_food(food_place, show)
        show_snake(snake_place, show)

        snake_place, food_place, result = make_snake(starting_point, snake_place, food_place,
                                                               controller, result)
        pygame.display.set_caption("result: " + str(result*10))
        pygame.display.update()
        clock.tick(50000)

        return snake_place, food_place, result