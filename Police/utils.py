import requests
import json
import pandas as pd
import os

path_project = os.getcwd()


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
    json_path = path_project + '/' + json_name
    csv_path = path_project + '/' + csv_name
    csv = pd.read_json(json_path)
    csv.to_csv(csv_path, index=False)


if __name__ == "__main__":
    json_to_csv('borough.json', 'borough.csv')
