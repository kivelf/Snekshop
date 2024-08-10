# image_editor.py
# handles all image-related operations

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from scipy.ndimage import sobel


class ImageEditor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def save_img(self, image):
        choice = input('Would you like to save the image (Y/N)?>>> ')
        if choice.upper() == 'Y':
            filename = input('What should we save the image as?>>> ')
            new_image_name = str(filename) + ".jpg"
            image.save(new_image_name)
            print('Image successfully saved!')
        elif choice.upper() == 'N':
            print("You've chosen not to save the image.")
        else:
            print('Please enter a valid choice!')

    def get_img_res(self, image):
        return image.size

    def resize_img(self, image, width=None, height=None, width_percent=None, height_percent=None):
        original_width, original_height = image.size

        if width_percent is not None:
            width = int(original_width * (width_percent / 100))
        if height_percent is not None:
            height = int(original_height * (height_percent / 100))

        if width is None and height is None:
            raise ValueError("At least one of width or height must be provided.")

        if width is not None and height is None:
            height = int((width / original_width) * original_height)
        elif height is not None and width is None:
            width = int((height / original_height) * original_width)

        resized = image.resize((width, height))
        return resized

    def crop_img(self, image, left=None, top=None, right=None, bottom=None, width=None, height=None, width_percent=None,
                 height_percent=None):
        original_width, original_height = image.size

        if width_percent is not None:
            width = int(original_width * (width_percent / 100))
        if height_percent is not None:
            height = int(original_height * (height_percent / 100))

        if width is None or height is None:
            raise ValueError("Both width and height must be provided for cropping.")

        if left is None:
            left = (original_width - width) // 2
        if top is None:
            top = (original_height - height) // 2
        if right is None:
            right = left + width
        if bottom is None:
            bottom = top + height

        cropped = image.crop((left, top, right, bottom))
        return cropped

    def center_img(self, image):
        width, height = image.size
        left = width / 4
        top = height / 4
        right = 3 * (width / 4)
        bottom = 3 * (height / 4)
        return (left, top, right, bottom)

    def rotate_img(self, image, angle):
        return image.rotate(angle)

    def greyscale_img(self, image):
        greyscale = image.convert("L")
        return greyscale

    def binary_img(self, image, threshold):
        greyscaled = self.greyscale_img(image)
        gr_arr = np.array(greyscaled)
        for i in range(len(gr_arr)):
            for j in range(len(gr_arr[i])):
                if gr_arr[i][j] >= threshold:
                    gr_arr[i][j] = 255
                else:
                    gr_arr[i][j] = 0
        return Image.fromarray(gr_arr)

    def flip_horiz_img(self, image):
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    def flip_vert_img(self, image):
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    def brightness_img(self, image, factor):
        enhanced_object = ImageEnhance.Brightness(image)
        brightness_enhanced = enhanced_object.enhance(factor)
        return brightness_enhanced

    def contrast_img(self, image, factor):
        enhanced_object = ImageEnhance.Contrast(image)
        contrast_enhanced = enhanced_object.enhance(factor)
        return contrast_enhanced

    def blur_img(self, image, choice, factor):
        if choice == 1:
            return image.filter(ImageFilter.BoxBlur(factor))
        elif choice == 2:
            return image.filter(ImageFilter.GaussianBlur(factor))
        elif choice == 3:
            return image.filter(ImageFilter.BLUR)

    def sharpen_img(self, image, factor):
        enhanced_object = ImageEnhance.Sharpness(image)
        sharper = enhanced_object.enhance(factor)
        return sharper

    def outlines_filter(self, image, threshold):
        edges = image.filter(ImageFilter.FIND_EDGES)
        bands = edges.split()
        outlined = bands[0].point(lambda x: 255 if x < threshold else 0)
        return outlined

    def edges_img(self, image):
        return image.filter(ImageFilter.EDGE_ENHANCE)

    def sobel_filter(self, image):
        # convert to grayscale if the image is not already in grayscale mode since the Sobel operator works on single-channel images
        if image.mode != 'L':
            image = image.convert('L')

        # convert the image to a numpy array
        image_array = np.array(image)

        # apply Sobel filter on both axes
        sobel_x = sobel(image_array, axis=0)
        sobel_y = sobel(image_array, axis=1)

        # combine the Sobel filter results from both axes
        sobel_combined = np.hypot(sobel_x, sobel_y)

        # normalise the result to the 0-255 range and convert it to uint8
        sobel_combined = (sobel_combined / np.max(sobel_combined) * 255).astype(np.uint8)

        # convert the numpy array back to an image
        filtered_image = Image.fromarray(sobel_combined)

        return filtered_image
