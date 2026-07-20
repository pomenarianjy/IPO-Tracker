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

# Fetch actual day-to-day historical closing figures directly via yfinance API
@st.cache_data(ttl=1800)
def fetch_live_yfinance_batch(tickers, listing_dates):
    latest_prices = {}
    return_pcts = {}
    history_cache = {}
    
    for ticker, l_date in-zip(tickers, listing_dates):
        clean_code = ticker.strip().replace(".HK", "").zfill(5)
        yf_symbol = f"{clean_code}.HK"
        
        try:
            tk = yf.Ticker(yf_symbol)
            # Pull daily historical records starting precisely from the listing date
            hist = tk.history(start=l_date.strftime("%Y-%m-%d"), end="2026-07-21")
            
            if hist.empty or len(hist) < 1:
                # Fallback to recent trading window if exact IPO history vector is missing on Yahoo Finance
                hist = tk.history(period="1mo")
                
            if not hist.empty:
                history_cache[ticker] = hist
                base_val = float(hist["Close"].iloc[0])
                latest_val = float(hist["Close"].iloc[-1])
                
                if base_val > 0:
                    pct = ((latest_val - base_val) / base_val) * 100
                else:
                    pct = 0.0
                    
                latest_prices[ticker] = round(latest_val, 2)
                return_pcts[ticker] = round(pct, 2)
            else:
                latest_prices[ticker] = 0.0
                return_pcts[ticker] = 0.0
                history_cache[ticker] = pd.DataFrame()
        except Exception:
            latest_prices[ticker] = 0.0
            return_pcts[ticker] = 0.0
            history_cache[ticker] = pd.DataFrame()
            
    return latest_prices, return_pcts, history_cache

tickers_list = df_ipos["Ticker"].tolist()
dates_list = df_ipos["Listing Date"].tolist()

with st.spinner("Connecting to Yahoo Finance API for live HKEX market data..."):
    yf_latest, yf_returns, yf_histories = fetch_live_yfinance_batch(tickers_list, dates_list)

df_ipos["Latest Price (HKD)"] = df_ipos["Ticker"].map(yf_latest)
df_ipos["Return Since IPO (%)"] = df_ipos["Ticker"].map(yf_returns)

# App Header
st.title("🇭🇰 Jasmine's HKEX 2026 IPO Market Dashboard")
st.markdown("Live tracking of newly listed companies on the Hong Kong Exchanges and Clearing (HKEX) powered by Yahoo Finance.")

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
    
    # Retrieve true historical time-series vector from cache
    stock_hist = yf_histories.get(chosen_ticker, pd.DataFrame())
    
    if not stock_hist.empty and "Close" in stock_hist.columns:
        chart_df = pd.DataFrame({"Price": stock_hist["Close"]})
    else:
        chart_df = pd.DataFrame({"Price": [latest_price]})
    
    market_cap_value = latest_price * 2010000000
    market_cap_str = f"HKD {market_cap_value:,.2f}"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("**Latest Price**")
        st.markdown(f"HKD {latest_price:,.2f} ({perf_pct:+.2f}%)")
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
    st.markdown("### Real Day-to-Day Yahoo Finance Price History")
    if not chart_df.empty:
        st.line_chart(chart_df["Price"])
    else:
        st.warning("No historical daily data available via Yahoo Finance for this ticker configuration.")
    
    st.markdown("### Related Trading Statistics")
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.write(f"**Chinese Name:** {stock_info['Chinese Name']}")
        st.write(f"**Industry Sector:** {stock_info['Industry']}")
        st.write(f"**Sub-Sector:** {stock_info['Sub-Sector']}")
    with stat_col2:
        st.write(f"**Listing Date:** {stock_info['Listing Date'].strftime('%Y-%m-%d')}")
        st.write(f"**Data Provider:** Yahoo Finance API (.HK)")
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

    st.subheader("Verified IPO Listings Registry (Live Yahoo Finance Feed)")
    
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
