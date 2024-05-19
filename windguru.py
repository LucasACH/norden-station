import hashlib
import random

import requests

BASE_URL = "https://www.windguru.cz/"


def _generate_hash(uid, password):
    salt = str(random.randint(10000000000000, 90000000000000))
    hash = hashlib.md5((salt + uid + password).encode()).hexdigest()
    return salt, hash


def upload_data(uid, password, wind, gust, direction):

    salt, hash = _generate_hash(uid, password)

    params = {
        "uid": uid,
        "salt": salt,
        "hash": hash,
        "interval": 360,
        "wind_avg": wind,
        "wind_max": gust,
        "wind_direction": direction,
    }

    res = requests.get(BASE_URL + "upload/api.php", params=params)

    if res.text != "OK":
        raise Exception("Failed to upload data to Windguru")


def get_station_current_data(uid, password):
    params = {
        "uid": uid,
        "password": password,
        "q": "station_data_current",
    }

    res = requests.get(BASE_URL + "int/wgsapi.php", params=params)

    return res.json()
