import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from CTC import CTC


class Model:

    def __init__(self):
        self.model = None
        self.input = None
        self.output = None

    def build(self):
        self.model = keras.models.Model(
            inputs=self.input, outputs=self.output)
        self.model.compile(optimizer='adam',
              loss=CTC(),
              metrics=['accuracy'])