from game import *
from generate import *
from restringed import restringed_places

def gen_training_data(display, clock):
    train_x = []
    train_y = []
    train_games = 1000
    stepsxround = 2000

    for _ in tqdm(range(train_games)):
        snake_start, snake_place, food_position, score = starting_places()
        prev_food_place = food_lenght_from_snake(food_position, snake_place)

        for _ in range(stepsxround):
            angle, snake_place_vector, food_place_vector_normalized, snake_place_vector_normalized = angle_with_food(
                snake_place, food_position)
            place, controller = gen_random_place(snake_place, angle)
            current_place_vector, front_restricted, left_restricted, right_restricted = restringed_places(
                snake_place)

            place, controller, train_y = gen_train_y(snake_place, angle_with_food,
                                                                                    controller, place,
                                                                                    train_y, front_restricted,
                                                                                    left_restricted, right_restricted)

            if front_restricted == 1 and left_restricted == 1 and right_restricted == 1:
                break

            train_x.append(
                [left_restricted, front_restricted, right_restricted, food_place_vector_normalized[0], \
                 snake_place_vector_normalized[0], food_place_vector_normalized[1], \
                 snake_place_vector_normalized[1]])

            snake_place, food_position, score = play_game(snake_start, snake_place, food_position,
                                                              controller, score, display, clock)

    return train_x, train_y


def gen_train_y(snake_place, angle_with_food, controller, place, train_y,
                             front_restricted, left_restricted, right_restricted):
    if place == -1:
        if left_restricted == 1:
            if front_restricted == 1 and right_restricted == 0:
                place, controller = place_vector(snake_place, angle_with_food, 1)
                train_y.append([0, 0, 1])
            elif front_restricted == 0 and right_restricted == 1:
                place, controller = place_vector(snake_place, angle_with_food, 0)
                train_y.append([0, 1, 0])
            elif front_restricted == 0 and right_restricted == 0:
                place, controller = place_vector(snake_place, angle_with_food, 1)
                train_y.append([0, 0, 1])

        else:
            train_y.append([1, 0, 0])

    elif place == 0:
        if front_restricted == 1:
            if left_restricted == 1 and right_restricted == 0:
                place, controller = place_vector(snake_place, angle_with_food, 1)
                train_y.append([0, 0, 1])
            elif left_restricted == 0 and right_restricted == 1:
                place, controller = place_vector(snake_place, angle_with_food, -1)
                train_y.append([1, 0, 0])
            elif left_restricted == 0 and right_restricted == 0:
                train_y.append([0, 0, 1])
                place, controller = place_vector(snake_place, angle_with_food, 1)
        else:
            train_y.append([0, 1, 0])
    else:
        if right_restricted == 1:
            if left_restricted == 1 and front_restricted == 0:
                place, controller = place_vector(snake_place, angle_with_food, 0)
                train_y.append([0, 1, 0])
            elif left_restricted == 0 and front_restricted == 1:
                place, controller = place_vector(snake_place, angle_with_food, -1)
                train_y.append([1, 0, 0])
            elif left_restricted == 0 and front_restricted == 0:
                place, controller = place_vector(snake_place, angle_with_food, -1)
                train_y.append([1, 0, 0])
        else:
            train_y.append([0, 0, 1])

    return place, controller, train_y