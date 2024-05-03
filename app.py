import pandas as pd
import streamlit as st
import plotly.express as px
import json
import sqlite3

st.set_page_config(layout="wide")
tab1, tab2, tab3, tab4 = st.tabs(["Main Project Page", "Questions", "Data Sources", "Visualizations"])

# Tab 1: Main Page
with tab1:
    st.header("Main Project Page")
    multi = '''Project By: Angel Su
   '''
    st.markdown(multi)
    #Q2-Q3 Responses
    st.markdown("The “zip” drop-down menu allows you to select a specific zip code within the Seattle area. Or, you can select “all” to view comprehensive demographic and restaurant data for the entire Seattle area.")
    st.divider()
    st.markdown("**How to use the webapp?**")
    multi = '''
    1. *Heatmap:* The heatmap is a geographic representation that visualizes the income distribution across the selected zip codes in the Seattle area. On the color spectrum, a darker blue will signify a lower-income zip code area, while a lighter blue and white will signify a higher-income zip code area.  
    2. *Stacked Bar Chart:* This horizontal stacked bar is segmented into multiple sections representing the various ethnic groups in the selected area. In the Seattle area, the majority of the population is white, making up more than half of the population, foll is a geographic representation that visualizes the income distribution across the selected zip codes in the Seattle area. On the color spectrum, a darker blue will signify a lower-income zip code area, while a lighter blue and white will signify a higher-income zip code area.  owed by the Asian population as the second largest group.   
    3. *Bar Graph:* The bar graph showcases the culinary landscape of the Seattle area by depicting the distribution of cuisine types. It shows the “Most Occured Types of Cuisines in Seattle”. In the Seattle area, the top 3 most popular cuisines are Cocktail Bars, New American, and Breakfast & Brunch, in that order.   
    4. *Table:* The two tables display the restaurants with relevant details including restaurant name, rating, pricing, number of reviews, categories (cuisine type), url, and zip code.'''
    st.markdown(multi)
    st.markdown("**Major gotchas**")
    multi = '''
    1. Web scrapping can sometimes be really slow. I also had to change websites to scrap between Milestones 2 and 3 because I realized that the government website has seemingly blocked access.  
    2. The data normalization could possibly be improved for even better data efficiency. Even though we only use two tables, dividing more and defining better relationships could allow data to be more normalized and robust to future changes.
    '''
    st.markdown(multi)

# Tab 2: Q4-8
with tab2:
    st.header("Questions")
    st.markdown("**What did you set out to study?**")
    multi = '''Through this research project, I aim to provide a more complete profile of the dining scene in the selected zip codes of Seattle. The location data will be combined with the restaurant information and demographic dataset. The project seeks to establish correlations between restaurant and demographical information to shed light on how factors such as cuisine types, household income, and restaurant price ranges relate. For instance, I will look into whether the demographics of a selected zip code area may be related to a certain type of cuisine’s popularity in the area. Or, we will look at how the demographic of a selected zip code area can define a pattern in the price range of cuisines in that area. Ultimately, the goal is to create a more comprehensive view of the restaurant culture of the selected zip code area, allowing the users to make informed decisions about where to dine.'''
    st.markdown(multi)
    st.markdown("**What did you discover / What were your conclusions?**")
    multi = '''
    *Household Income and Cuisine Types*  
    The zip code 98112 is the highest household income area. Breakfast & Brunch, New American, and Bars are the most popular cuisine types in this area. From the zip codes with a lower household income such as 98134 or 98108, there is a difference in the popularity of cuisine types. Burgers, sandwiches, and Mexican food are some of the popular options in these areas. These options tend to be more budget-friendly, which can be correlated to the lower household income in that area.  
    
    *Race/Ethnicity and Cuisine Types*  
    Throughout the visualizations, it also reveals how certain areas - such as Downtown Seattle (98101, 98134), being a larger tourist attraction and cultural hub, provide a wider range of options despite the local race/ethnicity or income. In other words, race&ethnicity and income are not the sole reasons that could determine the cuisine type. Similarly, in 98105, where the University of Washington is located, the cuisine types span a wider range of Asian, Indian, Mediterranean, and Mexican. This could be because a higher amount of student diversity results in a broader range of cuisines. However, in areas such as zip code 98104 where Chinatown is located, we can see that there is a relatively higher number of Cantonese restaurants in that area, which can be reflected through the Asian (Chinese) population in that area. These interpretations reveal the complex relationships of demographics, economics, and cultural dynamics that come into play in the cities that we live in today.
    '''
    st.markdown(multi)
    st.markdown("**What difficulties did you have in completing the project?**")
    multi = '''Being able to align project intentions and research intentions with code was challenging. For example, given the API, I had to slowly decipher the output and only take the information that I needed. For web scrapping, I had to also look through longer lines of HTML code to find the best way to extract data. For the most part, the difficulty of the project lied within data cleaning and organizing to fit our proposed database structure. Ensuring each data type, column, and informatino was challenging and time consuming. Converting it and reading the information into streamlit, thus was much faster and required less time.'''
    st.markdown(multi)
    st.markdown("**What skills did you wish you had while you were doing the project?**")
    multi = '''I wish I had stronger skills in data extraction and manipulation. Specifically, this included understanding the API output, being able to debug error codes, and lastly, being able to write robust code that covered certain, specific cases (i.e. what if the data scrapped had different numbers of columns, different columns for each zip code).  
    Being able to quickly think of test cases benefitted this project immensely, as it saved a lot of time debugging and figuring out what was wrong with the code or data.'''
    st.markdown(multi)
    st.markdown("**What would you do next to expand or argument the project?**")
    multi = '''There are several considerations I can take on to enhance this project. First, I could expand the geographic scope of my project beyond the selected zip codes of Seattle, allowing a broader use base. Additionally, I could implement a recommendation engine, which can recommend the most relevant restaurant based on the user’s selections, such as zip code area, price range, cuisine type, and reviews.'''
    st.markdown(multi)

