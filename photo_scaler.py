#!/usr/local/bin/python3
"""
Batch Photo Scaler 
by JL 2022

this script scales all .jpg and .jpeg files at given path
to the given (biger) dimension, and saves them in new folder
"""
import argparse
from pathlib import Path
from PIL import Image

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to dir with photos")
    parser.add_argument("max_dim", help="[int] maximum dimmention after scaling")
    parser.add_argument("-y", action="store_true", help="Do not ask for confirmation")
    return parser.parse_args()

def confirm_resize(photos):
    menu = None
    while menu not in ["y", "Y", "n", "N"]:
        menu = input(f"{len(photos)} images found, do you want to resize them? (y/n) ")

    if menu in ["n", "N"]:
        print("Abort mission!")
        raise SystemExit(0)
    

def mk_photo_dir(path: Path, max_dim: str):
    """
    ensure dest directory and return its path
    """
    dest_dir = Path.joinpath(path, f"{max_dim}px")
    Path(dest_dir).mkdir(exist_ok=True)
    return dest_dir


def locate_photos(path: Path) -> list:
    """
    returns a list of .jpg and jpeg paths
    """
    print("Working in: " + str(path))
    suffs = [".jpg", ".jpeg"]
    photo_list = []
    for f in path.iterdir():
        if f.suffix in suffs:
            photo_list.append(f)

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
    print("\nBatch Photo Scaler - welcome!\n")

    args = get_args()

    # path
    path = Path(args.path)
    if not path.is_dir():
        print(f"Invalid target dir: {str(path)}")
        raise SystemExit(1)

    # max_dim
    try: 
        max_dim = int(args.max_dim)
    except:
        print("Invalid max dimmension")
        raise SystemExit(1)

    photos = locate_photos(path)

    if not args.y:
        confirm_resize(photos)

    dest_dir = mk_photo_dir(path, max_dim)

    # resize images
    for i, f in enumerate(photos):
        print(f"\n{i+1}/{len(photos)} [{f}]")
        img = Image.open(f)
        img = scale_photo(img, max_dim)
        img.save(f"{dest_dir}/{f.name}")
        print()

    print("Done!\n")


if __name__ == "__main__":
    main()
