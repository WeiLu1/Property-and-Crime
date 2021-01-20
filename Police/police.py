from datetime import datetime
from utils import get_response
from postcode import get_borough
from utils import write_to_json


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


def match_police_code_to_borough():
    police_force = 'metropolitan'

    police_obj = PoliceAPI()
    borough = ''
    borough_total = []
    metropolitan_codes = police_obj.get_neighbourhood_codes(police_force)
    for pair in metropolitan_codes:
        borough_dict = {}
        id = pair['id']
        name = pair['name']
        boundaries = police_obj.get_neighbourhood_boundaries(police_force, id)

        i = 0
        while i < len(boundaries) - 1:
            lat = boundaries[i]['latitude']
            long = boundaries[i]['longitude']
            borough = get_borough(lat, long)
            if borough == "CAN'T FIND BOROUGH":
                i += 1
            else:
                break

        borough_dict['id'] = id
        borough_dict['name'] = name
        borough_dict['borough'] = borough
        borough_total.append(borough_dict)
        print(id + ', ' + name + ', ' + borough)
    write_to_json('borough.json', borough_total)


def get_polygon_district():
    pass


if __name__ == "__main__":

    match_police_code_to_borough()

