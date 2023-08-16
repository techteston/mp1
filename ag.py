#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#from st_aggrid import AgGrid
# In[4]:

st.set_page_config(page_title='Transport Optimization',page_icon=":tada:",layout="wide")

data_locations = [
    {"City": "London", "Latitude": 51.5074, "Longitude": -0.1278},
    {"City": "Birmingham", "Latitude": 52.4813, "Longitude": -1.9038},
    {"City": "Leeds", "Latitude": 53.7972, "Longitude": -1.5477},
    {"City": "Sheffield", "Latitude": 53.3806, "Longitude": -1.4750},
    {"City": "Bradford", "Latitude": 53.7958, "Longitude": -1.7543},
    {"City": "Liverpool", "Latitude": 53.4098, "Longitude": -2.9703},
    {"City": "Bristol", "Latitude": 51.4511, "Longitude": -2.5893},
    {"City": "Manchester", "Latitude": 53.4348, "Longitude": -2.2379},
    {"City": "Edinburgh", "Latitude": 55.9523, "Longitude": -3.1880},
    {"City": "Glasgow", "Latitude": 55.8626, "Longitude": -4.2677}
]

# Create a dataframe from the list of dictionaries
df_data_locations = pd.DataFrame(data_locations)
df_data_locations
with st.container():
    st.title('Transport Optimization')
    st.write("Optimize the Cost of Transportation to Deliver a Single Product")
    
with st.container():
    dem_col,cap_col,cost_col = st.columns((1,1,1))

    with dem_col:
        st.write("---")
        st.subheader('Demand at Locations')


        demand_data = {
            "Location": ["London","Birmingham","Leeds","Sheffield","Bradford","Liverpool","Bristol","Manchester","Edinburgh","Glasgow"],
            "Month-Year": ["October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23"],
            "Demand": [115,136,105,114,148,105,131,140,135,102]
        }

        # Create a DataFrame
        df_demand_data = pd.DataFrame(demand_data)

        # Pivot the DataFrame
        df_demand_data_pivoted = df_demand_data.pivot(index='Location', columns='Month-Year', values='Demand')

        # Display the pivoted DataFrame
        df_demand_data_pivoted

    with cap_col:
        st.write("---")
        st.subheader('Capacity at Locations')


        capacity_data = {
            "Location": ["London","Leeds","Liverpool","Glasgow"],
            "Month-Year": ["October-23","October-23","October-23","October-23"],
            "Demand": [1361,1423,1015,1106]
        }

        # Create a DataFrame
        df_capacity_data = pd.DataFrame(capacity_data)

        # Pivot the DataFrame
        df_capacity_data_pivoted = df_capacity_data.pivot(index='Location', columns='Month-Year', values='Demand')

        # Display the pivoted DataFrame
        df_capacity_data_pivoted

    with cost_col:
        st.write("---")
        st.subheader('Cost of Transportation')


        cost_data = {
            "Source": ["London","London","London","London","London","London","London","London","London","London","Leeds","Leeds","Leeds","Leeds","Leeds","Leeds","Leeds","Leeds","Leeds","Leeds","Liverpool","Liverpool","Liverpool","Liverpool","Liverpool","Liverpool","Liverpool","Liverpool","Liverpool","Liverpool","Glasgow","Glasgow","Glasgow","Glasgow","Glasgow","Glasgow","Glasgow","Glasgow","Glasgow","Glasgow"],
            "Destination":["London","Birmingham","Leeds","Sheffield","Bradford","Liverpool","Bristol","Manchester","Edinburgh","Glasgow","London","Birmingham","Leeds","Sheffield","Bradford","Liverpool","Bristol","Manchester","Edinburgh","Glasgow","London","Birmingham","Leeds","Sheffield","Bradford","Liverpool","Bristol","Manchester","Edinburgh","Glasgow","London","Birmingham","Leeds","Sheffield","Bradford","Liverpool","Bristol","Manchester","Edinburgh","Glasgow"],
            "Month-Year": ["October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23","October-23"],
            "Cost": [1,17,18,17,18,12,13,20,10,10,10,12,1,12,11,10,12,13,15,17,10,13,20,11,10,1,14,15,13,16,15,18,12,14,12,12,14,17,19,1]
        }

        # Create a DataFrame
        df_cost_data = pd.DataFrame(cost_data)

        # Pivot the DataFrame
        df_cost_data_pivoted = df_cost_data.pivot(index=['Source', 'Destination'], columns='Month-Year', values='Cost')
        # Display the pivoted DataFrame
        df_cost_data_pivoted

#df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
#grid_return = AgGrid(df, editable=True)
#new_df = grid_return['data']

df = pd.DataFrame(
    [
       {"command": "st.selectbox", "rating": 4, "is_widget": True},
       {"command": "st.balloons", "rating": 5, "is_widget": False},
       {"command": "st.time_input", "rating": 3, "is_widget": True},
   ]
)
edited_df = st.data_editor(df, num_rows="dynamic")

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

df2 = edited_df.copy()
df2


# st.write("---")


        

        


    
