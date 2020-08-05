import os
import numpy as np
from keras.models import load_model
from keras import Sequential
from keras.callbacks import History
from keras.layers import LSTM, Dense, Dropout
from keras.utils import np_utils
from tqdm import tqdm
from utilities import get_data
history = History()


def get_model(class_labels, input_shape):
    model = Sequential()
    model.add(LSTM(128, input_shape=(input_shape[0], input_shape[1])))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='tanh'))
    model.add(Dense(len(class_labels), activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    return model


def evaluateModel(model, model_path):
    # Train the epochs
    best_acc = 0
    global x_train, y_train, x_test, y_test
    for i in tqdm(range(50)):
        p = np.random.permutation(len(x_train))
        x_train = x_train[p]
        y_train = y_train[p]
        ret = model.fit(x_train, y_train, batch_size=32, epochs=20, callbacks=[history])
        # loss = ret.history['loss']
        acc = ret.history['acc']

        if acc[0] > best_acc:
            best_acc = acc[0]
            model.save_weights(model_path, overwrite=True)
    model.load_weights(model_path)
    print('Accuracy = ', best_acc)
    model.save(model_path, overwrite=True)
    return best_acc


def training(model_path, class_labels):
    # Read data
    global x_train, y_train, x_test, y_test
    x_train, x_test, y_train, y_test = get_data(flatten=False)
    y_train = np_utils.to_categorical(y_train)
    y_test = np_utils.to_categorical(y_test)

    print(x_train[0].shape)
    model = get_model(class_labels, x_train[0].shape)

    accuracy = evaluateModel(model, model_path)

    return accuracy


def training_model(model_path):
    class_labels = [x for x in os.listdir('dataset') if os.path.isdir(os.path.join('dataset', x))]
    return training(model_path, class_labels)


def loading_model(model_path):
    input_shape = [98, 39]
    try:
        dataset_folder = 'dataset'
        class_labels = [x for x in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, x))]

        model = get_model(class_labels, input_shape)
        model.load_weights(model_path)
        return model
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    voice_acc = training_model('models/my_lstm_model.h5')
    print('accuracy: {:.2f}%\n'.format(voice_acc*100))
    # model = loading_model('models/my_lstm_model.h5')
