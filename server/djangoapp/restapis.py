import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# def get_request(url, api_key = None, **kwargs):
#     try:
#         # Call get method of requests library with URL and parameters
#         if api_key is None :
#             response = requests.get(
#                 url,
#                 headers={'Content-Type': 'application/json'},
#                 params=kwargs
#             )
#         else:
#             params = dict()
#             params["text"] = kwargs["text"]
#             params["version"] = kwargs["version"]
#             params["features"] = kwargs["features"]
#             params["return_analyzed_text"] = kwargs["return_analyzed_text"]
#             response = requests.get(
#                 url,
#                 params=params,
#                 headers={'Content-Type': 'application/json'},
#                 auth=HTTPBasicAuth('apikey', api_key)
#             )

#     except:
#         # If any error occurs
#         print("Network exception occurred")

#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
            params=kwargs)
    except:
        #if any error
        print("Network exception occurred")
        status_code = response.status_code
        print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the data list in JSON as dealers
        dealers = json_result["data"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in dealer object
            dealer_obj = CarDealer(address=dealer["address"],city=dealer["city"],id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
            st=dealer["st"],state=dealer["state"],short_name=dealer["short_name"],zip=dealer["zip"])
            results.append(dealer_obj)

    return results



def get_dealer_by_id_from_cf(url, dealer_id):
    json_result = get_request(url, id=dealer_id)
    if json_result:
        # Get the data list in JSON as dealers
        dealer = json_result["data"]
        # For each dealer object
        
        # Create a CarDealer object with values in dealer object
        dealer_obj = CarDealer(address=dealer["address"],city=dealer["city"],id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
        st=dealer["st"],state=dealer["state"],short_name=dealer["short_name"],zip=dealer["zip"])

    return dealer_obj
            

def get_dealers_by_st_from_cf(url, state):
    results = []
    json_result = get_request(url, st=state)
    if json_result:
        # Get the data list in JSON as dealers
        dealers = json_result["data"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in dealer object
            dealer_obj = CarDealer(address=dealer["address"],city=dealer["city"],id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
            st=dealer["st"],state=dealer["state"],short_name=dealer["short_name"],zip=dealer["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews =  json_result["body"]["data"]
        for review in reviews:
            review_obj = DealerReview(
                name=review["name"],
                dealership=review["dealership"],
                review=review["review"],
                # sentiment=analyze_review_sentiments(review_doc["review"]),
                sentiment="neutral",
                purchase=review["purchase"],
                purchase_date=review["purchase_date"],
                id=review["id"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"]
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results



  
def analyze_review_sentiments(text): 

    url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/f9dd4548-de9f-4d65-9ba7-5e7932ee8975'
    api_key = '11L3dYqniDQxLUcLl8B_DFSBYK-oyFaWGzLOOZhQwQdn'


    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version="2022-04-07",authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze( text=text + " " + text + " " + text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 

    label=json.dumps(response, indent=2) 

    label = response['sentiment']['document']['label'] 

    return(label) 

