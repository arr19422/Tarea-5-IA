import tensorflow as tf
from keras.backend import set_session
from restringed import restringed_places
from smashing import smashing_border, smashing_self
from generate import angle_with_food, gen_controller
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True  
config.log_device_placement = True  
                                    
sess = tf.compat.v1.Session(config=config)
set_session(sess) 

from game import *
from keras.models import model_from_json

def run_game_with_ML(model, show, timer):
    max_result = 3
    avg_result = 0
    test_games = 5
    steps_per_game = 2000

    for _ in range(test_games):
        snake_start, snake_place, food_place, result = starting_places()

        count_same_place = 0
        prev_place = 0

        for _ in range(steps_per_game):
            current_place_vector, front_restringed, left_restringed, right_restringed = restringed_places(
                snake_place)
            angle, snake_place_vector, food_place_vector_normalized, snake_place_vector_normalized = angle_with_food(
                snake_place, food_place)
            predictions = []

            predicted_place = np.argmax(np.array(model.predict(np.array([left_restringed, front_restringed, \
                                                                             right_restringed,
                                                                             food_place_vector_normalized[0], \
                                                                             snake_place_vector_normalized[0],
                                                                             food_place_vector_normalized[1], \
                                                                             snake_place_vector_normalized[
                                                                                 1]]).reshape(-1, 7)))) - 1

            if predicted_place == prev_place:
                count_same_place += 1
            else:
                count_same_place = 0
                prev_place = predicted_place

            new_place = np.array(snake_place[0]) - np.array(snake_place[1])
            if predicted_place == -1:
                new_place = np.array([new_place[1], -new_place[0]])
            if predicted_place == 1:
                new_place = np.array([-new_place[1], new_place[0]])

            controller = gen_controller(new_place)

            next_step = snake_place[0] + current_place_vector
            if smashing_border(snake_place[0]) == 1 or smashing_self(next_step.tolist(),
                                                                                        snake_place) == 1:
                break
            snake_place, food_place, result = play_game(snake_start, snake_place, food_place,
                                                              controller, result, show, timer)

            if result > max_result:
                max_result = result

        avg_result += result

    return max_result, avg_result / 5


json_file = open('model.json', 'r')
loaded_json_model = json_file.read()
model = model_from_json(loaded_json_model)
model.load_weights('model.h5')


show_w = 500
show_h = 500
pygame.init()
show=pygame.display.set_mode((show_w,show_h))
timer=pygame.time.Clock()
max_result, avg_result = run_game_with_ML(model,show,timer)
print("Maximum result achieved is:  ", max_result)
print("Average result achieved is:  ", avg_result)