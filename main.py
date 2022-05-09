import sys
import math

from PIL import Image


def colored(r: tuple, g: tuple, b: tuple, text: list):
    return "\033[48;2;{};{};{}m{} \u001b[0m".format(r, g, b, text)


def pixels_equal(pixel1: tuple, pixel2: tuple, tolerance: int):
    for i in range(len(pixel1)):
        if abs(pixel1[i] - pixel2[i]) > tolerance:
            return False
    return True


def print_color_part(distance: int, color_rgb: list, px_to_cm: int):
    distance_cm = math.ceil(distance / px_to_cm)
    print("Barva ", colored(color_rgb[0], color_rgb[1], color_rgb[2], color_rgb), " na ", distance_cm, "cm.")


if len(sys.argv) < 2:
    print("Chyba! Musíte předat soubor se vzorem.")
    exit(1)

with Image.open(sys.argv[1]) as im:
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    print("Vzor s rozměry ", width, "x", height, "px")
    px_to_cm_input = int(input("Kolik px chcete reprezentovat jako 1cm? "))

    for index, pixelRow in enumerate(pixels):
        is_even = index % 2 == 0
        print("Řádek č.", index, "zleva doprava" if is_even else "zprava doleva")
        print("-------------------------------------------")
        last_distance = 0
        last_pixel = pixelRow[0]
        for pixel in (pixelRow if is_even else reversed(pixelRow)):
            if pixels_equal(pixel, last_pixel, 30):
                last_distance += 1
            else:
                print_color_part(last_distance, last_pixel, px_to_cm_input)
                last_pixel = pixel
                last_distance = 1
        print_color_part(last_distance, last_pixel, px_to_cm_input)
        print("\n")
