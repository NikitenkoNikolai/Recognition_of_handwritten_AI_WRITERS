from keras._tf_keras.keras.preprocessing import image
from keras._tf_keras.keras.applications.vgg16 import VGG16, preprocess_input
import numpy as np
class Vectorization:
    @staticmethod
    def vectorize_image(model,img_path):
        img = image.load_img(img_path, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        features = model.predict(img_array)
        return features.flatten()
model = VGG16(weights='imagenet', include_top=False)
img_path = 'D:\УЧЕБА_УРФУ\Программирование_Python\\2_семестр\Проект\screen1.png'
img_features = Vectorization.vectorize_image(model,img_path)
print(type(img_features))



# from keras._tf_keras.keras.datasets import fashion_mnist
# from keras._tf_keras.keras.models import Sequential
# from keras._tf_keras.keras.layers import Dense
# from keras._tf_keras.keras import utils
#
# (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
#
# x_train = x_train.reshape(60000, 784)
# print(type(x_train[0]))
# x_train /= 255
# y_train = utils.to_categorical(y_train, 10)
#
# model = Sequential()
# model.add(Dense(800, input_dim=784, activation="relu"))
# model.add(Dense(10, input_dim=784, activation="softmax"))
#
# model.compile(loss="cotegorical_crossentropy", optimizer="SGD", metrics=["accuracy"])
# print(model.summary())
