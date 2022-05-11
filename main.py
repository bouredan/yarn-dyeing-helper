import math

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

from PIL import Image

RGB_THRESHHOLD = 20
PIXEL_THRESHOLD = 10


def colored(r: tuple, g: tuple, b: tuple, text: list):
    return "\033[48;2;{};{};{}m{} \u001b[0m".format(r, g, b, text)


def from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


def pixels_equal(pixel1: tuple, pixel2: tuple, tolerance: int):
    for i in range(len(pixel1)):
        if abs(pixel1[i] - pixel2[i]) > tolerance:
            return False
    return True


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "Výpočet barvení příze"
        self.geometry("1024x768")

        # text output
        self.text_output = tk.scrolledtext.ScrolledText(self, font=("Arial", 16))
        self.text_output.pack(fill="both", expand=True)

        # button
        self.button = tk.Button(self, text="Vyber vzor", command=self.open_file)
        self.button.pack()

    def open_file(self):
        filename = filedialog.askopenfilename()
        self.process_image(filename)

    def process_image(self, filename: str):
        self.text_output.delete("1.0", tk.END)
        with Image.open(filename) as im:
            im = im.convert("RGB")
            pixels = list(im.getdata())
            width, height = im.size
            pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
            self.print_to_output(str.format("Vzor s rozměry {}x{}px\n\n", width, height))
            px_to_cm_input = 3  # int(input("Kolik px chcete reprezentovat jako 1cm? "))

            for index, pixelRow in enumerate(pixels):
                is_even = index % 2 == 0
                self.print_to_output(str.format("Řádek č. {} {}\n",
                                                index,
                                                "zleva doprava" if is_even else "zprava doleva"))
                self.print_to_output("-------------------------------------------\n")
                last_distance = 0
                last_pixel = pixelRow[0]
                for pixel in (pixelRow if is_even else reversed(pixelRow)):
                    if pixels_equal(pixel, last_pixel, RGB_THRESHHOLD):
                        last_distance += 1
                    else:
                        if last_distance < PIXEL_THRESHOLD:
                            last_distance += 1
                            continue
                        self.print_color_part(last_distance, last_pixel, px_to_cm_input)
                        last_pixel = pixel
                        last_distance = 1
                self.print_color_part(last_distance, last_pixel, px_to_cm_input)
                self.print_to_output("\n")

    def print_to_output(self, text: str, *args):
        self.text_output.insert(tk.INSERT, text, *args)

    def print_color_part(self, distance: int, color_rgb: list, px_to_cm: int):
        color = from_rgb(color_rgb)
        self.text_output.tag_configure(color, background=color)

        distance_cm = math.ceil(distance / px_to_cm)
        self.print_to_output("Barva ")
        self.print_to_output(color, color)
        self.print_to_output(str.format(" na {} cm.\n", distance_cm))


if __name__ == "__main__":
    app = App()
    app.mainloop()
