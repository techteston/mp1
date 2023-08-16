#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
#import numpy as np
#import matplotlib.pyplot as plt
#from st_aggrid import AgGrid
# In[4]:

st.set_page_config(page_title='Transport Optimization',page_icon=":tada:",layout="wide")

data_locations = [
    {"Location": "London", "Latitude": 51.5074, "Longitude": -0.1278},
    {"Location": "Birmingham", "Latitude": 52.4813, "Longitude": -1.9038},
    {"Location": "Leeds", "Latitude": 53.7972, "Longitude": -1.5477},
    {"Location": "Sheffield", "Latitude": 53.3806, "Longitude": -1.4750},
    {"Location": "Bradford", "Latitude": 53.7958, "Longitude": -1.7543},
    {"Location": "Liverpool", "Latitude": 53.4098, "Longitude": -2.9703},
    {"Location": "Bristol", "Latitude": 51.4511, "Longitude": -2.5893},
    {"Location": "Manchester", "Latitude": 53.4348, "Longitude": -2.2379},
    {"Location": "Edinburgh", "Latitude": 55.9523, "Longitude": -3.1880},
    {"Location": "Glasgow", "Latitude": 55.8626, "Longitude": -4.2677}
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

        df_demand_location = pd.merge(df_demand_data,df_data_locations,on="Location",how="left")

        df_demand_location

    with cap_col:
        st.write("---")
        st.subheader('Capacity at Locations')


        capacity_data = {
            "Location": ["London","Leeds","Liverpool","Glasgow"],
            "Month-Year": ["October-23","October-23","October-23","October-23"],
            "Capacity": [1361,1423,1015,1106]
        }

        # Create a DataFrame
        df_capacity_data = pd.DataFrame(capacity_data)

        # Pivot the DataFrame
        df_capacity_data_pivoted = df_capacity_data.pivot(index='Location', columns='Month-Year', values='Capacity')

        # Display the pivoted DataFrame
        df_capacity_data_pivoted

        df_capacity_location = pd.merge(df_capacity_data,df_data_locations,on="Location",how="left")

        df_capacity_location

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

        df_cost_location = pd.merge(df_cost_data,df_data_locations,left_on="Source",right_on="Location",how="left")
        df_cost_location = pd.merge(df_cost_location,df_data_locations,left_on="Destination",right_on="Location",how="left")

        df_cost_location.rename(columns={"Latitude_x":"Source_Latitude","Longitude_x":"Source_Longitude","Latitude_y":"Destination_Latitude","Longitude_y":"Destination_Longitude"},inplace="True")
        df_cost_location

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



dem_nodes_trace = go.Scattermapbox(
    lat=df_demand_location['Latitude'],
    lon=df_demand_location['Longitude'],
    mode='markers',
    marker=dict(
        size=df_demand_location['Demand']/10,
        color='blue',  # Circle color
        opacity=0.7,
    ),
    text= "Demand at " + df_demand_location['Location'] + " " + df_demand_location['Demand'].astype(str),
)

# Create a scattermapbox trace for CapQuantity nodes
cap_nodes_trace = go.Scattermapbox(
    lat=df_capacity_location['Latitude'],
    lon=df_capacity_location['Longitude'],
    mode='markers',
    marker=dict(
        size=df_capacity_location['Capacity']/100,
        color='green',  # Circle color
        opacity=0.7,
    ),
    text="Capacity at " + df_capacity_location['Location'] + " " + df_capacity_location['Capacity'].astype(str),
)


trav_edges_trace = []
for index, row in df_cost_location.iterrows():
    source = (row['Source_Latitude'], row['Source_Longitude'])
    destination = (row['Destination_Latitude'], row['Destination_Longitude'])
    trav_edges_trace.append(go.Scattermapbox(
        lat=[source[0], destination[0]],
        lon=[source[1], destination[1]],
        mode='lines',
        line=dict(width=row['Cost']/10, color='red'),  # Line width and color
        hoverinfo='none',
    ))

# Create the map layout
layout = go.Layout(
    mapbox=dict(
        center=dict(lat=df_demand_location['Latitude'].mean(), lon=df_demand_location['Longitude'].mean()),
        zoom=3,
        style='open-street-map',
    ),
    showlegend=False,
)

# Create the figure
fig = go.Figure(data=[dem_nodes_trace, cap_nodes_trace, *trav_edges_trace], layout=layout)

# Streamlit app
st.title('Data Visualization with Plotly in Streamlit')
st.plotly_chart(fig, use_container_width=True, width=600, height=2400)




        

        


    
