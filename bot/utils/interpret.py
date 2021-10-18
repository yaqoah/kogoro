# -*- coding: utf-8 -*-
import base64
from io import BytesIO
import requests
from PIL import Image
from bot import LOGGER


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format=image.format)
    return base64.b64encode(buffered.getvalue())


def url_to_base64(url):
    res = requests.get(url)
    if res.status_code == 200:
        return base64.b64encode(res.content)
    else:
        LOGGER.error(res.status_code)


def base64_to_image(img64):
    return Image.open(BytesIO(base64.b64decode(img64)))

