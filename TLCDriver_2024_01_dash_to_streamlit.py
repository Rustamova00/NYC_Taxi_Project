import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit.runtime.scriptrunner import add_script_run_ctx,get_script_run_ctx
from subprocess import Popen

ctx = get_script_run_ctx()
##Some code##
process = Popen(['python','my_script.py'])
add_script_run_ctx(process,ctx)
#import numpy as np
 #importing data
df = pd.read_csv("TLCDriver_2024_01_dash.csv")
df_tripdata_2024_01 = pd.DataFrame(df)

#st.write(df_tripdata_2024_01.head())
#User Selecting a weekday to focus on
st.subheader("Select Weekday")
weekdays= df_tripdata_2024_01["weekday"].unique().tolist()
#selected weekday dataframe
selected_weekday= st.selectbox("Select Weekday to filter by", weekdays)
unique_values = df_tripdata_2024_01[df_tripdata_2024_01['weekday'] == selected_weekday]['weekday'].unique()
filtered_df = df_tripdata_2024_01[df_tripdata_2024_01['weekday'] == selected_weekday]
 

# Create heatmap using Plotly Express
fig = px.scatter(
    filtered_df,
    x="hour",
    y="Zone",
    color="driver_pay",
    color_continuous_scale="blues",
)
st.plotly_chart(fig, theme="streamlit", use_container_width=False,selection_mode=('box'),size=100)
