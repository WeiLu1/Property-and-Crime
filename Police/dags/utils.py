import requests
import json
import numpy as np
import os
from datetime import datetime, timedelta


def get_response(url):
    try:
        response = requests.get(url)
        if response:
            json_response = json.loads(response.text)
            return json_response
    except Exception as e:
        raise e


def write_to_json(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)


def load_json(json_name):
    dir_path = os.getcwd() + '/Police/dags/'
    json_path = os.path.join(dir_path, json_name)
    print(json_path)
    with open(json_path) as file:
        data = json.load(file)
    return data


def load_json_local(json_name):
    with open(os.getcwd() + '/' + json_name) as file:
        data = json.load(file)
    return data


def get_linear_spaced_indexes(length, spacing):
    indexes = np.round(np.linspace(0, length - 1, spacing)).astype(int)
    return indexes


def get_last_month():
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime("%Y-%m")


if __name__ == "__main__":
    get_last_month()
