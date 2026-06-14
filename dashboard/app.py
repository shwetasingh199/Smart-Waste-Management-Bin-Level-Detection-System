import streamlit as st
import pandas as pd
import os
import sys

import folium
from streamlit_folium import st_folium

from streamlit_autorefresh import st_autorefresh

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(PROJECT_ROOT)

from alerts.alert_manager import generate_alert
from analytics.route_optimizer import optimize_route
from analytics.prediction import predict_fill_level
from reports.report_generator import generate_report

st.set_page_config(
    page_title="Smart Waste Management System",
    page_icon="🗑️",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="refresh"
)

st.title(
    "🗑️ Smart Waste Management & Bin Level Detection System"
)

st.markdown(
    "Real-Time Smart City Waste Monitoring Dashboard"
)

DATA_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "waste_data.csv"
)

LOCATION_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "bin_locations.csv"
)

df = pd.read_csv(DATA_FILE)

locations = pd.read_csv(
    LOCATION_FILE
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

with st.sidebar.form(
    "add_bin_data"
):

    st.subheader(
        "Add Bin Reading"
    )

    bin_id = st.selectbox(
        "Bin",
        ["B1","B2","B3","B4","B5"]
    )

    fill_percentage = st.slider(
        "Fill %",
        0,
        100,
        50
    )

    distance = st.number_input(
        "Distance (cm)",
        min_value=0
    )

    submit = st.form_submit_button(
        "Save Reading"
    )

if submit:

    timestamp = pd.Timestamp.now()

    location = locations[
        locations["bin_id"] == bin_id
    ]["location"].iloc[0]

    if fill_percentage < 40:
        status = "EMPTY"

    elif fill_percentage < 80:
        status = "HALF FULL"

    else:
        status = "FULL"

    new_row = pd.DataFrame([{
        "timestamp": timestamp,
        "bin_id": bin_id,
        "location": location,
        "distance": distance,
        "fill_percentage":
            fill_percentage,
        "status": status
    }])

    new_row.to_csv(
        DATA_FILE,
        mode="a",
        header=False,
        index=False
    )

    st.success(
        "Data Saved Successfully"
    )

    st.rerun()

latest_bins = (
    df.sort_values(
        "timestamp"
    )
    .groupby("bin_id")
    .tail(1)
)      

st.subheader(
    "📊 Waste Collection Overview"
)

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric(
    "Total Bins",
    latest_bins["bin_id"].nunique()
)

col2.metric(
    "Full Bins",
    len(
        latest_bins[
            latest_bins["status"]=="FULL"
        ]
    )
)

col3.metric(
    "Half Full",
    len(
        latest_bins[
            latest_bins["status"]=="HALF FULL"
        ]
    )
)

col4.metric(
    "Empty Bins",
    len(
        latest_bins[
            latest_bins["status"]=="EMPTY"
        ]
    )
)

col5.metric(
    "Avg Fill %",
    round(
        latest_bins[
            "fill_percentage"
        ].mean(),
        2
    )
)

st.subheader(
    "🚨 Active Alerts"
)

for _, row in latest_bins.iterrows():

    alert = generate_alert(
        row["fill_percentage"]
    )

    if alert == "CRITICAL":

        st.error(
            f"{row['bin_id']} ({row['location']}) "
            f"is {row['fill_percentage']}% full"
        )

    elif alert == "WARNING":

        st.warning(
            f"{row['bin_id']} ({row['location']}) "
            f"is {row['fill_percentage']}% full"
        )

st.subheader(
    "🗺️ Smart City Bin Map"
)

map_df = pd.merge(
    latest_bins,
    locations,
    on=["bin_id","location"]
)

m = folium.Map(
    location=[
        map_df["latitude"].mean(),
        map_df["longitude"].mean()
    ],
    zoom_start=16
)

for _, row in map_df.iterrows():

    if row["fill_percentage"] >= 80:
        color = "red"

    elif row["fill_percentage"] >= 40:
        color = "orange"

    else:
        color = "green"

    folium.Marker(
        [
            row["latitude"],
            row["longitude"]
        ],
        popup=
        f"{row['bin_id']} | "
        f"{row['fill_percentage']}%",
        icon=folium.Icon(
            color=color
        )
    ).add_to(m)

st_folium(
    m,
    width=1000,
    height=500
)

st.subheader(
    "🗑️ Current Bin Status"
)

st.dataframe(
    latest_bins,
    use_container_width=True
)

st.subheader(
    "📈 Fill Level Comparison"
)

comparison = latest_bins.set_index(
    "location"
)["fill_percentage"]

st.bar_chart(
    comparison
)

st.subheader(
    "📉 Historical Trends"
)

selected_bin = st.selectbox(
    "Select Bin",
    latest_bins["bin_id"].unique()
)

history = df[
    df["bin_id"] == selected_bin
]

st.line_chart(
    history.set_index(
        "timestamp"
    )["fill_percentage"]
)

st.subheader(
    "🚚 Route Optimization"
)

optimized = optimize_route(df)

optimized["Priority"] = range(
    1,
    len(optimized)+1
)

st.dataframe(
    optimized[
        [
            "Priority",
            "bin_id",
            "location",
            "fill_percentage",
            "status"
        ]
    ]
)

st.subheader(
    "📌 Collection Recommendations"
)

for _, row in optimized.iterrows():

    if row["fill_percentage"] >= 90:

        st.error(
            f"Collect {row['bin_id']} immediately"
        )

    elif row["fill_percentage"] >= 70:

        st.warning(
            f"Schedule pickup for {row['bin_id']}"
        )

    else:

        st.success(
            f"{row['bin_id']} is safe"
        )

st.subheader(
    "🤖 Predictive Analytics"
)

prediction_bin = st.selectbox(
    "Select Bin For Prediction",
    latest_bins["bin_id"].unique(),
    key="prediction"
)

prediction = predict_fill_level(
    df,
    prediction_bin
)

st.info(
    f"Predicted Future Fill Level: {prediction}"
)

st.subheader(
    "📄 Download Report"
)

report_path = generate_report(
    df
)

with open(
    report_path,
    "rb"
) as f:

    st.download_button(
        "Download PDF Report",
        f,
        file_name=
        "Waste_Report.pdf"
    )

st.markdown("---")

st.caption(
    "Smart Waste Management Platform | IoT + Analytics + GIS + Smart City Monitoring"
)