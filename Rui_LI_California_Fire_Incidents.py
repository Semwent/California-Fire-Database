'''
Name: Rui Li
Section: CS230 - 1
Dataset: California Fire Incident
URL:
Description:
This project is design to help people attain information about fire incidents that happen in the state of California.

Functionality of thh Program:
The program will have two main functions. First is mapping. User will be presented a map and a sidebar. The map will
display fire incident in a form of dot. The size of dot represent the amount of acres burned. The location of the dot
on the map represent the location of the fire. The sidebar control which month of the year the map is displaying.
To use this function, the program will first ask the user to enter what year they are searching for. Then user will be
able to move the sidebar and choose what time of the year they are searching for.
The second function is  the searching function. To use this function, users are asked to type in the county they are
searching for, then the program will display info about all historic fire incident that happened in this county,
including the name, the time, the location, and the amount of acres burned of the fire incident.

Overview of selected dataset:
In order to fulfill the needs of this project, three selected columns of the original dataset will be used. They are
'AcresBurned', 'Starting Time & Extinguished Time', and 'County & Longitude & latitude'. The map will utlized data from
all selected dataset columns to display info about the location, the size and the time of the fire incident.
Then the searching function will be based on the 'County & Longitude & latitud' to provide information about the spot
that enter by the user.

'''

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import altair as alt


# read data from the csv file
def read_data():
    return pd.read_csv('California_Fire_Incidents.csv')

df = read_data()

def filter_df(choose_county, choose_year):
    df = read_data()
    df = df.loc[df['Counties'].isin(choose_county)]
    df = df.loc[df['ArchiveYear'].isin(choose_year)]

    return df


Area = df['AcresBurned']
counties = df['Counties']
lon = df['Longitude']
lat = df['Latitude']
years = df['ArchiveYear']


# Create a list that contain all the year
year_list = []
for year in years:
    if year not in year_list:
        year_list.append(year)

# Set function for creating list that contain all the counties' names
def county_func():
    county_lst = []
    for county in counties:
            if county not in counties:
                county_lst.append(county)
    return county_lst



# count the sum of fire incidents that happen in each year
def count_year(years, firedata):
    return [firedata.loc[df['ArchiveYear'].isin([year])].shape[0] for year in years]

# count the sum of fire incidents that happen in each county
def count_county(counties, firedata):
    return [firedata.loc[df['Counties'].isin([county])].shape[0] for county in counties]

# let user select whether they want to see data sorted by year or data sorted by county
def data_display(choose_year, choose_county):
    display_type = ['Based on Year', 'Based on County']
    display = st.radio("Choose Data for Fire Incidents", display_type)
    # display data by years
    if display == display_type[0]:
        plt.title("Fire Incidents(Years)")
        x = choose_year
        y = sorted(count_year(choose_year, filter_df(choose_county, choose_year)), reverse = True)
        chart, axis = plt.subplots()
        plt.bar(x,y, color = 'darkorange')
        st.pyplot(chart)
        # display data by counties
    else:
        plt.title("Fire Incidents (Counties)")
        x = choose_county
        y = sorted(count_county(choose_county, filter_df(choose_county, choose_year)), reverse = True)
        chart, axis = plt.subplots()
        plt.xticks(rotation=-90)
        plt.bar(x, y, color='darkorange')
        st.pyplot(chart)



def sidebar():

    # Choose specific year


    choose_county = st.sidebar.multiselect("Select county you are searching for", county_func())
    choose_year = st.sidebar.slider("Please Chooes Year:", 2013, 2019)
    return choose_year, choose_county



def chart(dataset):
    chart_df = dataset.filter(["Name", "Location", "Counties", "AcresBurned", "ArchiveYear"])

    # add filter for displaying info
    info_sort = st.selectbox('Sorted by:', ('Ascending by Acres Burned', 'Descending by Acres Burned'))
    if info_sort == 'Ascending by Acres Burned':
        chart_df = chart_df.sort_values(by='AcresBurned', ascending=True)
        st.text("Fire Incident ascending by acres burned")
        st.dataframe(chart_df)
    elif info_sort == 'Descending by Acres Burned':
        chart_df = chart_df.sort_values(by='AcresBurned', ascending=False)
        st.text("Fire Incident descending by acres burned")
        st.dataframe(chart_df)


# set function to display the map
def mapping(df):
    mapping_df = df.filter(["Name", "Latitude", "Longitude", "Location"])

    California_map = pdk.ViewState(latitude=mapping_df['Latitude'].mean(), longitude=mapping_df['Longitude'].mean(),
                                   zoom=6, pitch=40)
    dot_layer = pdk.Layer('ScatterplotLayer', data=mapping_df, get_position='[Longitude, Latitude]',
                          get_radius=3000, get_color=[200, 80, 80, 175], pickable = True)


    tip = {"html": "Name:<b>{Name}</b> <br/> Location:<br/> <b>{Location}</b>", "style": {"backgroundColor": "white",
                                                                                          "color":"darkorange"}}

    Map = pdk.Deck(initial_view_state=California_map, layers=[dot_layer], tooltip=tip)
    st.pydeck_chart(Map)



# the final output to show all the data
def main():
    st.title("🔥California Fire Incidents🔥")
    st.subheader("This is the California Fire Incidents Database")
    st.image("Fire_Cover.jpeg", width=800)
    st.write(" ")


    st.sidebar.write("Please select filter to display the data you want:")


    choose_county = st.sidebar.multiselect("Select county you are searching for", county_func())
    choose_year = st.sidebar.multiselect("Please Chooes Year:", year_list)



    data = filter_df(choose_county, choose_year)



    if len(choose_county) > 0 and len(choose_year) > 0:
        chart(data)
        st.subheader("Bar Chart For Display the Numbers of Fire Incident")
        st.write(" ")

        data_display(choose_year, choose_county)
        st.write(" ")


        st.subheader("Map for Displaying Locations of Fire Incidents")
        mapping(data)

    else:
        st.write("Search Fire Incidents")
        input = st.text_input(label='Enter County Name')
        search_key = df['Counties'].str.contains(input, na=False)
        st.dataframe(df[search_key])



main()

























