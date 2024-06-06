import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from CTC import CTC

#нужен словарь с параметрами входного изображения

class Model:

    def __init__(self, parameters):
        self.model = None
        self.input = None
        self.output = None

        #img_shape -> (width, height, 1)
        self.shape = parameters['img_shape']

    def load_weights(self, path):
        self.model.load_weights(path)

    def build(self):
        self.model = keras.models.Model(
            inputs=self.input, outputs=self.output)
        self.model.compile(optimizer='adam',
              loss=CTC(),
              metrics=['accuracy'])

    def CNN(self):
    #первый сверточный слой
    self.x = layers.Conv2D(
        32,
        (5, 5),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv1",
    )(self.input)
    self.x = layers.MaxPooling2D((2, 2), name="pool1")(self.x)

    #второй сверточный слой
    self.x = layers.Conv2D(
        64,
        (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv2",
    )(self.x)
    self.x = layers.MaxPooling2D((2, 2), name="pool2")(self.x)

    #третий сверточный слой
    self.x = layers.Conv2D(
        128,
        (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv3",
    )(self.x)
    self.x = layers.MaxPooling2D((2, 2), name="pool3")(self.x)

    #четвертый сверточный слой
    self.x = layers.Conv2D(
        256,
        (2, 2),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv4",
    )(self.x)

    def RNN(self):
        self.x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(self.x)
        self.x = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(self.x)


    new_shape = ((self.shape[0] // 8), (self.shape[1] // 8) * 256)
    self.x = layers.Reshape(target_shape=new_shape, name="reshape")(self.x)
    self.x = layers.Dense(64, activation="relu", name="dense1")(self.x)
    self.x = layers.Dropout(0.2)(self.x)
