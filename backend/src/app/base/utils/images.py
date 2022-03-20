from tempfile import SpooledTemporaryFile
from typing import IO
from PIL import Image, ImageOps


def resize_image(img: SpooledTemporaryFile[bytes] | IO, size: tuple[int, int]):
    img: Image.Image = Image.open(img)
    crop: bool = not img.width / size[0] == img.height / size[1]
    if not crop:
        img.thumbnail(size, Image.ANTIALIAS)
    else:
        img = ImageOps.fit(img, size, Image.ANTIALIAS, centering=(0.5, 0.5))
    return img
