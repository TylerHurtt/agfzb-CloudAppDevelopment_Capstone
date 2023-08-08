import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth
def get_request(url, **kwargs):
    print('kwargs', kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print("response", response)
    print("text", response.text)
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def create_dealer_obj(dealer):
    address = 'address' in dealer and dealer['address'] or None
    city = 'city' in dealer and dealer['city'] or None
    full_name = 'full_name' in dealer and dealer['full_name'] or None
    id = 'id' in dealer and dealer['id'] or None
    lat = 'lat' in dealer and dealer['lat'] or None
    long = 'long' in dealer and dealer['long'] or None
    short_name = 'short_name' in dealer and dealer['short_name'] or None
    st = 'st' in dealer and dealer['st'] or None
    zip = 'zip' in dealer and dealer['zip'] or None
    return CarDealer(address=address or 'TBD - address', city=city or 'TBD  - ciy', full_name=full_name or 'TBD - full_name',
                        id=id or 'TBD - id', lat=lat or 'TBD - lat', long=long or 'TBD - long',
                        short_name=short_name or 'TBD - short_name',
                        st=st or 'TBD - st', zip=zip or 'TBD - zip')

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url)
    if dealers:
        # Get the row list in JSON as dealers
        # dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
           dealer_obj = create_dealer_obj(dealer)
           results.append(dealer_obj)
    return results

def get_dealers_by_state(url, **kwargs):
    state = kwargs['state']
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url, state=state)
    if dealers:
        # Get the row list in JSON as dealers
        state_dealers = list(filter(lambda dealers: dealers['state'] == state, dealerships))
        # For each dealer object
        for dealer in state_dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = create_dealer_obj(dealer)
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, **kwargs):
    dealer_id = kwargs["dealer_id"]
    # Call get_request with a URL parameter
    dealers = get_request(url, dealer_id=dealer_id)
    if dealers:
        # Get the row list in JSON as dealers
        dealer = list(filter(lambda dealer: dealer['id'] == dealerId, dealers))
        dealer_obj = create_dealer_obj(dealer)
    return dealer_obj


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



