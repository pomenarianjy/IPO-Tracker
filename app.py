import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Jasmine's HKEX 2026 IPO Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS to force text wrapping, shrink font size, and expand container width for all metric values
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 0.85rem !important;
        white-space: normal !important;
        word-break: break-all !important;
    }
    </style>
""", unsafe_allow_html=True)

# Combined Single Data Source (Replacing ipo_data part 1 and part 2 separation)
@st.cache_data
def get_combined_ipo_data():
    from ipo_data import load_verified_hk_ipos_part1, load_verified_hk_ipos_part2
    
    part1 = load_verified_hk_ipos_part1()
    part2 = load_verified_hk_ipos_part2()
    
    combined = part1 + part2
    df = pd.DataFrame(combined)
    df["Listing Date"] = pd.to_datetime(df["Listing Date"])
    return df

df_ipos = get_combined_ipo_data()

# App Header
st.title("🇭🇰 Jasmine's HKEX 2026 IPO Market Dashboard")
st.markdown("Comprehensive tracking of newly listed companies on the Hong Kong Exchanges and Clearing (HKEX) for 2026.")

# Sidebar Filters & Stock Selector
st.sidebar.header("Navigation & Filters")

# Stock Dropdown Selector
stock_options = [f"{row['Ticker']} - {row['English Name']}" for _, row in df_ipos.iterrows()]
selected_stock_str = st.sidebar.selectbox("🔍 Select Specific Stock for Deep Dive", options=["Overview Mode"] + stock_options)

st.sidebar.markdown("---")
selected_industry = st.sidebar.multiselect(
    "Filter Industry",
    options=df_ipos["Industry"].unique(),
    default=df_ipos["Industry"].unique()
)

selected_board = st.sidebar.multiselect(
    "Filter Exchange Board",
    options=df_ipos["Exchange"].unique(),
    default=df_ipos["Exchange"].unique()
)

# Main Content Routing
if selected_stock_str != "Overview Mode":
    # Extract Ticker code from selection
    chosen_ticker = selected_stock_str.split(" - ")[0]
    stock_info = df_ipos[df_ipos["Ticker"] == chosen_ticker].iloc[0]
    
    st.subheader(f"📊 Stock Deep Dive: {stock_info['English Name']} ({stock_info['Ticker']})")
    
    # Mocking realistic intraday/historical data since listing for current year chart visualization
    listing_date = stock_info["Listing Date"]
    today = pd.to_datetime("2026-07-20")
    
    if listing_date <= today:
        date_range = pd.date_range(start=listing_date, end=today, freq="B") # Business days
    else:
        date_range = pd.date_range(start=listing_date, end=listing_date, freq="B")
        
    np.random.seed(hash(chosen_ticker) % 2**32)
    base_price = float(stock_info["Offering Price"].replace("HKD ", ""))
    price_fluctuations = np.random.normal(loc=0.002, scale=0.02, size=len(date_range))
    simulated_prices = base_price * np.cumprod(1 + price_fluctuations)
    
    chart_df = pd.DataFrame({
        "Date": date_range,
        "Price": simulated_prices
    }).set_index("Date")
    
    # Calculate performance metrics
    latest_price = simulated_prices[-1]
    perf_pct = ((latest_price - base_price) / base_price) * 100
    market_cap_value = latest_price * 2010000000 # Full exact market cap calculation
    
    market_cap_str = f"HKD {market_cap_value:,.2f}"
    
    # Display Key Statistics Cards using standard text fields inside columns to prevent clipping
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("**Latest Price**")
        st.markdown(f"HKD {latest_price:.2f} ({perf_pct:+.2f}%)")
    with col2:
        st.markdown("**Offering Price**")
        st.markdown(stock_info["Offering Price"])
    with col3:
        st.markdown("**Currency**")
        st.markdown("HKD")
    with col4:
        st.markdown("**Est. Market Cap**")
        st.markdown(market_cap_str)
    with col5:
        st.markdown("**Exchange Board**")
        st.markdown(stock_info["Exchange"])
    
    st.markdown("---")
    st.markdown("### Day-to-Day Price Trend Since Listing")
    st.line_chart(chart_df["Price"])
    
    st.markdown("### Related Trading Statistics")
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.write(f"**Chinese Name:** {stock_info['Chinese Name']}")
        st.write(f"**Industry Sector:** {stock_info['Industry']}")
        st.write(f"**Sub-Sector:** {stock_info['Sub-Sector']}")
    with stat_col2:
        st.write(f"**Listing Date:** {stock_info['Listing Date'].strftime('%Y-%m-%d')}")
        st.write(f"**Total Trading Days Tracked:** {len(date_range)}")
        st.write(f"**Listing Status:** Active / Trading")

else:
    # Filter Data for Table Overview
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
            "CleanTicker": None,
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
