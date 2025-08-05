import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Page config
st.set_page_config(page_title="Global Fleet Explorer", layout="wide")

# Title
st.title("✈️ Global Aircraft Fleet Explorer")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("../DataSets/Global_Fleet.csv")
    return df

df = load_data()

# Region Selection
region = st.selectbox("Select Region:", sorted(df['Region'].dropna().unique()))

# Filter by Region
filtered_by_region = df[df['Region'] == region]

# Airline Selection
airlines = sorted(filtered_by_region['ParentAirline'].dropna().unique())
airline = st.selectbox("Select Airline:", airlines)

# Filter by Airline
filtered_by_airline = filtered_by_region[filtered_by_region['ParentAirline'] == airline]

# Plotting
st.subheader(f"Current Aircraft Types for {airline}")
plt.figure(figsize=(12,6))
sb.barplot(x='AircraftType', y='Current', data=filtered_by_airline)
plt.xticks(rotation=90)
plt.tight_layout()
st.pyplot(plt)
