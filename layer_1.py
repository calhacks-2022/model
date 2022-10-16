from suggest_library import get_recommendations
from npm_search import search_npm

def layer_1(user_input):
    cohere_api_key = ""
    with open('cohere_apikey.txt') as f:
        cohere_api_key = f.readline()
    google_api_key = ""
    with open('google_cloud_apikey.txt') as f:
        google_api_key = f.readline()
    
    cohere_suggestions = get_recommendations(cohere_api_key, user_input)
    plausible_packages = search_npm(google_api_key, cohere_suggestions)
    return plausible_packages

if __name__ == "__main__":
    print(layer_1("best ui library"))
    