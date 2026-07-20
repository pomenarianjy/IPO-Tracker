import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import ipo_data  # Imports your uploaded ipo_data.py file

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Jasmine’s HKEX IPO Tracker",
    page_icon="🌸",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.4rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<p class="main-title">🌸 Jasmine’s HKEX IPO Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tracking all Hong Kong Stock Exchange YTD listings with real-time Yahoo Finance data.</p>', unsafe_allow_html=True)

# --- LOAD DATA FROM ipo_data.py ---
@st.cache_data
def load_data():
    raw_list = ipo_data.load_verified_hk_ipos()
    df = pd.DataFrame(raw_list)
    return df

df_ipo = load_data()

if df_ipo.empty:
    st.error("No stock data returned from `ipo_data.load_verified_hk_ipos()`.")
    st.stop()

# --- SIDEBAR SCREENING OPTIONS ---
st.sidebar.markdown("## 🔍 Market Filters & Screening")
industries = ["All Industries"] + list(df_ipo["Industry"].dropna().unique())
selected_industry = st.sidebar.selectbox("Filter by Industry", industries)

if selected_industry != "All Industries":
    filtered_df = df_ipo[df_ipo["Industry"] == selected_industry]
else:
    filtered_df = df_ipo

subsectors = ["All Sub-Sectors"] + list(filtered_df["Sub-Sector"].dropna().unique())
selected_subsector = st.sidebar.selectbox("Filter by Sub-Sector", subsectors)

if selected_subsector != "All Sub-Sectors":
    filtered_df = filtered_df[filtered_df["Sub-Sector"] == selected_subsector]

search_query = st.sidebar.text_input("Search Ticker, English or Chinese Name", "").lower()
if search_query:
    filtered_df = filtered_df[
        filtered_df['English Name'].str.lower().str.contains(search_query, na=False) |
        filtered_df['Chinese Name'].str.contains(search_query, na=False) |
        filtered_df['Ticker'].str.lower().str.contains(search_query, na=False) |
        filtered_df['CleanTicker'].str.lower().str.contains(search_query, na=False)
    ]

# --- MAIN MENU SECTION ---
st.markdown("### 📋 HKEX Newly Listed Companies Full Menu")
st.markdown(f"Displaying **{len(filtered_df)}** matching companies from your database.")

# Menu columns display mapping
menu_display = filtered_df[['CleanTicker', 'English Name', 'Chinese Name', 'Industry', 'Sub-Sector', 'Exchange', 'Listing Date', 'Offering Price']].copy()
column_rename_map = {
    "CleanTicker": "Ticker Code", 
    "English Name": "English Name", 
    "Chinese Name": "Chinese Name (中文名称)", 
    "Industry": "Industry", 
    "Sub-Sector": "Sub-Sector", 
    "Exchange": "Exchange Board",
    "Listing Date": "Listing Date",
    "Offering Price": "Offering Price"
}
menu_display.rename(columns=column_rename_map, inplace=True)
st.dataframe(menu_display, use_container_width=True, hide_index=True)

# Selection configuration
selected_code = st.selectbox(
    "Select a specific company to inspect live charts & metrics on the right panel:",
    options=filtered_df['CleanTicker'].tolist(),
    format_func=lambda x: f"{x} - {filtered_df[filtered_df['CleanTicker']==x]['English Name'].values[0]} ({filtered_df[filtered_df['CleanTicker']==x]['Chinese Name'].values[0]})"
)

target_row = df_ipo[df_ipo['CleanTicker'] == selected_code].iloc[0]
ticker_symbol = target_row['Ticker']

# --- YAHOO FINANCE LIVE FEED BRIDGE ---
@st.cache_data(ttl=600)
def fetch_live_stock_data(symbol):
    tk = yf.Ticker(symbol)
    history = tk.history(period="max")
    inf = tk.info
    return history, inf

hist_data, stock_info = fetch_live_stock_data(ticker_symbol)

# --- SPLIT SCREEN PANEL DESIGN ---
st.markdown("---")
col_left, col_right = st.columns([1.1, 1.9])

