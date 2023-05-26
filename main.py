##############################################################################
#                                   Imports                                  #
##############################################################################
from edit import *
from create import create_json
from convert import convert_json_2_png

##############################################################################
#                                 CONSTANTS                                  #
##############################################################################
OPTION_1 = "1"
OPTION_2 = "2"
OPTION_3 = "3"
OPTION_4 = "4"
OPTION_5 = "5"
OPTION_6 = "6"
OPTION_7 = "7"
OPTION_8 = "8"
OPTION_9 = "9"

if __name__ == '__main__':
    input_val = False
    while not input_val:
        try:
            intro_question = input("Enter 1 for generating an image by Ai or Enter 2 to write an image path: ")
            if intro_question == "2":
                img_name = input("please enter the image path: ")
                try:
                    image = load_image(img_name)
                except Exception as e:
                    print("Error loading image: ", str(e))
                    continue
                input_val = True
            elif intro_question == "1":
                prompt = input("please describe the picture you would want: ")
                json_name = create_json(prompt)
                image_name = convert_json_2_png(json_name)  # list of images
                try:
                    image = load_image(image_name[0])
                except Exception as e:
                    print("Error loading image: ", str(e))
                    continue
                input_val = True
            else:
                print("Invalid input, only '1' and '2' are allowed")
        except Exception as e:
            print(str(e))

    option = None
    while option != OPTION_8:
        try:
            option = input(("please choose one of the following options by typing it's number:\n"
                            "1. Convert RGB Image to gray scale\n"
                            "2. Blur the image\n"
                            "3. Change the image size\n"
                            "4. Rotate the image by 90 degrees\n"
                            "5. Make edges for the image\n"
                            "6. Quantize the image\n"
                            "7. Show the image\n"
                            "8. Exit the program\n"
                            "Your answer: "))
            if option not in (OPTION_1, OPTION_2, OPTION_3, OPTION_4, OPTION_5, OPTION_6, OPTION_7, OPTION_8):
                raise Exception("Invalid option selected")
            if option == OPTION_1:
                image = RGB_2_gray(image)
            elif option == OPTION_2:
                image = blur_img(image)
            elif option == OPTION_3:
                image = resize_img(image)
            elif option == OPTION_4:
                image = rotate_img(image)
            elif option == OPTION_5:
                image = edge_img(image)
            elif option == OPTION_6:
                image = quantize_img(image)
            elif option == OPTION_7:
                show_image(image)
        except Exception as e:
            print(str(e))

    while True:
        try:
            save_or_not = input("Please enter 1 to save or 2 to quit without saving: ")
            if save_or_not not in ("1", "2"):
                raise Exception("Invalid input, only '1' and '2' are allowed")
            if save_or_not == "1":
                new_path = input("Please enter a name the image (saved locally): ")
                save_image(image, new_path)
                print(new_path+".png saved in your directory!")
                break
            elif save_or_not == "2":
                break
        except Exception as e:
            print(str(e))
    print("GOODBYE!")
