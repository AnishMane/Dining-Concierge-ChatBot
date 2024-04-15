import requests
import json
import sys
import time

API_KEY = "TTAN4E1LxC-u2Q52j8pZg2n-lScQACibolHb7-vV01W3D-Im-NNVRihJu-eASRCn9dhSIAmc5Q7CGPSWai8jCLhVnFLHUfBVyCaDUMzuBj2aqGEHjaeXNe6WrrccZnYx"
cuisines = ['chinese', 'japanese', 'italian', 'korean', 'french', 'american', 'mexican', 'indian']

def request(api_key, term, location = "New York", limit = 50):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % api_key}
    response = []
    id_set = set()
 
    offset = 0
    json_map = {}
    
    for i in range(20):
        offset += 50
        params = {'term':term,'location': location, 'limit': limit, 'offset': offset}
        req = requests.get(url, params = params, headers = headers)
        print(req.status_code)
        json_map[i] = req.json()
        

    file_name = term + '.json'
    with open(file_name, 'w') as openfile:
        json.dump(json_map, openfile, indent = 4)
    
def main():      
    for cuisine in cuisines:
        request(API_KEY, cuisine)
        
        time.sleep(150)


if __name__ == '__main__':
    main()