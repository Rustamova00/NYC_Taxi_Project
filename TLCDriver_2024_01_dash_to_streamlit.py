import streamlit as st
import pandas as pd
import plotly.express as px

df_01_2024 = pd.read_csv("TLCDriver_2024_01_dash.csv")
df_02_2024 = pd.read_csv("TLCDriver_2024_02_heatmap_df.csv")
month_df= ["df_01_2024","df_02_2024"]

# Dropdown for month weekday selection
selected_month = st.selectbox(
    "Select a Month",
    options=month_df.unique(),
    index=0
)
heatmap_data = pd.DataFrame(selected_month)

# Streamlit app title
st.title("Driver Pay Heatmap by Weekday and Hour")

# Dropdown for weekday selection
selected_weekday = st.selectbox(
    "Select a Weekday",
    options=heatmap_data['weekday'].unique(),
    index=0
)


# Filter data for the selected weekday
weekday_data = heatmap_data[heatmap_data['weekday'] == selected_weekday ]

# Create pivot table for the heatmap
heatmap_pivot = weekday_data.pivot(index='Zone', columns='hour', values='driver_pay')
# Check if data exists for the selected weekday
if heatmap_pivot.empty:
    st.warning(f"No data available for {selected_weekday}.")
else:
    # Plot the heatmap
    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Hour", y="Zone", color="Total Driver Pay"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale='reds'
    )

    # Customize layout
    fig.update_layout(
        title=f"Total Driver Pay for Top 10 Zones on {selected_weekday}",
        xaxis_title="Hour of Day",
        yaxis_title="Zone",
        coloraxis_colorbar=dict(title="Total Pay ($)"),
        autosize=True
        
    )
    

    # Display the heatmap in Streamlit
st.plotly_chart(fig,use_container_width=True, hight=800)
