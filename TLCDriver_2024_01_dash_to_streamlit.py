import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df_02_2023 = pd.read_csv("TLCDriver_2023_02_heatmap_df.csv")

df_01_2024 = pd.read_csv("TLCDriver_2024_01_heatmap_df.csv")
df_02_2024 = pd.read_csv("TLCDriver_2024_02_heatmap_df.csv")
df_03_2024 = pd.read_csv("TLCDriver_2024_03_heatmap_df.csv")
df_04_2024 = pd.read_csv("TLCDriver_2024_04_heatmap_df.csv")
df_05_2024 = pd.read_csv("TLCDriver_2024_05_heatmap_df.csv")
df_06_2024 = pd.read_csv("TLCDriver_2024_06_heatmap_df.csv")
df_07_2024 = pd.read_csv("TLCDriver_2024_07_heatmap_df.csv")
df_08_2024 = pd.read_csv("TLCDriver_2024_08_heatmap_df.csv")
df_09_2024 = pd.read_csv("TLCDriver_2024_09_heatmap_df.csv")
df_10_2024 = pd.read_csv("TLCDriver_2024_10_heatmap_df.csv")
df_11_2024 = pd.read_csv("TLCDriver_2024_11_heatmap_df.csv")
# Dictionary to map months to DataFrames
month_options = {
    "February 2023": df_02_2023,

    "January 2024": df_01_2024,
    "February 2024": df_02_2024,
    "March 2024": df_03_2024,
    "April 2024": df_04_2024,
    "May 2024": df_05_2024,
    "June 2024": df_06_2024,
    "July 2024": df_07_2024,
    "August 2024": df_08_2024,
    "September 2024": df_09_2024,
    "October 2024": df_10_2024,
    "November 2024": df_11_2024,
}

# Streamlit app title
st.title("NYC For-Hire Driver Earnings Analysis: Trends by Month, Week, Day & Hour")
st.link_button("Data source: Historical data ", "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")

st.markdown("""
### Dashboard Summary  
🚖 **Driver Earnings Heatmap** – This interactive visualization helps analyze **driver pay trends** across different ** Months, zones, weekdays, and hours of the day**.  

📊 **How to Use:**  
1️⃣ **Select a Month** – Choose the dataset for a specific month.  
2️⃣ **Select a Week Number** – Focus on earnings for a particular week.  
3️⃣ **Select a Weekday** – Analyze trends for a specific day.  
4️⃣ **Explore the Heatmap** – Darker areas indicate higher total driver pay.  

Use these insights to optimize driving schedules, understand peak hours, and maximize earnings based on historical data! 🚀  
""")
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
        fig = px.imshow(
            heatmap_pivot,
            labels={"x": "Hour", "y": "Zone", "color": "Total Driver Pay ($)"},
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            color_continuous_scale="reds",
        )
              # Update hover text formatting to include $ and thousand separators
        fig.update_traces(
            hovertemplate="Hour: %{x}<br>Zone: %{y}<br>Total Pay: $%{z:,.2f}"
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
