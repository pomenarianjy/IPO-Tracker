import streamlit as st
import pandas as pd
import yfinance as yf

# Page Configuration
st.set_page_config(
    page_title="Jasmine's HKEX 2026 IPO Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for styling metrics
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 0.85rem !important;
        white-space: normal !important;
        word-break: break-all !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load Initial Registry Data from local module structure
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

# Pure Yahoo Finance Data Pull (No simulations, no hardcoded overrides)
@st.cache_data(ttl=600)
def fetch_pure_yfinance_data(tickers, listing_dates):
    latest_prices = {}
    return_pcts = {}
    history_cache = {}
    
    for ticker, l_date in zip(tickers, listing_dates):
        clean_code = ticker.strip().replace(".HK", "").zfill(5)
        yf_symbol = f"{clean_code}.HK"
        
        try:
            tk = yf.Ticker(yf_symbol)
            # Pull max history directly from Yahoo Finance
            hist = tk.history(period="max")
            
            if not hist.empty:
                if hist.index.tz is not None:
                    hist.index = hist.index.tz_localize(None)
                
                # Filter strictly from the listing date onward
                sliced = hist[hist.index >= l_date]
                if sliced.empty:
                    sliced = hist  # Fallback to full series if listing date filter is out of range
                
                history_cache[ticker] = sliced
                
                base_val = float(sliced["Close"].iloc[0])
                latest_val = float(sliced["Close"].iloc[-1])
                
                if base_val > 0:
                    pct = ((latest_val - base_val) / base_val) * 100
                else:
                    pct = 0.0
                    
                latest_prices[ticker] = round(latest_val, 2)
                return_pcts[ticker] = round(pct, 2)
            else:
                latest_prices[ticker] = None
                return_pcts[ticker] = None
                history_cache[ticker] = pd.DataFrame()
        except Exception:
            latest_prices[ticker] = None
            return_pcts[ticker] = None
            history_cache[ticker] = pd.DataFrame()
            
    return latest_prices, return_pcts, history_cache

tickers_list = df_ipos["Ticker"].tolist()
dates_list = df_ipos["Listing Date"].tolist()

with st.spinner("Fetching live day-to-day market data from Yahoo Finance..."):
    yf_latest, yf_returns, yf_histories = fetch_pure_yfinance_data(tickers_list, dates_list)

df_ipos["Latest Price (HKD)"] = df_ipos["Ticker"].map(yf_latest)
df_ipos["Return Since IPO (%)"] = df_ipos["Ticker"].map(yf_returns)

# App Header
st.title("🇭🇰 Jasmine's HKEX 2026 IPO Market Dashboard")
st.markdown("Live day-to-day market tracking powered strictly by Yahoo Finance API records.")

# Sidebar Filters & Stock Selector
st.sidebar.header("Navigation & Filters")

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
    chosen_ticker = selected_stock_str.split(" - ")[0]
    stock_info = df_ipos[df_ipos["Ticker"] == chosen_ticker].iloc[0]
    
    st.subheader(f"📊 Stock Deep Dive: {stock_info['English Name']} ({stock_info['Ticker']})")
    
    latest_price = stock_info["Latest Price (HKD)"]
    perf_pct = stock_info["Return Since IPO (%)"]
    
    stock_hist = yf_histories.get(chosen_ticker, pd.DataFrame())
    
    if not stock_hist.empty and "Close" in stock_hist.columns:
        chart_df = pd.DataFrame({"Price": stock_hist["Close"]})
    else:
        chart_df = pd.DataFrame(columns=["Price"])
    
    market_cap_str = f"HKD {latest_price * 2010000000:,.2f}" if latest_price is not None else "N/A"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("**Latest Price**")
        if latest_price is not None:
            st.markdown(f"HKD {latest_price:,.2f} ({perf_pct:+.2f}%)")
        else:
            st.markdown("No Live Data Found")
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
    st.markdown("### Yahoo Finance Historical Price Chart")
    if not chart_df.empty:
        st.line_chart(chart_df["Price"])
    else:
        st.warning("Yahoo Finance returned no historical price series for this ticker symbol.")
    
    st.markdown("### Related Trading Statistics")
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.write(f"**Chinese Name:** {stock_info['Chinese Name']}")
        st.write(f"**Industry Sector:** {stock_info['Industry']}")
        st.write(f"**Sub-Sector:** {stock_info['Sub-Sector']}")
    with stat_col2:
        st.write(f"**Listing Date:** {stock_info['Listing Date'].strftime('%Y-%m-%d')}")
        st.write(f"**Data Source:** Yahoo Finance (.HK)")
        st.write(f"**Listing Status:** Active / Trading")

else:
    filtered_df = df_ipos[
        (df_ipos["Industry"].isin(selected_industry)) & 
        (df_ipos["Exchange"].isin(selected_board))
    ].copy()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tracked IPOs", len(filtered_df))
    with col2:
        st.metric("Main Board Listings", len(filtered_df[filtered_df["Exchange"] == "Main Board"]))
    with col3:
        st.metric("GEM Listings", len(filtered_df[filtered_df["Exchange"] == "GEM"]))

    st.markdown("---")

    st.subheader("Verified IPO Listings Registry (Pure Yahoo Finance Feed)")
    
    display_df = filtered_df.sort_values(by="Listing Date", ascending=False)
    
    st.dataframe(
        display_df,
        column_config={
            "Ticker": "Stock Code",
            "CleanTicker": None,
            "Listing Date": st.column_config.DateColumn("Listing Date", format="YYYY-MM-DD"),
            "Return Since IPO (%)": st.column_config.NumberColumn(
                "Return Since IPO (%)",
                format="%.2f%%"
            ),
            "Latest Price (HKD)": st.column_config.NumberColumn(
                "Latest Price (HKD)",
                format="HKD %.2f"
            )
        },
        use_container_width=True
    )

    st.subheader("Listings by Industry")
    if not filtered_df.empty:
        industry_counts = filtered_df["Industry"].value_counts()
        st.bar_chart(industry_counts)
    else:
        st.info("No data available for the selected filters.")
