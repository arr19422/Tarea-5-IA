import random

def smashing_food(food_place, result):
    food_place = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    result += 1
    return food_place, result


def smashing_border(starting_point):
    if starting_point[0] >= 500 or starting_point[0] < 0 or starting_point[1] >= 500 or starting_point[1] < 0:
        return 1
    else:
        return 0


def smashing_self(starting_point, snake_place):
    if starting_point in snake_place[1:]:
        return 1
    else:
        return 0