from game import *
from training_data import gen_training_data
from keras.models import Sequential
from keras.layers import Dense

show_w = 500
show_h = 500

pygame.init()
show=pygame.display.set_mode((show_w,show_h))
timer=pygame.time.Clock()

train_x, train_y = gen_training_data(show,timer)


model = Sequential()
model.add(Dense(units=9,input_dim=7))

model.add(Dense(units=15, activation='relu'))
model.add(Dense(3,  activation = 'softmax'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit((np.array(train_x).reshape(-1,7)),( np.array(train_y).reshape(-1,3)), batch_size = 256,epochs= 3)

model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)
model.save_weights('model.h5')