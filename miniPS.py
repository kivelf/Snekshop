import PIL          # Python Imaging Library - adds image processing capabilities
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np  # NumPy - mathematical and logical operations on large multi-dimensional arrays and matrices


def main():
    print('Welcome to snekshop v0.1!')
    image_path = choose_img()       # brugeren vælger et billede at redigere, som definerer vores image path
    image = read_img(image_path)
    print_menu(image)               # brugeren vaelger hvad der skal goeres med billedet


def read_img(path):        # definerer en funktion der laeser et billede som PIL objekt
    try:
        image = PIL.Image.open(path)  # Pillow stores the image in RAM as a PIL object
        return image
    except Exception as err:
        print(err)


def save_img(image):
    choice = input('Would you like to save the image (Y/N)?>>> ')
    if choice.upper() == 'Y':
        filename = input('What should we save the image as?>>> ')
        new_image_name = str(filename)+".jpg"
        image.save(new_image_name)
        print('Image successfully saved!')
    elif choice.upper() == 'N':
        print("You've chosen not to save the image.")
    else:
        print('Please enter a valid choice!')


def get_img_res(image):     # en funktion som returnerer vores billedes stoerrelse som tuple
    return image.size


def resize_img(image, height, width):       # en funktion der aendrer billedets stroerrelse
    resized = image.resize((height, width))
    return resized


def crop_img(image, left, top, right, bottom):  # en funktion der skaerer billedet
    cropped = image.crop((left, top, right, bottom))    # koordinater i px
    return cropped


def center_img(image):              # laver et 'center crop' hvor vi faar 50% af billedets højde og bredde
    width, height = image.size      # gemmer de to tal som tuple
    left = width/4
    top = width/4
    right = 3 * (width/4)
    bottom = 3 * (width/4)
    return ((left, top, right, bottom))     # returnerer de 4 tal som tuple


def rotate_img(image, angle):       # en funktion som roterer vores billede
    return image.rotate(angle)      # OBS!! Rotates counter-clockwise!


def greyscale_img(image):
    greyscale = image.convert("L")
    return greyscale


def binary_img(image, threshold):
    greyscaled = greyscale_img(image)       # first we need to convert the image to greyscale
    gr_arr = np.array(greyscaled)           # and then use the array from the greyscaled image
    for i in range (0, len(gr_arr)):        # a loop that goes through all the pixels in the image
        for j in range (0, len(gr_arr[i])): # second loop to make this work...
            if gr_arr[i][j] >= threshold:   # if the pxl is above the threshold value
                gr_arr[i][j] = 255          # then turn it to while
            else:
                gr_arr[i][j] = 0            # else turn the plx to black
    return PIL.Image.fromarray(gr_arr)


def flip_horiz_img(image):          # vender vores billede vandret - altså fra venstre til højre
    flipped_hz = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return flipped_hz


def flip_vert_img(image):           # vender vores billede vandret - altså fra top til bund
    flipped_vert = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return flipped_vert


def brightness_img(image, factor):    # 0.0 giver et sort billede, 1.0 er det originale billede
    enhanced_object = ImageEnhance.Brightness(image)
    brightness_enhanced = enhanced_object.enhance(factor)
    return brightness_enhanced


def contrast_img(image, factor):    # 0.0 giver 0 kontrast (gråt billede), 1.0 er det originale billede
    enhanced_object = ImageEnhance.Contrast(image)
    contrast_enhanced = enhanced_object.enhance(factor)
    return contrast_enhanced


def blur_img(image, choice, factor):
    if choice == 1:
        blurred = image.filter(ImageFilter.BoxBlur(factor))
    elif choice == 2:
        blurred = image.filter(ImageFilter.GaussianBlur(factor))
    elif choice == 3:
        blurred = image.filter(ImageFilter.BLUR)
    return blurred


def sharpen_img(image, factor):    # 1.0 er det originale billede, factor >= 1.0
    enhanced_object = ImageEnhance.Sharpness(image)
    sharper = enhanced_object.enhance(factor)
    return sharper


def outlines_filter(image, threshold):
    edges = image.filter(ImageFilter.FIND_EDGES)
    bands = edges.split()       # splits the image into its color bands
    outlined = bands[0].point(lambda x: 255 if x < threshold else 0)    # lambda function call for max-black or max-white
    return outlined


def edges_img(image):           # edge enhancement filter
    enhanced_edges = image.filter(ImageFilter.EDGE_ENHANCE)
    return enhanced_edges


def choose_img():
    choice = int(input('Please select one of the following images to work with:\n'
                       '1. German cityscape\n'
                       '2. Mountain landscape\n'
                       '3. Portrait of a woman\n'
                       '4. Animal portrait\n'
                       '5. The classic ;)\n'
                       '>>> '))
    if choice == 1:
        path = "city.jpg"
        print("You've chosen to work with city.jpg")
    elif choice == 2:
        path = "mountains.jpg"
        print("You've chosen to work with mountains.jpg")
    elif choice == 3:
        path = "portrait.jpg"
        print("You've chosen to work with portrait.jpg")
    elif choice == 4:
        path = "owl.jpg"
        print("You've chosen to work with owl.jpg")
    elif choice == 5:
        path = "lenna.jpg"
        print("You've chosen to work with lenna.jpg")
    else:
        print('Please enter a valid choice!')
    return path


