#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pulp import *
#import numpy as np
#import matplotlib.pyplot as plt
#from st_aggrid import AgGrid

st.set_page_config(page_title='Transport Optimization',page_icon=":tada:",layout="wide")

def get_lat_lon(fd_data,fv_location):

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
    
    df_data_locations = pd.DataFrame(data_locations)
    
    df_lat_long = pd.merge(fd_data,df_data_locations,left_on=fv_location,right_on="Location",how="left")
    
    return(df_lat_long)

def create_nodes(fd_data,fv_value_name,fv_value,fv_location,fv_color):
    nodes_trace = go.Scattermapbox(
        lat=fd_data['Latitude'],
        lon=fd_data['Longitude'],
        mode='markers',
        marker=dict(
            size=fd_data[fv_value]/50,
            color=fv_color,  # Circle color
            opacity=0.7,
        ),
        text=fv_value_name+" at " + fd_data[fv_location] + ": " + fd_data[fv_value].astype(str),
    )
    return(nodes_trace)

def create_edges(fd_data,fv_src,fv_src_lat,fv_srv_lon,fv_des,fv_des_lat,fv_des_lon,fv_value,fv_value_name,fv_color):

    edges_trace = []
    for index, row in fd_data.iterrows():
        source = (row[fv_src_lat], row[fv_srv_lon])
        destination = (row[fv_des_lat], row[fv_des_lon])
        hover_text = f"Source: {row[fv_src]}\nDestination: {row[fv_des]}\{fv_value_name}: {row[fv_value]}"
        edges_trace.append(go.Scattermapbox(
            lat=[source[0], destination[0]],
            lon=[source[1], destination[1]],
            mode='lines',
            line=dict(width=row[fv_value]/50, color=fv_color),  # Line width and color
            hoverinfo='text',  # Show custom hover text
            hovertext=hover_text,
        ))

    return(edges_trace)

with st.container():
    st.title('Transport Optimization')
    st.write("Optimize the Cost of Transportation to Deliver a Single Product")

with st.container():
    dem_col,cap_col,cost_col = st.columns((1,1,2))

    with dem_col:
        st.write("---")
        st.subheader('Demand at Locations')
        
        demand_data = {
            "Location": ["London","Birmingham","Leeds"],
            "Month-Year": ["October-23","October-23","October-23"],
            "Demand": [100,200,300]
        }
        
        df_demand_data = pd.DataFrame(demand_data)
        df_demand_data_pivoted = df_demand_data.pivot(index='Location', columns='Month-Year', values='Demand')
        df_demand_data_pivoted
        df_demand_location = get_lat_lon(df_demand_data,"Location")
        df_demand_data_pivoted.reset_index(inplace=True)
# Unpivot the DataFrame
        #df_demand_data_unpivoted = pd.melt(df_demand_data_pivoted, id_vars='Location', var_name='Month-Year', value_name='Demand')
        #df_demand_data_unpivoted        
        df_demand_nodes = create_nodes(df_demand_location,"Demand","Demand","Location","Blue")
        
    with cap_col:
        st.write("---")
        st.subheader('Capacity at Locations')


        capacity_data = {
            "Location": ["London","Glasgow"],
            "Month-Year": ["October-23","October-23"],
            "Capacity": [1000,1000]
        }
        df_capacity_data = pd.DataFrame(capacity_data)
        df_capacity_data_pivoted = df_capacity_data.pivot(index='Location', columns='Month-Year', values='Capacity')
        df_capacity_data_pivoted
        df_capacity_location = get_lat_lon(df_capacity_data,"Location")
        df_capacity_nodes = create_nodes(df_capacity_location,"Capacity","Capacity","Location","Green")        


    with cost_col:
        st.write("---")
        st.subheader('Cost of Transportation')


        cost_data = {
            "Source": ["London","London","London","Glasgow","Glasgow","Glasgow"],
            "Destination":["London","Birmingham","Leeds","London","Birmingham","Leeds"],
            "Month-Year": ["October-23","October-23","October-23","October-23","October-23","October-23"],
            "Cost": [300,100,200,10,20,30]}

        df_cost_data = pd.DataFrame(cost_data)
        df_cost_data_pivoted = df_cost_data.pivot(index=['Source', 'Destination'], columns='Month-Year', values='Cost')
        df_cost_data_pivoted
        df_cost_location = get_lat_lon(df_cost_data,"Source")
        df_cost_location = get_lat_lon(df_cost_location,"Destination")
        df_cost_location.rename(columns={"Latitude_x":"Source_Latitude","Longitude_x":"Source_Longitude","Latitude_y":"Destination_Latitude","Longitude_y":"Destination_Longitude"},inplace="True")
        dt_edges = create_edges(df_cost_location,"Source","Source_Latitude","Source_Longitude",
                        "Destination","Destination_Latitude","Destination_Longitude","Cost","Cost","Red")


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
fig = go.Figure(data=[df_demand_nodes, df_capacity_nodes], layout=layout)

# Streamlit app
st.subheader('Current Demand and Capacity')
st.caption("The Demand and Capacity at each location is noted.")
fig.update_layout(height=600)
st.plotly_chart(fig,height=600)


if st.button('Show Optimal Solution'):

