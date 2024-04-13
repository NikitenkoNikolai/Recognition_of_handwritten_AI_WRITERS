from PIL import ImageFilter, Image, ImageEnhance
import os


class ImageCorrector:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    @staticmethod
    def filter_image(img):
        img = img.filter(ImageFilter.BLUR)
        img = img.filter(ImageFilter.SMOOTH)
        img = img.filter(ImageFilter.DETAIL)
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.CONTOUR)
        return img

    @staticmethod
    def create_size(img, width, height):
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        return img

    @staticmethod
    def correct_color(img):
        img = img.convert(mode='L')
        img = ImageEnhance.Contrast(img).enhance(1.5)
        return img

    @staticmethod
    def save_image(img):
        img.save(f'{img}', 'png')

    @staticmethod
    def show_image(img):
        img.show()

    @staticmethod
    def check_the_reality_of_folder(output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    @staticmethod
    def adjust_images_in_folder(file_input_folder, file_output_folder):
        for file_name in os.listdir(file_input_folder):
            if file_name.endswith('.jpg') or file_name.endswith('.png'):
                image_path = os.path.join(file_input_folder, file_name)
                image = Image.open(image_path)
                image = ImageCorrector.correct_color(image)
                output_path = os.path.join(file_output_folder, file_name)
                image.save(output_path)

    @staticmethod
    def looking_for_a_folder_with_imgs(path_input, path_output):
        for file_name in os.listdir(path_input):
            if file_name.endswith('.jpg') or file_name.endswith('.png'):
                ImageCorrector.adjust_images_in_folder(path_input, path_output)
            else:
                file_input_folder = path_input + f'\\{str(file_name)}'
                file_output_folder = path_output + f'\\{str(file_name)}'
                ImageCorrector.check_the_reality_of_folder(file_output_folder)
                ImageCorrector.looking_for_a_folder_with_imgs(file_input_folder, file_output_folder)

    def adjust_dataset(self):
        self.check_the_reality_of_folder(self.output_folder)
        self.looking_for_a_folder_with_imgs(self.input_folder, self.output_folder)


inputer = 'D:\\УЧЕБА_УРФУ\\Программирование_Python\\2_семестр\Проект\\пример_папки_входа'
outputer = 'D:\\УЧЕБА_УРФУ\\Программирование_Python\\2_семестр\\Проект\\Пример_папки_выхода'
ImgCor = ImageCorrector(inputer, outputer).adjust_dataset()
