import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("TLCDriver_2024_01_dash.csv")
heatmap_data = pd.DataFrame(df)

# Streamlit app title
st.title("Driver Pay Heatmap by Weekday and Hour")

# Dropdown for weekday selection
selected_weekday = st.selectbox(
    "Select a Weekday",
    options=heatmap_data['weekday'].unique(),
    index=0
)

# Filter data for the selected weekday
weekday_data = heatmap_data[heatmap_data['weekday'] == selected_weekday]

# Create pivot table for the heatmap
heatmap_pivot = weekday_data.pivot(index='Zone', columns='hour', values='driver_pay')

