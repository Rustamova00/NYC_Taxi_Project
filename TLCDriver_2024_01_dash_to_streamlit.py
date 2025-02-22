import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df_01_2024 = pd.read_csv("TLCDriver_2024_01_heatmap_df.csv")
df_02_2024 = pd.read_csv("TLCDriver_2024_02_heatmap_df.csv")

# Dictionary to map months to DataFrames
month_options = {
    "January 2024": df_01_2024,
    "February 2024": df_02_2024
}

# Streamlit app title
st.title("Driver Pay Heatmap by Weekday, Week Number, and Hour")

# Dropdown for month selection
selected_month_label = st.selectbox(
    "Select a Month",
    options=list(month_options.keys()),
    index=0
)

# Retrieve the selected DataFrame
heatmap_data = month_options[selected_month_label]

# Ensure heatmap_data is not empty
if heatmap_data.empty:
    st.warning("No data available for the selected month.")
    st.stop()

# Dropdown for week number selection
selected_week_number = st.selectbox(
    "Select a Week Number",
    options=sorted(heatmap_data['week_number'].unique()),  # Ensure sorted order
    index=0
)

# Filter data by selected week number
weekly_data = heatmap_data[heatmap_data['week_number'] == selected_week_number]

# Ensure there is data available for the selected week
if weekly_data.empty:
    st.warning(f"No data available for week {selected_week_number}.")
    st.stop()

# Dropdown for weekday selection
selected_weekday = st.selectbox(
    "Select a Weekday",
    options=sorted(weekly_data['weekday'].unique()),  # Ensure sorted order
    index=0
)

# Filter data for the selected week number and weekday
weekday_data = weekly_data[weekly_data['weekday'] == selected_weekday]

# Create pivot table for the heatmap
if not weekday_data.empty:
    heatmap_pivot = weekday_data.pivot(index='Zone', columns='hour', values='driver_pay')

    # Check if pivot table is empty
    if heatmap_pivot.empty:
        st.warning(f"No data available for {selected_weekday} in week {selected_week_number}.")
    else:
        # Plot the heatmap
        fig = px.imshow(
            heatmap_pivot,
            labels={"x": "Hour", "y": "Zone", "color": "Total Driver Pay"},
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            color_continuous_scale="reds"
        )

        # Customize layout
        fig.update_layout(
            title=f"Total Driver Pay for Top 10 Zones on {selected_weekday}, Week {selected_week_number}",
            xaxis_title="Hour of Day",
            yaxis_title="Zone",
            coloraxis_colorbar=dict(title="Total Pay ($)"),
            autosize=True
        )

        # Display the heatmap in Streamlit
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No data available for {selected_weekday} in week {selected_week_number}.")