with col_left:
    st.markdown("#### 🏢 Company Profile")
    st.markdown(f"**English Name:** {target_row['English Name']}")
    st.markdown(f"**Chinese Name:** {target_row['Chinese Name']}")
    st.markdown(f"**Ticker Symbol:** `{target_row['Ticker']}`")
    st.markdown(f"**Board Exchange:** {target_row['Exchange']}")
    st.markdown(f"**Industry / Sub-Sector:** {target_row['Industry']} / *{target_row['Sub-Sector']}*")
    st.markdown(f"**Listing Date:** {target_row['Listing Date']}")
    st.markdown(f"**Offering Price:** {target_row['Offering Price']}")
    
    st.markdown("---")
    st.markdown("#### 📊 Trading Statistics & Crucial Info")
    
    current_price = stock_info.get('currentPrice', stock_info.get('regularMarketPrice', np.nan))
    previous_close = stock_info.get('previousClose', np.nan)
    currency = stock_info.get('currency', 'HKD')
    market_cap = stock_info.get('marketCap', 'N/A')
    volume = stock_info.get('volume', 'N/A')
    beta = stock_info.get('beta', 'N/A')
    pe_ratio = stock_info.get('trailingPE', 'N/A')
    
    if not pd.isna(current_price) and not pd.isna(previous_close):
        pct_change = ((current_price - previous_close) / previous_close) * 100
    else:
        pct_change = 0.0

    st.metric(label=f"Live Price ({currency})", value=f"{current_price:,.2f}" if not pd.isna(current_price) else "Fetching feed...", delta=f"{pct_change:.2f}%")
    st.markdown(f"- **Currency:** {currency}")
    st.markdown(f"- **Market Capitalization:** {market_cap}")
    st.markdown(f"- **Trading Volume:** {volume}")
    st.markdown(f"- **Volatility Metric (Beta):** {beta}")
    st.markdown(f"- **Price-to-Earnings (P/E):** {pe_ratio}")

with col_right:
    st.markdown("#### 📈 Stock Performance Chart (Day-to-Day Changes)")
    if not hist_data.empty:
        st.line_chart(hist_data['Close'], height=310)
    else:
        st.warning("Historical price data populating from market feed for this security.")

    st.markdown("#### 🔗 Comparable Companies from Universe")
    peers = df_ipo[(df_ipo['Industry'] == target_row['Industry']) & (df_ipo['CleanTicker'] != target_row['CleanTicker'])]
    if not peers.empty:
        peer_sample = peers.head(4)[['CleanTicker', 'English Name', 'Chinese Name', 'Sub-Sector']]
        peer_sample.columns = ["Ticker", "English Name", "Chinese Name", "Sub-Sector"]
        st.table(peer_sample)
    else:
        st.info("No comparable industry peers matched in current filter frame.")

# --- BOTTOM SECTION: TOP 5 PERFORMING STOCKS YTD ---
st.markdown("---")
st.markdown("### 🏆 Top 5 Performing IPO Stocks Year-to-Date")

@st.cache_data(ttl=1800)
def compute_ytd_leaderboard(df):
    results = []
    for _, row in df.iterrows():
        t_obj = yf.Ticker(row['Ticker'])
        h_df = t_obj.history(period="ytd")
        if not h_df.empty and len(h_df) > 1:
            start_val = h_df['Close'].iloc[0]
            end_val = h_df['Close'].iloc[-1]
            gain = ((end_val - start_val) / start_val) * 100
            results.append({
                "Ticker Code": row['CleanTicker'],
                "English Name": row['English Name'],
                "Chinese Name": row['Chinese Name'],
                "Industry": row['Industry'],
                "YTD Return (%)": round(gain, 2)
            })
    res_df = pd.DataFrame(results)
    if not res_df.empty:
        return res_df.sort_values(by="YTD Return (%)", ascending=False).head(5)
    return pd.DataFrame()

top_performers_df = compute_ytd_leaderboard(df_ipo)

if not top_performers_df.empty:
    st.dataframe(top_performers_df, use_container_width=True, hide_index=True)
else:
    st.info("Leaderboard data calculating from market streams...")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6B7280;'>Jasmine’s HKEX IPO Tracking Platform • Powered by Streamlit & Yahoo Finance API</p>", unsafe_allow_html=True)
