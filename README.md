# Batch Photo Scaler
## by JL (lipabass@gmail.com)
### Python 3.10
This script scales all .jpg and .jpeg images in a given folder.
Images are resized so that the biger dimension equals the desired value. Rescaled images are saved in a new folder with a name matching the desired dimension.

### Instalation and requirements
This script uses [Pillow (PIL Fork)](https://pillow.readthedocs.io).
To install Pillow run:
```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

### How to run Batch Photo Scaler
To run Batch Photo Scaler from terminal cd to the folder and run:
```
python3 photo_scaler.py
```
The script will ask you for a directory with photos and the desired dimension. Alternatively, you can:
```
python3 photo_scaler.py "folder_path" [dimension in px]
```