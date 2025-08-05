import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Config
st.set_page_config(page_title="Global Fleet Explorer", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Fleet_Reg.csv")

df = load_data()

st.title("✈️ Global Aircraft Fleet Explorer")

# Step 1: Choose Region
st.subheader("Step 1: Choose a Region")
region_list = sorted(df['Region'].dropna().unique())
selected_region = None

cols = st.columns(4)
for i, region in enumerate(region_list):
    if cols[i % 4].button(region):
        selected_region = region

if selected_region:
    st.success(f"Selected Region: {selected_region}")
    reg_df = df[df['Region'] == selected_region]

    # Step 2: Choose Airline
    st.subheader("Step 2: Choose an Airline")
    airline_list = sorted(reg_df['ParentAirline'].dropna().unique())
    selected_airline = None

    cols2 = st.columns(4)
    for i, airline in enumerate(airline_list):
        if cols2[i % 4].button(airline):
            selected_airline = airline

    if selected_airline:
        st.success(f"Selected Airline: {selected_airline}")
        airline_df = reg_df[reg_df['ParentAirline'] == selected_airline]

        # Metrics
        st.markdown("### ✈️ Fleet Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current", int(airline_df['Current'].sum()))
        col2.metric("Historic", int(airline_df['Historic'].sum()))
        col3.metric("Future", int(airline_df['Future'].sum()))

        # Aircraft Type Chart
        st.markdown("### 📊 Current Aircraft Types")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=airline_df, x='AircraftType', y='Current', ax=ax)
        ax.set_xlabel("Aircraft Type")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.info("Please select a region to begin.")
