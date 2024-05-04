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
