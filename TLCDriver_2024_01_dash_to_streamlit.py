import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df_tripdata_2024_01 = pd.read_csv("TLCDriver_2024_01_dash.csv")
st.write(df_tripdata_2024_01.head())