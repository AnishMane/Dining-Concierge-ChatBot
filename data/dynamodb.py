from collections import defaultdict
import json
import time
from datetime import datetime
from decimal import Decimal
import boto3

def check_empty(input):
    if len(str(input)) == 0:
        return 'N/A'
    else:
        return input

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

cuisines = ['american', 'chinese', 'french', 'indian', 'italian', 'japanese', 'korean', 'mexican']

manhattan_nbhds = ['Lower East Side, Manhattan',
                    'Upper East Side, Manhattan',
                    'Upper West Side, Manhattan',
                    'Washington Heights, Manhattan',
                    'Central Harlem, Manhattan',
                    'Chelsea, Manhattan',
                    'Manhattan',
                    'East Harlem, Manhattan',
                    'Gramercy Park, Manhattan',
                    'Greenwich, Manhattan',
                    'Lower Manhattan, Manhattan']

# Define the limit for the number of businesses to process
business_limit = 10  # Adjust this value as needed

start = time.time()

for cuisine in cuisines:
    for nbhd in manhattan_nbhds:
        with open(f'data/JSON/{cuisine}.json', 'r') as f:
            data = json.load(f)
            businesses = data['0']['businesses'][:business_limit]  # Limit the number of businesses
            for business in businesses:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                table.put_item(
                    Item = {
                        'BusinessID': check_empty(business['id']),
                        'insertedAtTimestamp': check_empty(dt_string),
                        'Name':  check_empty(business['name']),
                        'Cuisine': check_empty(cuisine),
                        'Rating': check_empty(Decimal(str(business['rating']))),
                        'Number of Reviews': check_empty(Decimal(str(business['review_count']))),
                        'Address': check_empty(business['location']['address1']),
                        'Zip Code': check_empty(business['location']['zip_code']),
                        'Latitude': check_empty(str(business['coordinates']['latitude'])),
                        'Longitude': check_empty(str(business['coordinates']['longitude'])),
                        'Open': 'N/A'
                    }
                )
    print('Fin ', cuisine, time.time() - start)
