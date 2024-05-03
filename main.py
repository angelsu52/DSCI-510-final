import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import sqlite3
import time

# Data Source 1: Web Scrapping Census Data
# Outputs the df of a specified data topic of the city, state
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def convert_values(extracted_values):
    result = []
    for value in extracted_values:
        if '%' in value:
            result.append(round(float(value.strip('%')), 2))
        elif '$' in value:
            result.append(float(value.replace('$', '').replace(',', '')))
        else:
            result.append(value)
    return result


def get_codes(city, state):
    url = f'https://statisticalatlas.com/place/{state}/{city}/Overview'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    codes = [code.text for code in soup.select('.info-table-contents-div a[href*=zip]')]
    return codes


# Race-And-Ethnicity, Household-Income
def get_city_data(topic, city, zip):
    if zip == 'all':
        url = f'https://statisticalatlas.com/place/Washington/{city}/{topic}'
    else:
        url = f'https://statisticalatlas.com/zip/{zip}/{topic}'
    r = requests.get(url, timeout=10, headers=request_headers, verify=True)
    soup = BeautifulSoup(r.text, 'html.parser')
    # select values according to data
    if topic == 'Household-Income':
        shape_select = '[id="figure/household-income-percentiles"] rect title'
        labels = soup.select('[id="figure/household-income-percentiles"] g text[text-anchor="end"]')
        if labels:
            extracted_labels = [labels[i].text for i in range(0, int(len(labels) / 2))]
    elif topic == 'Race-and-Ethnicity':
        shape_select = '[id="figure/race-and-ethnicity"] rect title'
        labels = soup.select('[id="figure/race-and-ethnicity"] g text[text-anchor="end"]')
        if labels:
            # if exist, then take the 6 official demographics
            extracted_labels = [labels[i].text for i in range(0, 6)]
    else:
        print("Topic Unavailable.")

    values = soup.select(shape_select)
    df = pd.DataFrame()
    if values:
        extracted_values = [values[i].text for i in range(0, len(values), 2)]
        result = convert_values(extracted_values)
        df = pd.DataFrame({
            'city': city,
            'zip': zip,
            'description': extracted_labels,
            'value': result
        })
    return df


# Data Source 2: Yelp API

# Gets Yelp Data, 1000 data points
def get_yelp_data(location, term, api_key):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'

    data = []
    # Offset, 20 API calls per run (0 to 1000, offset by 50)
    for offset in range(0, 1000, 50):
        params = {
            'limit': 50,
            'location': location.replace(' ', '+'),
            'term': term.replace(' ', '+'),
            'offset': offset
        }

        response = requests.get(url, headers=headers, params=params)
        #  Catches required error codes
        if response.status_code == 200:
            data += response.json()['businesses']
        elif response.status_code == 429:
            print('Too many Requests')
            break
        elif response.status_code == 400:
            print('400 Bad Request')
            break

    return data


# Extract Yelp data and changes the response result to a dataframe containing the following columns:
#   - city, source, name, rating, categories, pricing, num_reviews
def extract_yelp_data(data):
    names = []
    ratings = []
    pricing = []
    cnt = []
    categories = []
    latitude = []
    longitude = []
    url = []
    zip = []
    for i in range(len(data)):
        store = data[i]
        names.append(store['name'])
        ratings.append(store['rating'])
        url.append(store['url'])
        zip.append(store['location']['zip_code'])
        # coordinates
        latitude.append(store['coordinates']['latitude'])
        longitude.append(store['coordinates']['longitude'])
        # categories
        cats = store['categories']
        titles = [single['title'] for single in cats]
        categories.append(", ".join(titles))

        try:
            pricing.append(len(store['price']))
        except:
            pricing.append(None)

        cnt.append(store['review_count'])

    biz = {
        'city': city,
        'source': 'Yelp',
        'name': names,
        'rating': ratings,
        'pricing': pricing,
        'num_reviews': cnt,
        'categories': categories,
        'url': url,
        'latitude': latitude,
        'longitude': longitude,
        'zip': zip
    }

    df_b = pd.DataFrame(biz)
    return df_b


# Data Source 3 : TripAdvisor API

# Helper function that converts price level to numerical values
def convert_price(price):
    if price == '$$$$':
        return 4
    elif (price == '$$$') | (price == '$$ - $$$'):
        return 3
    elif price == '$$':
        return 2
    elif price == '$':
        return 1
    else:
        return None


