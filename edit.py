import math

##############################################################################
#                                   Imports                                  #
##############################################################################
from helper import *

##############################################################################
#                                  Sub Functions                             #
##############################################################################

def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    # separates a colored image's channels
    image_lst = []
    for r in range(len(image[0][0])):
        image_rows = []
        for m in range(len(image)):
            image_columns = []
            for n in range(len(image[0])):
                image_columns.append(image[m][n][r])
            image_rows.append(image_columns)
        image_lst.append(image_rows)
    return image_lst


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    # combines a colored image's channels
    colored_image = []
    for r in range(len(channels[0])):
        image_rows = []
        for m in range(len(channels[0][0])):
            image_columns = []
            for n in range(len(channels)):
                image_columns.append(channels[n][r][m])
            image_rows.append(image_columns)
        colored_image.append(image_rows)
    return colored_image


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    # converts colored image to gray scale
    single_img = []
    for i in range(len(colored_image)):
        single_columns = []
        for j in range(len(colored_image[0])):
            cell_sum = 0
            cell_sum += colored_image[i][j][0] * 0.299
            cell_sum += colored_image[i][j][1] * 0.587
            cell_sum += colored_image[i][j][2] * 0.114
            cell_sum = round(cell_sum)
            single_columns.append(cell_sum)
        single_img.append(single_columns)
    return single_img


def blur_kernel(size: int) -> Kernel:
    # creates a kernel by the given size
    table = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(1 / (size ** 2))
        table.append(row)
    return table


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    # applies a kernel on a gray scale image
    new_img = deepcopy(image)
    clac_size = len(kernel) // 2
    for i in range(len(image)):
        for j in range(len(image[0])):
            kernel_sum = 0
            kernel_row = 0
            for m in range(i - clac_size, i + clac_size + 1):
                kernel_column = 0
                for n in range(j - clac_size, j + clac_size + 1):
                    if (0 <= m < len(image)) and (0 <= n < len(image[0])):
                        cell_loc = image[m][n]
                    else:
                        cell_loc = image[i][j]
                    kernel_sum += cell_loc * kernel[kernel_row][kernel_column]
                    kernel_column += 1
                kernel_row += 1
            if kernel_sum > 255:
                kernel_sum = 255
            elif kernel_sum < 0:
                kernel_sum = 0
            else:
                kernel_sum = round(kernel_sum)
            new_img[i][j] = kernel_sum
    return new_img


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    # applies bilinear interpolation on an image
    a = image[int(y)][int(x)]
    b = image[math.ceil(y)][int(x)]
    c = image[int(y)][math.ceil(x)]
    d = image[math.ceil(y)][math.ceil(x)]
    disc_x = x % 1
    disc_y = y % 1
    sum_a = a * (1 - disc_x) * (1 - disc_y)
    sum_b = b * disc_y * (1 - disc_x)
    sum_c = c * disc_x * (1 - disc_y)
    sum_d = d * disc_x * disc_y
    return round(sum_a + sum_b + sum_c + sum_d)


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    # resizes the image by the given measures
    table = []
    for i in range(new_height):
        row = []
        for j in range(new_width):
            if i == 0 and j == 0:
                row.append(image[0][0])
            elif i == 0 and j == new_width - 1:
                row.append(image[0][len(image[0]) - 1])
            elif i == new_height - 1 and j == 0:
                row.append(image[len(image) - 1][0])
            elif i == new_height - 1 and j == new_width - 1:
                row.append(image[len(image) - 1][len(image[0]) - 1])
            else:
                y_loc = (len(image) - 1) * i / (new_height - 1)
                x_loc = (len(image[0]) - 1) * j / (new_width - 1)
                row.append(bilinear_interpolation(image, y_loc, x_loc))
        table.append(row)
    return table


def rotate_90(image: Image, direction: str) -> Image:
    # rotates the image by 90 degrees by a given direction
    table = []
    if direction == "R":
        for i in range(len(image[0])):
            row = []
            for j in range(len(image) - 1, -1, -1):
                row.append(image[j][i])
            table.append(row)
    else:
        for i in range(len(image[0]) - 1, -1, -1):
            row = []
            for j in range(len(image)):
                row.append(image[j][i])
            table.append(row)
    return table


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    # creates and return the edges of an image
    kernel = blur_kernel(blur_size)
    blured_image = apply_kernel(image, kernel)
    avg_kernel = blur_kernel(block_size)
    avg_image = apply_kernel(blured_image, avg_kernel)
    for i in range(len(blured_image)):
        for j in range(len(blured_image[0])):
            if blured_image[i][j] < avg_image[i][j] - c:
                blured_image[i][j] = 0
            else:
                blured_image[i][j] = 255
    return blured_image


