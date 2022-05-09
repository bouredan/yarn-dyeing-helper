import sys
from PIL import Image


def colored(r, g, b, text):
    return "\033[48;2;{};{};{}m{} \u001b[0m".format(r, g, b, text)


def pixels_equal(pixel1, pixel2, tolerance):
    for i in range(len(pixel1)):
        if abs(pixel1[i] - pixel2[i]) > tolerance:
            return False
    return True


if len(sys.argv) < 2:
    print("Chyba! Musíte předat soubor se vzorem.")
    exit(1)

with Image.open(sys.argv[1]) as im:
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    print("Vzor s rozměry ", width, "x", height, "px")

    for index, pixelRow in enumerate(pixels):
        is_even = index % 2 == 0
        print("Řádek č. ", index, " zleva doprava" if is_even else "zprava doleva")
        print("-------------------------------------------")
        last_distance = 0
        last_pixel = pixelRow[0]
        for pixel in (pixelRow if is_even else reversed(pixelRow)):
            if pixels_equal(pixel, last_pixel, 30):
                last_distance += 1
            else:
                print("Barva ", colored(last_pixel[0], last_pixel[1], last_pixel[2], last_pixel), " na ", last_distance,
                      "px.")
                last_pixel = pixel
                last_distance = 1
        print("Barva ", colored(last_pixel[0], last_pixel[1], last_pixel[2], last_pixel), " na ", last_distance, "px.\n\n")
