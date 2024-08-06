# menus.py
# handles the user interaction and menu navigation

from image_editor import ImageEditor

class MainMenu:
    def __init__(self):
        self.editor = None
        self.current_image = None

    def display(self):
        print('Welcome to snekshop v1.1!')
        image_path = self.choose_img()
        if image_path:
            self.editor = ImageEditor(image_path)
            self.current_image = self.editor.image
            self.print_menu()

    def choose_img(self):
        while True:
            try:
                choice = int(input('Please select one of the following images to work with:\n'
                                   '1. German cityscape\n'
                                   '2. Mountain landscape\n'
                                   '3. Portrait of a woman\n'
                                   '4. Animal portrait\n'
                                   '5. The classic ;)\n'
                                   '>>> '))
                if choice in {1, 2, 3, 4, 5}:
                    image_files = {
                        1: "images/city.jpg",
                        2: "images/mountains.jpg",
                        3: "images/portrait.jpg",
                        4: "images/owl.jpg",
                        5: "images/lenna.jpg"
                    }
                    path = image_files[choice]
                    print(f"You've chosen to work with {path}")
                    return path
                else:
                    print('Please enter a valid choice!')
            except ValueError:
                print('Please enter a valid integer for your choice!')

    def print_menu(self):
        while True:
            try:
                choice = int(input('How would you like to change the image?\n'
                                   '1. Edit\n'
                                   '2. Manipulate\n'
                                   '3. Use a filter\n'
                                   '4. Save and/or exit\n'
                                   '>>> '))
                if choice in {1, 2, 3, 4}:
                    if choice == 1:
                        self.edit_menu()
                    elif choice == 2:
                        self.manip_menu()
                    elif choice == 3:
                        self.filter_menu()
                    elif choice == 4:
                        self.editor.save_img(self.current_image)
                        print("Image saved and exiting.")
                        break
                else:
                    print('Please enter a valid choice!')
            except ValueError:
                print('Please enter a valid integer for your choice!')

    def edit_menu(self):
        while True:
            try:
                choice = int(input('How would you like to edit the image?\n'
                                   '1. Resize\n'
                                   '2. Crop\n'
                                   '3. Center crop\n'
                                   '4. Rotate\n'
                                   '5. Flip horizontally\n'
                                   '6. Flip vertically\n'
                                   '7. Go back\n'
                                   '>>> '))
                if choice in {1, 2, 3, 4, 5, 6, 7}:
                    if choice == 1:
                        width = self.get_valid_optional_integer('Please enter the desired width (or leave empty for percentage)>>> ')
                        height = self.get_valid_optional_integer('Please enter the desired height (or leave empty for percentage)>>> ')
                        width_percent = self.get_valid_optional_integer('Please enter the desired width percentage (or leave empty for absolute value)>>> ', 0, 100)
                        height_percent = self.get_valid_optional_integer('Please enter the desired height percentage (or leave empty for absolute value)>>> ', 0, 100)
                        self.current_image = self.editor.resize_img(self.current_image, width=width, height=height, width_percent=width_percent, height_percent=height_percent)
                    elif choice == 2:
                        width = self.get_valid_integer('Please enter the desired width (integer)>>> ')
                        height = self.get_valid_integer('Please enter the desired height (integer)>>> ')
                        left = self.get_valid_integer('Please enter the horizontal starting point for the crop (integer)>>> ')
                        top = self.get_valid_integer('Please enter the vertical starting point for the crop (integer)>>> ')
                        self.current_image = self.editor.crop_img(self.current_image, left=left, top=top, width=width, height=height)
                    elif choice == 3:
                        left, top, right, bottom = self.editor.center_img(self.current_image)
                        self.current_image = self.editor.crop_img(self.current_image, left=left, top=top, right=right, bottom=bottom)
                    elif choice == 4:
                        angle = self.get_valid_integer('Please enter the desired rotation angle (integer)>>> ')
                        self.current_image = self.editor.rotate_img(self.current_image, angle)
                    elif choice == 5:
                        self.current_image = self.editor.flip_horiz_img(self.current_image)
                    elif choice == 6:
                        self.current_image = self.editor.flip_vert_img(self.current_image)
                    elif choice == 7:
                        break
                    self.current_image.show()
                else:
                    print('Please enter a valid choice!')
            except ValueError:
                print('Please enter a valid integer for your choice!')

    def manip_menu(self):
        while True:
            try:
                choice = int(input('How would you like to manipulate the image?\n'
                                   '1. Greyscale\n'
                                   '2. Adjust brightness\n'
                                   '3. Adjust contrast\n'
                                   '4. Blur\n'
                                   '5. Sharpen\n'
                                   '6. Go back\n'
                                   '>>> '))
                if choice in {1, 2, 3, 4, 5, 6}:
                    if choice == 1:
                        self.current_image = self.editor.greyscale_img(self.current_image)
                    elif choice == 2:
                        factor = self.get_valid_float('Please enter the desired brightness factor (0.0-2.0, where 1.0 is original)>>> ')
                        self.current_image = self.editor.brightness_img(self.current_image, factor)
                    elif choice == 3:
                        factor = self.get_valid_float('Please enter the desired contrast factor (0.0-2.0, where 1.0 is original)>>> ')
                        self.current_image = self.editor.contrast_img(self.current_image, factor)
                    elif choice == 4:
                        blur_choice = self.get_valid_integer('Please select which kind of blur you want to use:\n'
                                                             '1. Box blur\n'
                                                             '2. Gaussian blur\n'
                                                             '3. Blur\n'
                                                             '>>> ', choices={1, 2, 3})
                        factor = self.get_valid_integer('Please enter the desired blur factor (positive integer)>>> ')
                        self.current_image = self.editor.blur_img(self.current_image, blur_choice, factor)
                    elif choice == 5:
                        factor = self.get_valid_float('Please enter the desired sharpness factor (1.0 or higher)>>> ')
                        self.current_image = self.editor.sharpen_img(self.current_image, factor)
                    elif choice == 6:
                        break
                    self.current_image.show()
                else:
                    print('Please enter a valid choice!')
            except ValueError:
                print('Please enter a valid integer for your choice!')

    def filter_menu(self):
        while True:
            try:
                choice = int(input('Which filter would you like to use on the image?\n'
                                   '1. Binary\n'
                                   '2. Outlines\n'
                                   '3. Enhanced edges\n'
                                   '4. Go back\n'
                                   '>>> '))
                if choice in {1, 2, 3, 4}:
                    if choice == 1:
                        threshold = self.get_valid_integer('Please select the binary threshold (0-255)>>> ', 0, 255)
                        self.current_image = self.editor.binary_img(self.current_image, threshold)
                    elif choice == 2:
                        threshold = self.get_valid_integer('Please select the outlines threshold (0-255)>>> ', 0, 255)
                        self.current_image = self.editor.outlines_filter(self.current_image, threshold)
                    elif choice == 3:
                        self.current_image = self.editor.edges_img(self.current_image)
                    elif choice == 4:
                        break
                    self.current_image.show()
                else:
                    print('Please enter a valid choice!')
            except ValueError:
                print('Please enter a valid integer for your choice!')

    def get_valid_integer(self, prompt, min_value=None, max_value=None, choices=None):
        while True:
            try:
                value = int(input(prompt))
                if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                    print(f"Please enter a value between {min_value} and {max_value}!")
                elif choices and value not in choices:
                    print(f"Please select a valid choice from {choices}!")
                else:
                    return value
            except ValueError:
                print("Please enter a valid integer!")

    def get_valid_float(self, prompt, min_value=None, max_value=None):
        while True:
            try:
                value = float(input(prompt))
                if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                    print(f"Please enter a value between {min_value} and {max_value}!")
                else:
                    return value
            except ValueError:
                print("Please enter a valid number!")

    def get_valid_optional_integer(self, prompt, min_value=None, max_value=None):
        while True:
            value = input(prompt).strip()
            if not value:
                return None
            try:
                value = int(value)
                if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                    print(f"Please enter a value between {min_value} and {max_value} or leave empty!")
                else:
                    return value
            except ValueError:
                print("Please enter a valid integer or leave empty!")
