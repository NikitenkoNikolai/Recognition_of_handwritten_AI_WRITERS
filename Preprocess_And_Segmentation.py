import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


class ImagePreprocessor:

    @staticmethod
    def preprocess_image(image_path):
        image = Image.open(image_path)
        image = image.resize((1500, 1500))
        image = image.filter(ImageFilter.MedianFilter())
        image = image.convert('L')
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        image = image.filter(ImageFilter.SMOOTH)
        #фикс
        image_rgb = image.convert('RGB')
        original_image = np.array(image_rgb)
    
        threshold = 150
        image = image.point(lambda p: p > threshold and 255)
        return original_image, image


class TextSegmenter:

    @staticmethod
    def text_segmentation(original_image, image):
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)

        _, thresh = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)
        kernel_for_erode = np.ones((3, 3), np.uint8)
        image = cv2.erode(thresh, kernel_for_erode, iterations=1)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

        contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        letters = []
        out_size = 28
        for idx, contour in enumerate(contours):
            if idx == 0: continue

            (x, y, w, h) = cv2.boundingRect(contour)
            if hierarchy[0][idx][3] == 0:
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (70, 0, 0), 2)
                letter = original_image[y: y + h, x: x + w]
                letters.append((x, w, cv2.resize(letter, (out_size, out_size), interpolation=cv2.INTER_AREA)))

        letters.sort(key=lambda x: x[0], reverse=False)
        return letters



image_path = 'poezd.jpg'

original_image, preprocessed_image = ImagePreprocessor.preprocess_image(image_path)
letters = TextSegmenter.text_segmentation(original_image, preprocessed_image)

for idx, let in enumerate(letters):
    cv2.imwrite(f'{idx}.jpg', let[2])