def quantize(image: SingleChannelImage, n: int) -> SingleChannelImage:
    # quantize a gray scale image
    q_img = deepcopy(image)
    for i in range(len(image)):
        for j in range(len(image[0])):
            q_img[i][j] = round(math.floor(image[i][j] * (n / 256)) * 255 / (n - 1))
    return q_img


def quantize_colored_image(image: ColoredImage, n: int) -> ColoredImage:
    # quantize a colored image
    sep_img = separate_channels(image)
    for i in range(len(sep_img)):
        sep_img[i] = quantize(sep_img[i], n)
    new_img = combine_channels(sep_img)
    return new_img


def apply_on_colored_image1(image: ColoredImage, function, var=None) -> ColoredImage:
    # applies gray scale images functions on colored images
    sep_img = separate_channels(image)
    for i in range(len(sep_img)):
        sep_img[i] = function(sep_img[i], var)
        image = combine_channels(sep_img)
    return image


def apply_on_colored_image2(image: ColoredImage, function, var1=None, var2=None) -> ColoredImage:
    # applies gray scale images functions on colored images
    sep_img = separate_channels(image)
    for i in range(len(sep_img)):
        sep_img[i] = function(sep_img[i], var1, var2)
        image = combine_channels(sep_img)
    return image


def is_Image_colored(image: Image) -> bool:
    # Checks if an image is colored
    if type(image[0][0]) == list:
        return True
    else:
        return False


def is_pos_int(s):
    # Checks if a string can be cast to a positive integer
    try:
        int(s)
        if int(s) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def is_pos_odd_int(s):
    # Checks if a string can be cast to an odd integer
    try:
        int(s)
        if int(s) > 0 and int(s) % 2 != 0:
            return True
        else:
            return False
    except ValueError:
        return False


def is_bigger_than_1_int(s):
    # Checks if a string can be cast to an integer bigger than 1
    try:
        int(s)
        if int(s) > 1:
            return True
        else:
            return False
    except ValueError:
        return False


def is_not_neg_float(s):
    # Checks if a string can be cast to a non-negative float
    try:
        float(s)
        if float(s) >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


##############################################################################
#                                  Main Functions                            #
##############################################################################

# func 1
def RGB_2_gray(image):
    if is_Image_colored(image):
        image = RGB2grayscale(image)
    else:
        print("The image is already in gray scale")
    return image


# func 2
def blur_img(image):
    kernel_size = input("Please enter the kernel size for blurring: ")
    if is_pos_odd_int(kernel_size):
        kernel_size = int(kernel_size)
        kernel = blur_kernel(kernel_size)
        if is_Image_colored(image):
            image = apply_on_colored_image1(image, apply_kernel, kernel)
        else:
            image = apply_kernel(image, kernel)
    else:
        print("The number isn't round and positive")
    return image


# func 3
def resize_img(image):
    sizes = input("Please enter: wide,length: ")
    if sizes.count(",") == 1:
        sizes = sizes.split(",")
        if is_bigger_than_1_int(sizes[0]) and is_bigger_than_1_int(sizes[1]):
            if is_Image_colored(image):
                apply_on_colored_image2(image, resize, int(sizes[0]), int(sizes[1]))
            else:
                image = resize(image, int(sizes[0]), int(sizes[1]))
        else:
            print("The input isn't valid")
    else:
        print("The input isn't valid")
    return image


# func 4
def rotate_img(image):
    direction = input("Please enter R or L to choose direction: ")
    if direction == "L" or direction == "R":
        image = rotate_90(image, direction)
    else:
        print("The input isn't valid")
    return image


# func 5
def edge_img(image):
    user_input = input("Please enter blur-size,block-size,number: ")
    if user_input.count(",") == 2:
        user_input = user_input.split(",")
        if is_pos_odd_int(user_input[0]) and is_pos_odd_int(user_input[1]) and is_not_neg_float(user_input[2]):
            blur = int(user_input[0])
            block = int(user_input[1])
            number = float(user_input[2])
            if is_Image_colored(image):
                image = RGB2grayscale(image)
            image = get_edges(image, blur, block, number)
        else:
            print("The input isn't valid")
    else:
        print("The input isn't valid")
    return image


# func 6
def quantize_img(image):
    quant_num = input("Please enter the number of shades for quantization: ")
    if is_bigger_than_1_int(quant_num):
        quant_num = int(quant_num)
        if is_Image_colored(image):
            image = quantize_colored_image(image, quant_num)
        else:
            image = quantize(image, quant_num)
    else:
        print("The input isn't valid")
    return image
