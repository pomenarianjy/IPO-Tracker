import streamlit as st
import pandas as pd
from ipo_data import load_verified_hk_ipos_part1
from ipo_data2 import load_verified_hk_ipos_part2

# Page Configuration
st.set_page_config(
    page_title="HKEX 2026 IPO Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load and Combine Data from Both Modules
@st.cache_data
def get_combined_ipo_data():
    part1 = load_verified_hk_ipos_part1()
    part2 = load_verified_hk_ipos_part2()
    combined = part1 + part2
    df = pd.DataFrame(combined)
    df["Listing Date"] = pd.to_datetime(df["Listing Date"])
    return df

df_ipos = get_combined_ipo_data()

# App Header
st.title("🇭🇰 HKEX 2026 IPO Market Dashboard")
st.markdown("Comprehensive tracking of newly listed companies on the Hong Kong Exchanges and Clearing (HKEX) for 2026.")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_industry = st.sidebar.multiselect(
    "Select Industry",
    options=df_ipos["Industry"].unique(),
    default=df_ipos["Industry"].unique()
)

selected_board = st.sidebar.multiselect(
    "Select Exchange Board",
    options=df_ipos["Exchange"].unique(),
    default=df_ipos["Exchange"].unique()
)

# Filter Data
filtered_df = df_ipos[
    (df_ipos["Industry"].isin(selected_industry)) & 
    (df_ipos["Exchange"].isin(selected_board))
]

# Metrics Overview
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Tracked IPOs", len(filtered_df))
with col2:
    st.metric("Main Board Listings", len(filtered_df[filtered_df["Exchange"] == "Main Board"]))
with col3:
    st.metric("GEM Listings", len(filtered_df[filtered_df["Exchange"] == "GEM"]))

st.markdown("---")

# Data Table Display
st.subheader("Verified IPO Listings Registry")
st.dataframe(
    filtered_df.sort_values(by="Listing Date", ascending=False),
    column_config={
        "Ticker": "Stock Code",
        "CleanTicker": None,  # Hide helper column if present
        "Listing Date": st.column_config.DateColumn("Listing Date", format="YYYY-MM-DD")
    },
    use_container_width=True
)

# Industry Breakdown Chart
st.subheader("Listings by Industry")
if not filtered_df.empty:
    industry_counts = filtered_df["Industry"].value_counts()
    st.bar_chart(industry_counts)
else:
    st.info("No data available for the selected filters.")
