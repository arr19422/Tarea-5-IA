import math
import numpy as np

def gen_random_place(snake_place, angle_with_food):
    place = 0
    if angle_with_food > 0:
        place = 1
    elif angle_with_food < 0:
        place = -1
    else:
        place = 0

    return place_vector(snake_place, angle_with_food, place)


def place_vector(snake_place, angle_with_food, place):
    current_vector_place = np.array(snake_place[0]) - np.array(snake_place[1])
    left_place_vector = np.array([current_vector_place[1], -current_vector_place[0]])
    right_place_vector = np.array([-current_vector_place[1], current_vector_place[0]])

    new_place = current_vector_place

    if place == -1:
        new_place = left_place_vector
    if place == 1:
        new_place = right_place_vector

    controller = gen_controller(new_place)

    return place, controller


def gen_controller(new_place):
    controller = 0
    if new_place.tolist() == [10, 0]:
        controller = 1
    elif new_place.tolist() == [-10, 0]:
        controller = 0
    elif new_place.tolist() == [0, 10]:
        controller = 2
    else:
        controller = 3

    return controller


def angle_with_food(snake_place, food_place):
    food_place_vector = np.array(food_place) - np.array(snake_place[0])
    snake_place_vector = np.array(snake_place[0]) - np.array(snake_place[1])

    norm_of_food_place_vector = np.linalg.norm(food_place_vector)
    norm_of_snake_place_vector = np.linalg.norm(snake_place_vector)
    if norm_of_food_place_vector == 0:
        norm_of_food_place_vector = 10
    if norm_of_snake_place_vector == 0:
        norm_of_snake_place_vector = 10

    food_place_vector_normalized = food_place_vector / norm_of_food_place_vector
    snake_place_vector_normalized = snake_place_vector / norm_of_snake_place_vector
    angle = math.atan2(
        food_place_vector_normalized[1] * snake_place_vector_normalized[0] - food_place_vector_normalized[
            0] * snake_place_vector_normalized[1],
        food_place_vector_normalized[1] * snake_place_vector_normalized[1] + food_place_vector_normalized[
            0] * snake_place_vector_normalized[0]) / math.pi
    return angle, snake_place_vector, food_place_vector_normalized, snake_place_vector_normalized