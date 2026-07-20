import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="IPO Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    # Check if a custom dataset exists, otherwise create a mock/sample dataframe or look for ipo_data.py / csv
    if os.path.exists("ipo_data.csv"):
        df = pd.read_csv("ipo_data.csv")
    else:
        # Fallback or sample dataset structure including English and Chinese names
        data = {
            "Company": [
                "TechCorp Ltd (科创有限公司)", 
                "BioHealth Inc (生物健康股份)", 
                "GreenEnergy Co (绿色能源集团)", 
                "CloudScale Systems (云规模系统)", 
                "SmartRetail Ltd (智慧零售股份)"
            ],
            "Ticker": ["09999", "01810", "09618", "09888", "06618"],
            "Sector": ["Technology", "Healthcare", "Clean Energy", "Technology", "Consumer"],
            "Listing_Date": ["2026-01-15", "2026-02-20", "2026-03-10", "2026-04-05", "2026-05-12"],
            "Funds_Raised_USD_M": [1200, 450, 800, 2500, 300],
            "Issue_Price": [50.0, 22.5, 100.0, 150.0, 15.0],
            "Current_Price": [65.0, 20.0, 130.0, 140.0, 18.5]
        }
        df = pd.DataFrame(data)
    
    # Data preprocessing
    if "Listing_Date" in df.columns:
        df["Listing_Date"] = pd.to_datetime(df["Listing_Date"])
        df["Year"] = df["Listing_Date"].dt.year
        df["Month"] = df["Listing_Date"].dt.strftime("%Y-%m")
        
    if "Issue_Price" in df.columns and "Current_Price" in df.columns:
        # Ensure proper numeric type conversion to prevent zero division or string concatenation issues
        df["Issue_Price"] = pd.to_numeric(df["Issue_Price"], errors="coerce")
        df["Current_Price"] = pd.to_numeric(df["Current_Price"], errors="coerce")
        df["Return_Pct"] = ((df["Current_Price"] - df["Issue_Price"]) / df["Issue_Price"]) * 100
        
    return df

df = load_data()

# App Title & Description
st.title("📈 Initial Public Offering (IPO) Analytics Dashboard")
st.markdown("Explore market trends, capital raised, and post-listing performance metrics interactively.")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Sector Filter
sectors = ["All"] + sorted(df["Sector"].unique().tolist()) if "Sector" in df.columns else ["All"]
selected_sector = st.sidebar.selectbox("Select Sector", sectors)

# Year Filter
years = ["All"] + sorted(df["Year"].dropna().unique().tolist(), reverse=True) if "Year" in df.columns else ["All"]
selected_year = st.sidebar.selectbox("Select Listing Year", years)

# Company / Stock Filter (showing English and Chinese names)
companies = ["All"] + sorted(df["Company"].unique().tolist()) if "Company" in df.columns else ["All"]
selected_company = st.sidebar.selectbox("Select Stock (Company)", companies)

# Apply Filters
filtered_df = df.copy()
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]
if selected_company != "All":
    filtered_df = filtered_df[filtered_df["Company"] == selected_company]

# Main Dashboard Metrics
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_ipos = len(filtered_df)
total_funds = filtered_df["Funds_Raised_USD_M"].sum() if "Funds_Raised_USD_M" in filtered_df.columns else 0
avg_return = filtered_df["Return_Pct"].mean() if "Return_Pct" in filtered_df.columns else 0
max_fund = filtered_df["Funds_Raised_USD_M"].max() if "Funds_Raised_USD_M" in filtered_df.columns else 0

col1.metric("Total IPOs", f"{total_ipos}")
col2.metric("Total Capital Raised", f"${total_funds:,.2f}M")
col3.metric("Avg. Post-Listing Return", f"{avg_return:.2f}%" if not pd.isna(avg_return) else "N/A")
col4.metric("Largest Deal", f"${max_fund:,.2f}M")

st.markdown("---")

# Charts Section
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Capital Raised by Sector")
    if "Sector" in filtered_df.columns and "Funds_Raised_USD_M" in filtered_df.columns:
        sector_df = filtered_df.groupby("Sector")["Funds_Raised_USD_M"].sum().reset_index()
        fig_sector = px.bar(sector_df, x="Sector", y="Funds_Raised_USD_M", 
                            title="Total Funds Raised per Sector (USD Millions)",
                            color="Sector", text_auto='.2f')
        st.plotly_chart(fig_sector, use_container_width=True)
    else:
        st.info("Sector or Funds data unavailable.")

with row1_col2:
    st.subheader("IPO Timeline Trend")
    if "Month" in filtered_df.columns:
        time_df = filtered_df.groupby("Month").size().reset_index(name="IPO_Count")
        fig_time = px.line(time_df, x="Month", y="IPO_Count", markers=True,
                           title="Number of Listings Over Time")
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("Date data unavailable for timeline.")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Performance Distribution (Returns %)")
    if "Return_Pct" in filtered_df.columns:
        fig_hist = px.histogram(filtered_df, x="Return_Pct", nbins=20,
                                title="Distribution of Post-Listing Returns (%)",
                                color_discrete_sequence=["indianred"])
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("Return data unavailable.")

with row2_col2:
    st.subheader("Top 10 IPOs by Capital Raised")
    if "Funds_Raised_USD_M" in filtered_df.columns and "Company" in filtered_df.columns:
        top_ipos = filtered_df.nlargest(10, "Funds_Raised_USD_M")
        fig_top = px.bar(top_ipos, x="Funds_Raised_USD_M", y="Company", orientation="h",
                         title="Largest IPOs by Funds Raised", color="Funds_Raised_USD_M")
        fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("Required columns for top IPOs missing.")

st.markdown("---")

# Data Table Explorer
st.subheader("Detailed IPO Dataset Explorer")
st.dataframe(filtered_df, use_container_width=True)

# Download button for filtered data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_ipo_data.csv',
    mime='text/csv',
)
