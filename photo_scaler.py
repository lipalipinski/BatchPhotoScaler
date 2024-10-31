#!/usr/local/bin/python3
"""
Batch Photo Scaler 
by JL 2022

this script scales all .jpg and .jpeg files at given path
to the given dimension, and saves them in new folder
"""
import argparse
import logging
import sys
from pathlib import Path
from PIL import Image

prog_name = "img-scaler"
prog_version = "1.0.0"

def get_args():
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="Scale images in <path> to <max_dim> size",
        epilog="JL 2024"
        )
    parser.add_argument("path", help="path to dir with photos")
    parser.add_argument("max_dim", help="[int] maximum dimmention after scaling")
    parser.add_argument("-y", action="store_true", help="Do not ask for confirmation")
    parser.add_argument("-s", "--silent", action="store_true", help="silent mode")
    parser.add_argument("--version", action="version", version=f"{prog_name} {prog_version}")
    return parser.parse_args()

def confirm_resize(photos):
    menu = None
    while menu not in ["y", "Y", "n", "N"]:
        menu = input(f"{len(photos)} images found, do you want to resize them? (y/n) ")

    if menu in ["n", "N"]:
        logging.info("Abort mission!")
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
    logging.info("Working in: " + str(path))
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
    logging.info(f"{h}x{w} -> {new_h}x{new_w}")
    photo = photo.resize((new_h, new_w))
    return photo


def main():
    args = get_args()
    logging.basicConfig(level=logging.INFO if not args.silent else logging.WARN, 
                        handlers=[logging.StreamHandler(sys.stdout)], 
                        format="%(message)s")

    logging.info("\nBatch Photo Scaler - welcome!\n")


    # path
    path = Path(args.path).absolute()
    if not path.is_dir():
        logging.warning(f"Invalid target dir: {str(path)}")
        raise SystemExit(1)

    # max_dim
    try: 
        max_dim = int(args.max_dim)
    except:
        logging.warning("Invalid max dimmension")
        raise SystemExit(1)

    photos = locate_photos(path)

    if not args.y:
        confirm_resize(photos)

    dest_dir = mk_photo_dir(path, max_dim)

    # resize images
    for i, f in enumerate(photos):
        logging.info(f"\n{i+1}/{len(photos)} [{f}]")
        img = Image.open(f)
        img = scale_photo(img, max_dim)
        img.save(Path.joinpath(dest_dir, f.name))

    logging.info("\nDone!\n")


if __name__ == "__main__":
    main()
