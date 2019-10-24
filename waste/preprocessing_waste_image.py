from keras.models import Sequential
from keras.layers import Convolution2D, MaxPool2D
from keras.layers import Activation, Dropout, Flatten, Dense

root_dir = "./waste_image/"
categories = ['bed', 'chair', 'computer', 'dresser', 'refrigerator', 'sofa', 'stove', 'table', 'tv', 'wordrobe']
nb_classes = len(categories)
image_size = 50


def build_model(in_shape):
    model = Sequential()
    print('in_shape:', in_shape)
    model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(Activation('relu'))

    model.add(Convolution2D(64, 3, 3))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    return model
