import requests
import json
import numpy as np
import pandas as pd
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


def json_to_csv(json_name, csv_name):
    dir_path = os.getcwd() + '/Police/dags/'
    json_path = dir_path + json_name
    csv_path = dir_path + csv_name
    csv = pd.read_json(json_path)
    csv.to_csv(csv_path, index=False)


def load_json(json_name):
    dir_path = os.getcwd() + '/Police/dags/'
    json_path = os.path.join(dir_path, json_name)
    print(json_path)
    with open(json_path) as file:
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
    load_json('boroughs_info.json')
    get_last_month()
