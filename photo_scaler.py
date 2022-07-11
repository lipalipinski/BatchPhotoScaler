"""
Batch Photo Scaler 
by JL 2022

this script scales all .jpg and .jpeg files at given path
to the given (biger) dimension, and saves them in new folder
"""
import sys
import os
import re
from PIL import Image


def get_path():
    """
    gets path from 1st arg passed from terminal or
    asks for a folder path
    checkec if it's valid
    returns a folder path (string)
    returns False if folder path from command is incorrect
    """
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isdir(path):
            return path
        else:
            print("Folder path incorrect!")
            return False

    while True:
        path = input("Image folder path: ")
        if os.path.isdir(path):
            return path
        else:
            print("Folder path incorrect!")


def get_dimension():
    """
    gets dimension from 2nd arg passed from terminal or
    asks for a maximum dimension
    returns int
    """

    # check if dim passed from terminal
    if len(sys.argv) == 3:
        try:
            dim = int(sys.argv[2])
            return dim
        except ValueError:
            print("Passed dimension incorrect...")

    # if not or incorrect ask for dim
    while True:
        try:
            dim = int(input("Max dimension (px): "))
            break
        except ValueError:
            print("Incorrect value!")
    return dim


def mk_photo_dir(path, dim):
    """
    checks if destination folder exists
    creates new if not
    """
    if os.path.isdir(path + "/" + str(dim) + "px"):
        return
    else:
        os.mkdir(path + "/" + str(dim) + "px")
    return


def locate_photos(path):
    """
    returns a list of .jpg and jpeg
    files at given path, case insensitive
    """
    photo_list = []
    list_dir = os.listdir(path)
    for guess in list_dir:

        pat = re.compile("(?i)(jpe?g)$")
        if re.search(pat, guess):
            photo_list.append(guess)

    return photo_list


def scale_photo(photo: Image, max_dim):
    """
    returnes scaled down image
    """
    h, w = photo.size
    factor = max_dim / max(w, h)
    new_h = int(h * factor)
    new_w = int(w * factor)
    print(f"{h}x{w} -> {new_h}x{new_w}")
    photo = photo.resize((new_h, new_w))
    return photo


def main():
    """
    main func
    """
    print("\nBatch Photo Scaler - welcome!\n")
    path = get_path()

    # break if path provided incorrect
    if path == False:
        return

    print("Working in: " + path)
    photos = locate_photos(path)

    # comfirm resizing
    menu = None
    while menu not in ["y", "Y", "n", "N"]:
        menu = input(f"{len(photos)} images found, do you want to resize them? (y/n) ")

    if menu in ["n", "N"]:
        print("Abort mission!")
        return

    # ask for dimension
    max_dim = get_dimension()

    # create a directory (if necessary)
    mk_photo_dir(path, max_dim)

    # resize images
    for num, name in enumerate(photos):
        print(f"\n{num+1}/{len(photos)} [{name}]")
        img = Image.open(path + "/" + name)
        img = scale_photo(img, max_dim)
        img.save(path + "/" + str(max_dim) + "px/" + name)
        print()

    print("Done!\n")


if __name__ == "__main__":
    main()
