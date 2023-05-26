import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
from edit import *
from create import create_json
from convert import convert_json_2_png

WHITE = "#ffffff"
YELLOW = "#ebeb34"
BLUE = "#348ac9"
GREEN = "#3bc934"
LBLUE = "#b0d7ff"
RED = "#de4028"


# ImageEditor GUI
class ImageEditorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor")
        self.config(bg=LBLUE)
        self.window = tk.Tk
        self.__widget_lst = []
        self.__round = 0
        self.json_path = ""
        self.image_path = ""
        self.image = []
        self.attributes('-fullscreen', True)
        self.columnconfigure(index=0, weight=100)
        self.columnconfigure(index=20, weight=100)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=8, weight=1)
        self.__create_exit_button()
        self.__create_submit_button()
        self.create_json = create_json
        self.convert_json_2_png = convert_json_2_png
        self.load_image = load_image
        self.save_image = save_image
        self.show_image = show_image

    # create the exit button
    def __create_exit_button(self):
        btn = tk.Button(self, text="Exit", font=("Helvetica", 12))
        btn.configure(command=lambda e=1: self.destroy())
        btn.place(height=30, width=60, relx=0.95, rely=0.05)

    # create a start button for the game (for first initiation of the game itself, meaning to start first round)
    def __create_submit_button(self):
        self.prompt = tk.Label(self, text="Please describe the picture you would want:")
        self.prompt.grid(row=1, column=0)
        self.text_entry = tk.Entry(self)
        self.text_entry.grid(row=2, column=0)
        btn = tk.Button(self, text="Submit", font=("Helvetica", 12))
        btn.configure(command=lambda button=btn: self.__submit_btn_pressed(button))
        self.__widget_lst.append(btn)
        btn.place(height=30, width=60, relx=0.5, rely=0.5, anchor="center")

    # generates the image and move to the editing window
    def __submit_btn_pressed(self, button):
        self.create_image()
        button.destroy()
        self.prompt.destroy()
        self.text_entry.destroy()
        self.__widget_lst.pop()
        self.__start()

    def create_image(self):
        prompt = self.text_entry.get()
        self.json_path = self.create_json(prompt)
        self.image_path = self.convert_json_2_png(self.json_path)  # list of images
        self.image = self.load_image(self.image_path[0])  # Use the first image file path

    # starts a round of the game by destroying all widget that need replacing, creating the alternate ones and setting
    # up needed values
    def __start(self):
        self.__destroy_all(self.__widget_lst)
        self.__button_grid = []
        self.__current_path = []
        self.__create_widgets()

    # destroys all widgets in the given widget list
    def __destroy_all(self, widget_lst):
        for widget in widget_lst:
            widget.grid_remove()
        self.__widget_lst.clear()

    # create all widgets in the game (except for the buttons, which are created separately)
    def __create_widgets(self):
        # create the save button
        self.__save_btn = tk.Button(self, text="Save", font=("Helvetica", 12))
        self.__save_btn.configure(command=lambda e=1: self.save_image(self.image))
        self.__save_btn.place(height=30, width=60, relx=0.95, rely=0.10)
        self.__widget_lst.append(self.__save_btn)

        # create the show image button
        self.__show_img_btn = tk.Button(self, text="Show Image", font=("Helvetica", 12))
        self.__show_img_btn.configure(command=lambda e=1: self.show_image(self.image))
        self.__show_img_btn.place(height=30, width=60, relx=0.95, rely=0.20)
        self.__widget_lst.append(self.__show_img_btn)

        # create the RGB to gray button
        self.__RGB_2_gray_button = tk.Button(self, text="Convert RGB Image to gray", font=("Helvetica", 10))
        self.__RGB_2_gray_button.configure(command=lambda e=1: self.edit_image(RGB_2_gray(self.image)))
        self.__RGB_2_gray_button.place(height=30, width=60, relx=0.95, rely=0.25)
        self.__widget_lst.append(self.__RGB_2_gray_button)

        # create the resize button
        self.__blur_button = tk.Button(self, text="Blur the image", font=("Helvetica", 10))
        self.__blur_button.configure(command=lambda e=1: self.edit_image(blur_img(self.image)))
        self.__blur_button.place(height=30, width=60, relx=0.95, rely=0.30)
        self.__widget_lst.append(self.__blur_button)

        # create the resize button
        self.__resize_button = tk.Button(self, text="Change the image size", font=("Helvetica", 10))
        self.__resize_button.configure(command=lambda e=1: self.edit_image(resize_img(self.image)))
        self.__resize_button.place(height=30, width=60, relx=0.95, rely=0.35)
        self.__widget_lst.append(self.__resize_button)

        # create the Rotate button
        self.__rotate_button = tk.Button(self, text="Rotate the image by 90 degrees", font=("Helvetica", 10))
        self.__rotate_button.configure(command=lambda e=1: self.edit_image(rotate_img(self.image)))
        self.__rotate_button.place(height=30, width=60, relx=0.95, rely=0.40)
        self.__widget_lst.append(self.__rotate_button)

        # create the edge button
        self.__edge_button = tk.Button(self, text="Make edges for the image", font=("Helvetica", 10))
        self.__edge_button.configure(command=lambda e=1: self.edit_image(edge_img(self.image)))
        self.__edge_button.place(height=30, width=60, relx=0.95, rely=0.45)
        self.__widget_lst.append(self.__edge_button)

        # create the quantize button
        self.__quantize_button = tk.Button(self, text="Quantize the image", font=("Helvetica", 10))
        self.__quantize_button.configure(command=lambda e=1: self.edit_image(quantize_img(self.image)))
        self.__quantize_button.place(height=30, width=60, relx=0.95, rely=0.50)
        self.__widget_lst.append(self.__quantize_button)

        for idx, button in enumerate(self.__widget_lst):
            button.grid(row=idx, column=0)  # Adjust row and column values according to your layout

        # self.__save_button.grid(row=len(self.__widget_lst),
        #                         column=0)  # Adjust row and column values according to your layout

    def edit_image(self, edit_func):
        def thread_func():
            self.image = edit_func(self.image)
            self.show_image(self.image)

        messagebox.showinfo("Please wait", "Processing image...")

        edit_thread = threading.Thread(target=thread_func)
        edit_thread.start()

    # end the edit, and check if the player wants to go again
    def end_game(self):
        play_again = messagebox.askyesno("Do you want to save and exit?")
        if play_again:
            self.__start()
        else:
            self.save_image()
            self.destroy()

    # runs the program
    def run(self):
        self.mainloop()


if __name__ == '__main__':
    gui = ImageEditorGUI()
    gui.run()