# Tab 3: Data Sources
with tab3:
    st.header("Data Sources")
    st.markdown("**Data Source 1: The Demographic Statistical Atlas of the United States**")
    multi = '''Overview: https://statisticalatlas.com/place/Washington/Seattle/Overview  
    Race and Ethnicity in Seattle, Washington: https://statisticalatlas.com/place/Washington/Seattle/Race-and-Ethnicity  
    Household Income in Seattle, Washington: https://statisticalatlas.com/place/Washington/Seattle/Household-Income  
    The data/API contains statistics for all states and counties of the United States. These statistics include demographic information such as household income and race and ethnicity by neighborhood.'''
    st.markdown(multi)
    st.markdown("**Data Source 2: TripAdvisor**")
    multi = '''Location Reviews API: https://tripadvisor-content-api.readme.io/reference/getlocationreviews   
    The data/API (Location Reviews API) contains details, photos, reviews, search, and nearby location search of locations. The Location Reviews request returns up to 5 of the most recent reviews for a specific location. The API also allows us to search and collect x amount of reviews and details on each location. This could range from around fifty to potentially hundreds, depending on what is provided and available in the provided database and service.'''
    st.markdown(multi)
    st.markdown("**Data Source 3: Yelp**")
    multi = '''Yelp Fusion API: https://docs.developer.yelp.com/docs/fusion-intro  
    The data/API (Yelp Fusion API) contains the local content and user reviews from millions of businesses around the world. This includes reviews (up to 3 review excerpts for a business), business details, and category search. The API also allows us to search and collect x amount of reviews and details on each location. This could range from around fifty to potentially hundreds, depending on what is provided and available in the provided database and service.'''
    st.markdown(multi)

# Visualization Code
# get db data using python code
def get_rest_data(source):
    conn = sqlite3.connect('module2.db')
    cur = conn.cursor()
    ## code here
    df = pd.read_sql_query(f""" 
      SELECT name, rating, pricing, num_reviews, categories, url, zip FROM
      rest_data WHERE
      source = '{source}'
   """, conn)
    ####
    cur.close()
    conn.commit()
    conn.close()
    return df


def get_city_data(city):
    conn = sqlite3.connect('module2.db')
    df = pd.read_sql_query(f"""
      SELECT zip, description, value FROM
      city_data WHERE city = '{city}'
   """, conn)
    conn.commit()
    conn.close()
    return df


# bar chart
def plot_bar(df, zip):
    ## if not all data, then just get categories
    if zip != 'all':
        df = df.loc[
            df['zip'] == zip
            ]
    # Split the 'categories' column by comma and stack them into separate rows
    categories = df['categories'].str.split(', ').explode()

    # Count the occurrences of each category
    category_counts = categories.value_counts().sort_values(ascending=False)
    return category_counts

# Function to get second selection to show user selection of zip code on map
def get_highlights(selections, geojson, lookup):
    geojson_highlights = dict()
    print(selections)
    for k in geojson.keys():
        if k != 'features':
            geojson_highlights[k] = geojson[k]
        else:
            geojson_highlights[k] = [lookup[selection] for selection in selections]
    return geojson_highlights

