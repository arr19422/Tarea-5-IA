import numpy as np
from smashing import smashing_border, smashing_self


def restringed_places(snake_place):
    current_vector_place = np.array(snake_place[0]) - np.array(snake_place[1])

    left_place_vector = np.array([current_vector_place[1], -current_vector_place[0]])
    right_place_vector = np.array([-current_vector_place[1], current_vector_place[0]])

    front_restringed = restringed_place(snake_place, current_vector_place)
    left_restringed = restringed_place(snake_place, left_place_vector)
    right_restringed = restringed_place(snake_place, right_place_vector)

    return current_vector_place, front_restringed, left_restringed, right_restringed


def restringed_place(snake_place, current_vector_place):
    next_step = snake_place[0] + current_vector_place
    starting_point = snake_place[0]
    if smashing_border(next_step) == 1 or smashing_self(next_step.tolist(), snake_place) == 1:
        return 1
    else:
        return 0