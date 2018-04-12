# import re
import os

import numpy
import pandas
import tensorflow as tf
import keras
import numpy as np

import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation, ConvLSTM2D
from keras.optimizers import SGD

# input data
memberListDir = "data/MemberList/"
securityDir = "data/FieldData/"




# Input dimension
GRID_NUM = 50
STEP_NUM = 8
#
# # x = tf.placeholder("float", [None, STEP_NUM, GRID_NUM, GRID_NUM])
# # y = tf.placeholder("float", [None, GRID_NUM, GRID_NUM])
#
# x_train = np.random.random((100, STEP_NUM, GRID_NUM, GRID_NUM, 1))
# y_train = np.random.random((100, GRID_NUM, GRID_NUM, 1))
#
# x_test = np.random.random((10, STEP_NUM, GRID_NUM, GRID_NUM, 1))
# y_test = np.random.random((10, GRID_NUM, GRID_NUM, 1))


model = Sequential()
model.add(ConvLSTM2D(32, kernel_size=(2,2), return_sequences=True, padding='same',
               input_shape=(STEP_NUM, GRID_NUM, GRID_NUM, 1)))  # returns a sequence of vectors of dimension 32
model.add(ConvLSTM2D(64, kernel_size=(2,2), padding='same', return_sequences=True))  # returns a sequence of vectors of dimension 32
model.add(ConvLSTM2D(128, kernel_size=(2,2), padding='same'))  # returns a sequence of vectors of dimension 32
# model.add(LSTM(32))  # return a single vector of dimension 32
model.add(Dense(1, activation='linear'))

# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
              optimizer='adam')

model.fit(x_train, y_train,
          epochs=20,
          batch_size=16)
score = model.evaluate(x_test, y_test, batch_size=64)