# Function that gets tripadvisor data, extracts required columns, and outputs a dataframe
def get_tripadvisor_data(city, state, api_key):
    url = (f"https://api.content.tripadvisor.com/api/v1/location/"
           f"search?key={api_key}&"
           f"searchQuery={city}%2C%20{state}&category=restaurants&language=en")

    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    location_details = []

    if response.status_code == 200:
        for item in data['data']:
            location_id = item['location_id']
            details_url = (f"https://api.content.tripadvisor.com/api/v1/"
                           f"location/{location_id}/details?language=en&currency=USD&key={api_key}")
            details_response = requests.get(details_url, headers=headers)

            if details_response.status_code == 200:
                location_details.append(json.loads(details_response.text))
            elif details_response.status_code == 429:
                print(f"Error code {details_response.status_code}: Too many requests, and over daily limit")
            else:
                print(f"Error retrieving details for location {location_id}: {details_response.status_code}")

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(location_details)

    # Extract required column names only
    columns = ['name', 'price_level', 'cuisine', 'num_reviews', 'rating', 'longitude', 'latitude',
               'web_url', 'address_obj']
    # Only select required columns
    selected_df = df[columns].copy()
    # Data Organizing to df
    selected_df['price_level'] = selected_df['price_level'].apply(convert_price)
    selected_df['price_level'] = selected_df['price_level'].astype(int)
    selected_df['cuisine'] = selected_df['cuisine'].apply(lambda x: ', '.join(item['localized_name'] for item in x))
    selected_df['address_obj'] = selected_df['address_obj'].apply(lambda item: item['postalcode'].split('-')[0])
    selected_df['city'] = city
    selected_df['source'] = 'TripAdvisor'
    # Rename column names to structure
    selected_df.columns = ['name', 'pricing', 'categories', 'num_reviews', 'rating', 'longitude',
                           'latitude', 'url', 'zip', 'city', 'source']
    return selected_df


# Data modeling and Saving

# Function to create the initial tables for the database
import sqlite3

def create_tables():
    conn = sqlite3.connect('module2.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS city_data')
    cur.execute("""
         CREATE TABLE city_data (
            cityID INTEGER PRIMARY KEY AUTOINCREMENT,
            zip TEXT,
            description TEXT,
            value REAL,
            city TEXT
        );

    """)

    cur.execute('DROP TABLE IF EXISTS rest_data')
    cur.execute("""
        CREATE TABLE rest_data (
            restID INTEGER PRIMARY KEY AUTOINCREMENT,
            cityID INTEGER,
            source TEXT,
            name TEXT,
            rating REAL,
            pricing TEXT,
            num_reviews INTEGER,
            categories TEXT,
            longitude REAL,
            latitude REAL,
            url TEXT,
            zip TEXT,
            FOREIGN KEY (cityID) REFERENCES city_data(cityID)
        )
    """)

    conn.commit()
    conn.close()

# Function to insert city data, given city df
def insert_city_data(city_df):
    conn = sqlite3.connect('module2.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    # Insert data into city_data table
    for index, row in city_df.iterrows():
        cur.execute("INSERT INTO city_data (city, zip, description, value) VALUES (?, ?, ?, ?)",
                    (row['city'],
                     row['zip'],
                     row['description'],
                     row['value']))

    conn.commit()
    conn.close()

## Function to insert restaurant data, given restaurant df
def insert_rest_data(rest_df):
    conn = sqlite3.connect('module2.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    for index, row in rest_df.iterrows():
        cur.execute("SELECT cityID FROM city_data WHERE city = ?", (row['city'],))
        city_id = cur.fetchone()

        if city_id is None:
            print("Current city does not exist in database, please insert data into city_data table first")
            continue

        city_id = city_id[0]

        cur.execute(
            "INSERT INTO rest_data (cityID, source, name, rating, pricing, num_reviews, categories, longitude, "
            "latitude, url, zip) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (city_id,
             row['source'],
             row['name'],
             row['rating'],
             row['pricing'],
             row['num_reviews'],
             row['categories'],
             row['longitude'],
             row['latitude'],
             row['url'],
             row['zip']))

    conn.commit()
    conn.close()



# ========================= # =========
# Focus City: Seattle
locations = ['Seattle, Washington']
df_city_data = pd.DataFrame()
# SQL tables Initiation
create_tables()

# Counter to count process
tic = time.perf_counter()
# Get data for locations
for location in locations:
    city, state = location.split(", ")
    # Get census data of all zips of city(income and race demographics)
    codes = get_codes(city, state)
    for zipCode in codes:
        df_income = get_city_data('Household-Income', city, zipCode)
        df_demo = get_city_data('Race-and-Ethnicity', city, zipCode)
        # Concatenate income and demographic data for each zip
        df_city_data = pd.concat([df_city_data, df_demo, df_income], ignore_index=True)

    # Get Seattle Data
    df_s_income = get_city_data('Household-Income', city, 'all')
    df_s_demo = get_city_data('Race-and-Ethnicity', city, 'all')
    df_city_data = pd.concat([df_city_data, df_s_demo, df_s_income], ignore_index=True)
    # Get Yelp Data
    yelp_api_key = 'vFlx3BX6S0gT7J5Ph1p8HpNzRzToenYD1rOlaCQHQzKzzAiXnlb8maaPYXWU_ng4r9ygdUdQHEigLtxapVXR_D06GSsNBQmYTX1WQPOh6K791wBWdFv7WpRdKZMZZnYx'
    yelp_response = get_yelp_data(city, 'restaurants', yelp_api_key)
    yelp_data = extract_yelp_data(yelp_response)

    # Get TripAdvisor Data
    ta_api_key = "14A28D3BDDAA403E9FD44A40CFFA7637"
    trip_advisor_data = get_tripadvisor_data(city, state, ta_api_key)

    # Populate SQL Tables
    insert_city_data(df_city_data)
    insert_rest_data(yelp_data)
    insert_rest_data(trip_advisor_data)
    print(f"{location} data has been added to the database.")

toc = time.perf_counter()
print(f"Time taken to scrape, download, and save data: {toc - tic: 0.4f} seconds")