# Function to plot the map, according to selection
def plot_map(df, zip):
    geojson_file_path = "zip-codes.geojson"
    with open(geojson_file_path) as f:
        geojson_data = json.load(f)

    # Plotting with Plotly Express
    fig = px.choropleth_mapbox(df,
                               geojson=geojson_data,
                               featureidkey='properties.ZCTA5CE10',
                               locations='zip',
                               color='value',
                               mapbox_style="carto-positron",
                               opacity=0.4,
                               zoom=9, center={"lat": 47.6062, "lon": -122.3321},
                               labels={'color': 'Zip Code'})

    if zip != 'all':
        # get all zipcodes
        zipcode_lookup = {
            feature['properties']['ZCTA5CE10']: feature for feature in geojson_data['features']
        }
        # get just highlights
        highlights = get_highlights([zip], geojson_data, zipcode_lookup)
        fig.add_trace(
            px.choropleth_mapbox(df, geojson=highlights,
                                 color='value',
                                 locations='zip',
                                 featureidkey="properties.ZCTA5CE10",
                                 opacity=1).data[0]
        )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

# Function to plot the stacked bar plot
def plot_stacked_bar_plot(df):
    # filter the data by just the demograhic description
    df = df.loc[
        (df['description'] == 'White') |
        (df['description'] == 'Hispanic') |
        (df['description'] == 'Black') |
        (df['description'] == 'Asian') |
        (df['description'] == 'Mixed') |
        (df['description'] == 'Other')
        ]
    fig = px.bar(df, y='zip', x='value', color='description', orientation='h',
                 text='description'
                 )
    fig.update_traces(textposition='inside')
    # don't show any gridlines for design purposes
    fig.update_layout(
        showlegend=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=200
    )
    return fig

# filter dataframe by zipcode, if not label: 'all'
def filter_by_zip(df, zip):
    return df.loc[df['zip'] == zip] if zip != 'all' else df


# Get data from DB
df_rest_seattle_yelp = get_rest_data("Yelp")
df_rest_seattle_trip = get_rest_data("TripAdvisor")
df_location_data = get_city_data("Seattle")
filters = {
    "zip": "all"
}
# Tab 4: Main App (visualizations)
with tab4:
    # make map of city statistics and income
    map_c1, map_c2 = st.columns([3, 2])
    # Location/Demographics data
    map_c2.subheader("Demographics & Income")
    last_index = len(df_location_data['zip'].unique()) - 1
    # get unique list of postal codes
    zip_selection = map_c2.selectbox("Zip", options=df_location_data['zip'].unique(),
                                     index=last_index,
                                     placeholder="Select a zip code...")

    map_fig = plot_map(df_location_data.loc[
                           df_location_data["description"] == 'Median'
                           ], zip_selection)
    map_c1.plotly_chart(map_fig, use_container_width=True)

    # get filtered dataframe by zipcode/or all
    filters["zip"] = zip_selection
    filter_zip = df_location_data.loc[
        df_location_data['zip'] == filters["zip"]
        ]

    # stacked bar plot
    race_plot = plot_stacked_bar_plot(filter_zip)
    map_c2.plotly_chart(race_plot, use_container_width=True)

    # income dataframe
    income_df = filter_zip[filter_zip['description'].str.contains('median|percentile', case=False)]
    income_pivot = income_df.pivot(index='zip', columns='description', values='value')
    map_c2.dataframe(income_pivot, hide_index=True, use_container_width=True)
    map_c2.markdown("**\*value of demographic data in percentages, income in USD*")

    # bar plot
    header_cuisine = zip_selection if zip_selection != 'all' else 'Seattle'
    st.subheader(f"Most Occurred Types of Cuisines in {header_cuisine}")
    bar_plot = plot_bar(df_rest_seattle_yelp, zip_selection)
    st.bar_chart(bar_plot)

    col1, col2 = st.columns(2)
    # Yelp Data
    col1.subheader("Yelp, Featured Restaurants")
    #  filter by zip code in yelp data
    df_z_yelp = filter_by_zip(df_rest_seattle_yelp, zip_selection)
    col1.dataframe(df_z_yelp,
                   hide_index=True,
                   use_container_width=True,
                   column_config={
                       "url": st.column_config.LinkColumn("url")
                   })


    col2.subheader("TripAdvisor, Featured Restaurants")
    # filter by zip code in tripadvisor data
    df_z_ta = filter_by_zip(df_rest_seattle_trip, zip_selection)
    col2.dataframe(df_z_ta,
                   hide_index=True,
                   use_container_width=True,
                   column_config={
                       "url": st.column_config.LinkColumn("url")
                   })
