from datetime import datetime
from utils import get_response


class PoliceAPI(object):

    def __init__(self):
        self.base_url = 'https://data.police.uk/api/'
        self.today = datetime.today()
        # self.current_month = str(datetime(self.today.year, self.today.month, 1))[:7]
        self.current_month = '2020-07'

    def get_crime_at_location(self, lat, long):
        url = self.base_url + 'crimes-at-location?date=' + self.current_month + '&lat=' + lat + '&lng=' + long
        response = get_response(url)
        return response

    def get_neighbourhood_codes(self, police_force):
        url = self.base_url + police_force + '/neighbourhoods'
        response = get_response(url)
        return response

    def get_neighbourhood_boundaries(self, police_force, neighbourhood_code):
        url = self.base_url + police_force + '/' + neighbourhood_code + '/boundary'
        response = get_response(url)
        return response


if __name__ == "__main__":
    police = PoliceAPI()
