import numpy as np
import pandas as pd
from keras.layers import Dense, Input, Dropout
from keras.utils import np_utils
from keras.preprocessing import image as keras_image
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Flatten, BatchNormalization
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json

import scipy
from scipy import misc

import os
from os.path import isfile, join
from os import walk

from sklearn.model_selection import train_test_split

# Le model utilisé par COZMO pour reconnaître les lettres
def generateNetwork(num_classes,IMAGE_WIDTH, IMAGE_HEIGHT):
    model = Sequential()
    model.add(Conv2D(30, kernel_size=(3, 3), activation='relu',input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT,3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
    model.add(Dropout(0.4))
    model.add(Dense(num_classes, activation='softmax'))
    
    return model

# Fonction permettant de récupérer les pré-images et de les organiser proprement
def processData(IMAGE_WIDTH, IMAGE_HEIGHT, batch_size):
    dir_path = "./Images/"
    label_list = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    dirname_list = []
    for (dirpath, dirnames, filenames) in walk(os.path.join(dir_path)):
        dirname_list.extend(dirnames)

    images_labels = {}

    for i in range(0, len(label_list) + 1):
        for(dirpath, dirnames, filenames) in walk(os.path.join(dir_path, dirname_list[i])):
            for files in filenames :
                images_labels[dirpath + "/" + files] = label_list[i - 1]

    images_df = pd.DataFrame(images_labels.items(), columns=['Image', 'Label'])
    train, test = train_test_split(images_df, test_size=0.30)

    train_datagen = ImageDataGenerator(rescale=1./255)
    valid_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_dataframe(
        train, 
        x_col='Image',
        y_col='Label',
        target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
        class_mode='categorical',
        batch_size=batch_size
    )
    valid_generator = valid_datagen.flow_from_dataframe(
        test,
        x_col='Image',
        y_col='Label',
        target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
        class_mode='categorical',
        batch_size=batch_size
    )
    return [train_generator, valid_generator]
    
def learner(model, train_generator, valid_generator, epochs, batch_size):

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Ces trois lignes permettent à Keras de limiter le learning rate si il voit de l'overfit, ou de complètement l'arrêter si c'est vraiment trop.
    earlystop = EarlyStopping(patience=8)
    learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc', patience=2, verbose=1, factor=0.5, min_lr=0.00001)
    callbacks = [earlystop, learning_rate_reduction]

    total_train = train_generator.n
    total_validate = valid_generator.n

    model.fit_generator(
        train_generator, 
        epochs=epochs,
        validation_data=valid_generator,
        validation_steps=total_validate//batch_size,
        steps_per_epoch=total_train//batch_size,
        callbacks=callbacks
    )
 
    # serialize model to JSON
    model_json = model.to_json()
    with open("model_fresh.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model_fresh.h5")
    print("Saved model to disk")

def modelloader():
    json_file = open('model_fresh.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model_fresh.h5")

    return loaded_model



model = generateNetwork(61, 50, 50)
images = processData(50, 50, 20)
learner(model, images[0], images[1], 20, 20)




    