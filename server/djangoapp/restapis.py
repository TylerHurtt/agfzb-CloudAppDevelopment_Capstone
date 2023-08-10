import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
def get_request(url, **kwargs):
    print('kwargs', kwargs)
    print("GET from {} ".format(url))

    try:
        params = dict()
        params["user_id"] = 15
        params["IAM_API_KEY"] = "cweLMsiMGq4xdfSrZEoAwt5fhnbNUe9LQbqxh07f2s7F"
        params["COUCH_URL"] = "https://c9a85a36-e64f-40a1-a6a6-797774dbc9f8-bluemix.cloudantnosqldb.appdomain.cloud"
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})

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
    return CarDealer(address=address or 'TBD - address', city=city or 'TBD  - city', full_name=full_name or 'TBD - full_name',
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
    dealer_id = kwargs['dealer_id']
    # Call get_request with a URL parameter
    review_obj.sentiment = analyze_review_sentiments(review_obj.review)
    print('here')
    reviews = get_request(url)
    print('reviews', reviews)
    results = []
    if reviews:
        for review in reviews:
            dealership = review['dealership'] or 'TBD - dealership'
            name = review['name'] or 'TBD - name'
            purchase = review['purchase'] or 'TBD - purchase'
            purchase_date = ('purchase_date'in review and review['purchase_date']) or 'TBD - purchase_date'
            dealer_review = review['review'] or 'TBD - review'
            car_make = ('car_make'in review and review['car_make']) or 'TBD - car_make'
            car_model = ('car_model'in review and review['car_model']) or 'TBD - car_model'
            car_year = ('car_year'in review and review['car_year']) or 'TBD - car_year'
            sentiment = ('review'in review and analyze_review_sentiments(review['review']) or 'TBD - sentiment'
            test = ('test'in review and review['test']) or 'TBD - test'

            # removed sentiment
            results.append(DealerReview(dealership=dealership, name=name, purchase=purchase, review=dealer_review,
                purchase_date=purchase_date, car_make=car_make, car_model=car_model,
                car_year=car_year, sentiment=7, id=dealer_id))
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):