#    df_capacity_data_pivoted
    df_capacity_data_pivoted.reset_index(inplace=True)
    new_row = [1000000] * len(df_capacity_data_pivoted.columns)
    df_capacity_data_pivoted.loc[len(df_capacity_data_pivoted)] = new_row
    df_capacity_data_pivoted["Location"][len(df_capacity_data_pivoted)-1] = "Shortage"
#    df_capacity_data_pivoted

    df_cost_data = pd.DataFrame(cost_data)
    df_cost_data_pivoted = df_cost_data.pivot(index=['Source'], columns='Destination', values='Cost')
#    df_cost_data_pivoted
    df_cost_data_pivoted.reset_index(inplace=True)
#    df_cost_data_pivoted
    new_row = [1000000] * len(df_cost_data_pivoted.columns)
    df_cost_data_pivoted.loc[len(df_cost_data_pivoted)] = new_row
    df_cost_data_pivoted["Source"][len(df_cost_data_pivoted)-1] = "Shortage"
#    df_cost_data_pivoted

    # number of origins and destinations
    n_plants = df_capacity_data_pivoted.shape[0]
    print(n_plants)
    n_dest = df_demand_data_pivoted.shape[0]
    print(n_dest)

    # cost of shipping from plant i to destination j 
    cost_matrix = np.array(df_cost_data_pivoted)[0:n_plants,1:(n_dest+1)]
    print(cost_matrix)

    number = 0
    for month in range(1,df_demand_data_pivoted.shape[1]):
        number = number + 1
        
        # demand of demand points in each month
        demand = np.array(df_demand_data_pivoted[df_demand_data_pivoted.columns[month]])

        # supply of supply points in each month
        supply = np.array(df_capacity_data_pivoted[df_capacity_data_pivoted.columns[month]])
        
        # initialise LP model
        model = LpProblem("Disguised"+df_capacity_data_pivoted.columns[month], LpMinimize)
        
            # create variable names from plant i send product j
        variable_names = [str(i)+"_"+str(j) for i in range(1,n_plants+1) for j in range(1, n_dest+1)]
        
        # decision variables
        dec_var = LpVariable.matrix("X", variable_names, cat = "Continuous", lowBound = 0)
        
        # shape the decision variables into 10 by 25 matrix (10 supply locations, 25 destinations)
        allocation = np.array(dec_var).reshape(n_plants,n_dest)
        
        # objective function
        obj_fun = lpSum(allocation * cost_matrix)
        
        # add objective function to the model
        model += obj_fun
        
        # add supply constraints
        for i in range(n_plants): 
            model += lpSum(allocation[i][j] for j in range(n_dest)) <= supply[i]
            
        # add demand constraints
        for j in range(n_dest):
            model += lpSum(allocation[i][j] for i in range(n_plants)) >= demand[j]
                    
        # write model to file
        model.writeLP("Disguised"+str(number)+df_capacity_data_pivoted.columns[month]+".lp")
            
        # solve the model
        model.solve()
                
        # Decision Variables
        solutionnames = [] #initialise vectors to keep decision variables
        solutionvalues = [] #initialise vectors to keep the values of the decision variables
        
        for v in model.variables():
            try:
                solutionnames.append(v.name)
                solutionvalues.append(v.value())
            except:
                print("error couldnt find value")
        
        d = {"Var": solutionnames, "Value": solutionvalues}
        dfsol = pd.DataFrame(data = d)
        
        costcoef = []
        for i in range(dfsol.shape[0]):
            index1 = [int(s) for s in solutionnames[i].split("_") if s.isdigit()]
            res = np.array(index1)-[1, 1]
            costcoef.append(cost_matrix[res[0], res[1]])
        
        dfsol['Cost'] = costcoef
        
        manualcalculation = sum(dfsol['Value'] * costcoef)
    print(manualcalculation)

    split_values = dfsol['Var'].str.split('_', expand=True)
    dfsol['SRC'] = split_values[1]
    dfsol['DES'] = split_values[2]

    dfsol["SRC"] = dfsol["SRC"].astype(int) - 1
    dfsol["DES"] = dfsol["DES"].astype(int) - 1

    dfsol['Source'] = dfsol['SRC'].map(df_capacity_data_pivoted['Location'])
    dfsol['Destination'] = dfsol['DES'].map(df_demand_data_pivoted['Location'])
    
    
    dfsol = dfsol[~(dfsol['Source'] == 'Shortage')]
    df_sol_location = get_lat_lon(dfsol,"Source")
    df_sol_location = get_lat_lon(df_sol_location,"Destination")
    df_sol_location.rename(columns={"Latitude_x":"Source_Latitude","Longitude_x":"Source_Longitude",
                                    "Latitude_y":"Destination_Latitude","Longitude_y":"Destination_Longitude"}
                                    ,inplace="True")
    dt_edges = create_edges(df_sol_location,"Source","Source_Latitude","Source_Longitude",
                        "Destination","Destination_Latitude","Destination_Longitude","Value","Value","Red")
    
    # Create the figure
    fig2 = go.Figure(data=[df_demand_nodes,*dt_edges], layout=layout)

    # Streamlit app
    st.subheader('Optimized Solution')
    st.caption("The Optimal Solution shows the optimal quantity of product to be delivered from Source to Destination")
    fig2.update_layout(height=600)
    st.plotly_chart(fig2, width=800,height=600)

else:
    st.write('')