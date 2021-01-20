from utils import get_response


class PostCodeAPI(object):

    def __init__(self):
        self.base_url = 'http://api.postcodes.io/postcodes'

    def get_nearest_postcode_response(self, lat, long):
        url = self.base_url + '?lon=' + long + '&lat=' + lat
        response = get_response(url)
        return response


def get_borough(lat, long):
    postcode = PostCodeAPI()
    nearest_postcode = postcode.get_nearest_postcode_response(lat, long)
    if nearest_postcode['result'] is None:
        return "CAN'T FIND BOROUGH"
    else:
        borough = nearest_postcode['result'][0]['admin_district']
        return borough