def print_menu(imagepath):
    image = imagepath
    choice = int(input('How would you like to change the image?\n'
          '1. Edit\n'
          '2. Manipulate\n'
          '3. Use a filter\n'
          '>>> '))
    if choice == 1:
        print('Here are your edit options:')
        edit_menu(image)
    elif choice == 2:
        print('Here are your manipulation options:')
        manip_menu(image)
    elif choice == 3:
        print('Here are your filter options:')
        filter_menu(image)
    else:
        print('Please enter a valid choice!')


def edit_menu(image_path):
    image = image_path
    choice = int(input('How would you like to edit the image?\n'
                       '1. Resize\n'
                       '2. Crop\n'
                       '3. Center crop\n'
                       '4. Rotate\n'
                       '5. Flip horizontally\n'
                       '6. Flip vertically\n'
                       '7. Go back\n'
                       '>>> '))
    if choice == 1:
        height = int(input('Please enter the desired height>>> '))
        width = int(input('Please enter the desired width>>> '))
        resized_image = resize_img(image, height, width)
        resized_image.show()
        save_img(resized_image)
    elif choice == 2:
        x1 = int(input('Please enter the beginning of the crop on the horizontal axis>>> '))
        x2 = int(input('Please enter the end of the crop on the horizontal axis>>> '))
        y1 = int(input('Please enter the beginning of the crop on the vertical axis>>> '))
        y2 = int(input('Please enter the end of the crop on the vertical axis>>> '))
        cropped = crop_img(image, x1, y1, x2, y2)
        cropped.show()
        save_img(cropped)
    elif choice == 3:
        center = center_img(image)          # faar koordinaterne til vores center crop
        left, top, right, bottom = center   # unpacks the tuple
        center_cropped = crop_img(image, left, top, right, bottom)
        center_cropped.show()
        save_img(center_cropped)
    elif choice == 4:
        angle = int(input('Please enter the desired rotation angle>>> '))   # OBS!! Roterer MOD uret!
        rotated = rotate_img(image, angle)
        rotated.show()
        save_img(rotated)
    elif choice == 5:
        horizontally_flipped_image = flip_horiz_img(image)
        horizontally_flipped_image.show()
        save_img(horizontally_flipped_image)
    elif choice == 6:
        vertically_flipped_image = flip_vert_img(image)
        vertically_flipped_image.show()
        save_img(vertically_flipped_image)
    elif choice == 7:
        print_menu(image)
    else:
        print('Please enter a valid choice!\n')


def manip_menu(image_path):
    image = image_path
    choice = int(input('How would you like to manipulate the image?\n'
                       '1. Greyscale\n'
                       '2. Adjust brightness\n'
                       '3. Adjust contrast\n'
                       '4. Blur\n'
                       '5. Sharpen\n'
                       '6. Go back\n'
                       '>>> '))
    if choice == 1:
        greyscaled = greyscale_img(image)
        greyscaled.show()
        save_img(greyscaled)
    elif choice == 2:
        brightness_factor = float(input('Please enter the desired brightness factor>>> '))   # 0.0 giver et sort billede, 1.0 er det originale billede
        brightness_adjusted_image = brightness_img(image, brightness_factor)
        brightness_adjusted_image.show()
        save_img(brightness_adjusted_image)
    elif choice == 3:
        contrast_factor = float(input('Please enter the desired contrast factor>>> '))       # 0.0 giver 0 kontrast (gråt billede), 1.0 er det originale billede
        contrast_adjusted_image = contrast_img(image, contrast_factor)
        contrast_adjusted_image.show()
        save_img(contrast_adjusted_image)
    elif choice == 4:
        blur_choice = int(input('Please select which kind of blur you want to use\n'
                                '1. Box blur\n'
                                '2. Gaussian blur\n'
                                '3. Blur\n'
                                '>>> '))
        blur_factor = int(input('Please enter the desired blur factor>>> '))
        blurred_image = blur_img(image, blur_choice, blur_factor)
        blurred_image.show()
        save_img(blurred_image)
    elif choice == 5:
        sharpness_factor = float(input('Please enter the desired sharpness factor>>> '))      # som float-tal
        sharpened_image = sharpen_img(image, sharpness_factor)    # sharpen_factor er en float-variable
        sharpened_image.show()
        save_img(sharpened_image)
    elif choice == 6:
        print_menu(image)
    else:
        print('Please enter a valid choice!\n')


def filter_menu(image_path):
    image = image_path
    choice = int(input('Which filter would you like to use on the image?\n'
                       '1. Binary\n'
                       '2. Outlines\n'
                       '3. Enhanced edges\n'
                       '4. Go back\n'
                       '>>> '))
    if choice == 1:
        threshold_binary = int(input('Please select the threshold>>> '))      # som int, 100 er en god start
        binary_image = binary_img(image, threshold_binary)
        binary_image.show()
        save_img(binary_image)
    elif choice == 2:
        threshold_outlines = int(input('Please select the threshold>>> '))      # som int, 100 er en god start
        outlines_only = outlines_filter(image, threshold_outlines)
        outlines_only.show()
        save_img(outlines_only)
    elif choice == 3:
        edge_enhanced_image = edges_img(image)
        edge_enhanced_image.show()
        save_img(edge_enhanced_image)
    elif choice == 4:
        print_menu(image)
    else:
        print('Please enter a valid choice!\n')


if __name__ == "__main__":
    main()