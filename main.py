# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import time

# Setting up page configuration
# icon = Image.open("ICN.png")
page_icon_url = 'https://raw.githubusercontent.com/gopiashokan/Airbnb-Analysis/main/airbnb_logo.png'
st.set_page_config(page_title="Airbnb Data Visualization ",
                   page_icon=page_icon_url,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# Data has been gathered from mongodb atlas for the dasboard
                                        """}
                   )

# Creating option menu in the side bar
selected = option_menu(options=["Home", "Overview", "Explore"],
                       icons=["house", "graph-up-arrow", "bar-chart-line"],
                       menu_title=None,
                       menu_icon="cast",
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                       )

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient(
    "mongodb+srv://prithivin22:Mongodb2@cluster0.nqcbt0t.mongodb.net/")
db = client.sample_airbnb
col = db.listingsAndReviews

# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    # Title Image
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.markdown(
        "## :blue[Domain] : Travel Industry, Property Management and Tourism")
    col2.markdown(
        "## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    col3.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    col2.markdown("#   ")
    col2.markdown("#   ")
    # col2.image("home.jpg")

# OVERVIEW PAGE
if selected == "Overview":
    tab1, tab2 = st.tabs(["$\huge 📝 RAW DATA $", "$\huge🚀 INSIGHTS $"])

    # RAW DATA TAB
    with tab1:
        # RAW DATA
        col1, col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            col1.write(col.find_one())
        # DATAFRAME FORMAT
        if col2.button("Click to view Dataframe"):
            col1.write(col.find_one())
            col2.write(df)

    # INSIGHTS TAB
    with tab2:
        # GETTING USER INPUTS
        country = st.multiselect(label='Select a Country', options=sorted(
            df.country.unique()), placeholder="Select Country")
        prop = st.multiselect(label='Select Property_type', options=sorted(
            df.property_type.unique()), placeholder="Select Property_type")
        room = st.multiselect(label='Select Room_type', options=sorted(
            df.room_type.unique()), placeholder="Select Room_type")
        price = st.slider('Select Price', df.price.min(),
                          df.price.max(), (df.price.min(), df.price.max()))

        # CONVERTING THE USER INPUT INTO QUERY
        query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

        # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')

        with col1:

            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["property_type"]).size().reset_index(
                name="listings").sort_values(by='listings', ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='listings',
                         y='property_type',
                         orientation='h',
                         color='property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["host_name"]).size().reset_index(
                name="listings").sort_values(by='listings', ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='listings',
                         y='host_name',
                         orientation='h',
                         color='host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:

            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(
                ["room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                         )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig, use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['country'], as_index=False)[
                'name'].count().rename(columns={'name': 'total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='country',
                                locationmode='country names',
                                color='total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                                )
            st.plotly_chart(fig, use_container_width=True)

# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")

    # GETTING USER INPUTS
    country = st.multiselect(label='Select a country',
                             options=sorted(df.country.unique()), placeholder="Select country")
    prop = st.multiselect(label='Select property_type', options=sorted(
        df.property_type.unique()), placeholder="Select property_type")
    room = st.multiselect(label='Select room_type', options=sorted(
        df.room_type.unique()), placeholder="Select room_type")
    price = st.slider(label='Select price', min_value=df.price.min(),
                      max_value=df.price.max(), value=(df.price.min(), df.price.max()))

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

    # HEADING 1
    st.markdown("## Price Analysis")

    # CREATING COLUMNS
    col1, col2 = st.columns(2, gap='medium')

    with col1:

        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('room_type', as_index=False)[
            'price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

        # HEADING 2
        st.markdown("## Availability Analysis")

        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                     title='Availability by Room_type'
                     )
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby(
            'country', as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                             locations='country',
                                       color='price',
                             hover_data=['price'],
                             locationmode='country names',
                             size='price',
                             title='Avg Price in each Country',
                             color_continuous_scale='agsunset'
                             )
        col2.plotly_chart(fig, use_container_width=True)

        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('country', as_index=False)[
            'availability_365'].mean()
        country_df.Availability_365 = country_df.availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                             locations='country',
                                       color='availability_365',
                             hover_data=['availability_365'],
                             locationmode='country names',
                             size='availability_365',
                             title='Avg Availability in each Country',
                             color_continuous_scale='agsunset'
                             )
        st.plotly_chart(fig, use_container_width=True)