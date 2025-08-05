import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Configuration
st.set_page_config(page_title="🌍 Global Fleet Explorer", layout="wide")

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("Fleet_Reg.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("🔎 Filter Options")
region = st.sidebar.selectbox("🌎 Select Region", sorted(df['Region'].dropna().unique()))
filtered_region = df[df['Region'] == region]

airlines = sorted(filtered_region['ParentAirline'].dropna().unique())
airline = st.sidebar.selectbox("✈️ Select Airline", airlines)

filtered_airline = filtered_region[filtered_region['ParentAirline'] == airline]

# Header
st.title("✈️ Global Aircraft Fleet Dashboard")
st.markdown(f"Analyzing **Aircraft Types** operated by **{airline}** in **{region}** region")

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("🛬 Current Fleet", int(filtered_airline['Current'].sum()))
col2.metric("📜 Historic Fleet", int(filtered_airline['Historic'].sum()))
col3.metric("📈 Future Orders", int(filtered_airline['Future'].sum()))

st.markdown("---")

# Aircraft Type Barplot
st.subheader("📊 Aircraft Type Distribution (Current)")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=filtered_airline, x='AircraftType', y='Current', ax=ax)
ax.set_xlabel("Aircraft Type")
ax.set_ylabel("Current Fleet Count")
plt.xticks(rotation=45)
st.pyplot(fig)

# Optional: Expandable Table
with st.expander("📄 View Detailed Table"):
    st.dataframe(filtered_airline[['AircraftType', 'Current', 'Historic', 'Future', 'Age']].sort_values(by="Current", ascending=False))

# Optional: Aircraft Age Distribution
st.subheader("📈 Aircraft Age Distribution")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_airline['Age'], bins=10, kde=True, ax=ax2)
ax2.set_xlabel("Age (Years)")
ax2.set_ylabel("Number of Aircraft")
st.pyplot(fig2)

# Optional Footer
st.markdown("""
---
💡 *Built with love using Streamlit & Seaborn.*  
Data Source: Global_Fleet.csv
""")
