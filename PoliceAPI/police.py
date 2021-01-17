import requests
import json
from datetime import datetime


def get_response(url):
    try:
        response = requests.get(url)
        if response:
            json_response = json.loads(response.text)
            return json_response
    except Exception as e:
        raise e


class PoliceAPI(object):

    def __init__(self):
        self.base_url = "https://data.police.uk/api/"
        self.today = datetime.today()
        # self.current_month = str(datetime(self.today.year, self.today.month, 1))[:7]
        self.current_month = '2020-07'

    def get_crime_at_location(self, lat, long):
        url = self.base_url + "crimes-at-location?date=" + self.current_month + "&lat=" + lat + "&lng=" + long
        json_response = get_response(url)
        return json_response

    def get_stop_search(self, lat, long):
        url = self.base_url + "stops-street?lat=" + lat + "lng=" + long + "&date=" + self.current_month
        json_response = get_response(url)
        return json_response


if __name__ == "__main__":
    police = PoliceAPI()
