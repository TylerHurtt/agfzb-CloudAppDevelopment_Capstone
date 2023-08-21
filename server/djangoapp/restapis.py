import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
import Features, CategoriesOptions, SentimentOptions, SyntaxOptions, SyntaxOptionsTokens

API_KEY = "cweLMsiMGq4xdfSrZEoAwt5fhnbNUe9LQbqxh07f2s7F"
SERVICE_URL = "https://c9a85a36-e64f-40a1-a6a6-797774dbc9f8-bluemix.cloudantnosqldb.appdomain.cloud"

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        params = {}
        params["api_key"] = "api_key" in kwargs and kwargs['api_key'] or API_KEY
        params["service_url"] = SERVICE_URL
        params["dealer_id"] = "dealer_id" in kwargs and kwargs["dealer_id"] or None
        params["text"] = "text" in kwargs and kwargs["text"] or None
        params["version"] = "version" in kwargs and kwargs["version"] or None
        params["features"] = "features" in kwargs and kwargs["features"] or None
        params["return_analyzed_text"] = "return_analyzed_text" in kwargs and kwargs["return_analyzed_text"] or None
        if API_KEY:
            response = requests.get(
                url,
                headers={'Content-Type': 'application/json'},
                params=params,
                auth=HTTPBasicAuth('apikey', API_KEY))
        else: 
            response = requests.get(
                url,
                headers={'Content-Type': 'application/json'},
                params=params)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print('kwargs', kwargs)
    print("POST from {} ".format(url))
    try:
        # Call post method of requests library with URL and parameters
        params = {}
        params["api_key"] = API_KEY
        params["service_url"] = SERVICE_URL
        print('params', params)
        response = requests.post(
            url,
            params=params)
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
    print('results', results)
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
    reviews = get_request(url)
    print('reviews', reviews)
    results = []
    if reviews:
        for review in reviews:
            if 'dealership' in review and review['dealership'] == dealer_id:
                dealership = ('dealership' in review and review['dealership']) or 'TBD - car_make'
                name = ('name'in review and review['name']) or 'TBD - car_make'
                purchase = ('purchase'in review and review['purchase']) or 'TBD - car_make'
                purchase_date = ('purchase_date' in review and review['purchase_date']) or 'TBD - purchase_date'
                dealer_review = ('review' in review and review['review']) or 'TBD - review'
                car_make = ('car_make' in review and review['car_make']) or 'TBD - car_make'
                car_model = ('car_model' in review and review['car_model']) or 'TBD - car_make'
                car_year = ('car_year 'in review and review['car_year']) or 'TBD - car_make'
                sentiment = dealer_review and analyze_review_sentiments(dealer_review) or None
                # removed sentiment
                results.append(DealerReview(dealership=dealership, name=name, purchase=purchase, review=dealer_review,
                    purchase_date=purchase_date, car_make=car_make, car_model=car_model,
                    car_year=car_year, sentiment=sentiment, id=dealer_id))
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    api_key = 'R3iPUaL4O5Z6JSBHCj9jvc9Ws1JnTv_kPA-q66FwRblG'
    service_url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f368f39c-7d0c-4114-a122-66eeb7235d47'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(service_url)

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions())).get_result()


    print(json.dumps(response, indent=2))
    return response['sentiment']['document']['label']
