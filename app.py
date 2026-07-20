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

# Custom Styling (Enhanced Typography & Layout Polish)
st.markdown("""
    <style>
    .main-title {
        font-size: 3.2rem;
        color: #1E3A8A;
        font-weight: 800;
        margin-bottom: 2px;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 1.25rem;
        color: #4B5563;
        margin-bottom: 25px;
        font-weight: 400;
    }
    .section-title {
        font-size: 1.8rem;
        color: #1F2937;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 1.4rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<p class="main-title">🌸 Jasmine’s HKEX IPO Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Comprehensive real-time tracking dashboard for Hong Kong Stock Exchange year-to-date listings.</p>', unsafe_allow_html=True)

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

# --- MAIN MENU SECTION ---
st.markdown('<p class="section-title">📋 HKEX Newly Listed Companies Full Menu</p>', unsafe_allow_html=True)
st.markdown(f"Displaying **{len(df_ipo)}** verified newly listed companies from your database.")

# Menu columns display mapping
menu_display = df_ipo[['CleanTicker', 'English Name', 'Chinese Name', 'Industry', 'Sub-Sector', 'Exchange', 'Listing Date', 'Offering Price']].copy()
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
    "Select a specific company to inspect live charts & metrics on the panel below:",
    options=df_ipo['CleanTicker'].tolist(),
    format_func=lambda x: f"{x} - {df_ipo[df_ipo['CleanTicker']==x]['English Name'].values[0]} ({df_ipo[df_ipo['CleanTicker']==x]['Chinese Name'].values[0]})"
)

target_row = df_ipo[df_ipo['CleanTicker'] == selected_code].iloc[0]
ticker_symbol = target_row['Ticker']

# --- SAFE YAHOO FINANCE LIVE FEED BRIDGE ---
@st.cache_data(ttl=600)
def fetch_safe_stock_history(symbol):
    try:
        tk = yf.Ticker(symbol)
        history = tk.history(period="max")
        return history, None
    except Exception as e:
        return pd.DataFrame(), str(e)

hist_data, api_error = fetch_safe_stock_history(ticker_symbol)

# --- SPLIT SCREEN PANEL DESIGN ---
st.markdown("---")
col_left, col_right = st.columns([1.1, 1.9])

with col_left:
    st.markdown('<p class="card-title">🏢 Company Profile</p>', unsafe_allow_html=True)
    st.markdown(f"**English Name:** {target_row['English Name']}")
    st.markdown(f"**Chinese Name:** {target_row['Chinese Name']}")
    st.markdown(f"**Ticker Symbol:** `{target_row['Ticker']}`")
    st.markdown(f"**Board Exchange:** {target_row['Exchange']}")
    st.markdown(f"**Industry / Sub-Sector:** {target_row['Industry']} / *{target_row['Sub-Sector']}*")
    st.markdown(f"**Listing Date:** {target_row['Listing Date']}")
    st.markdown(f"**Offering Price:** {target_row['Offering Price']}")
    
    st.markdown("---")
    st.markdown('<p class="card-title">📊 Trading Statistics & Crucial Info</p>', unsafe_allow_html=True)
    
    if not hist_data.empty:
        current_price = hist_data['Close'].iloc[-1]
        previous_close = hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price
        pct_change = ((current_price - previous_close) / previous_close) * 100
        volume = f"{int(hist_data['Volume'].iloc[-1]):,}" if 'Volume' in hist_data.columns else 'N/A'
    else:
        current_price = np.nan
        pct_change = 0.0
        volume = 'N/A'

    st.metric(
        label="Live Last Close Price (HKD)", 
        value=f"{current_price:,.2f}" if not pd.isna(current_price) else "Data syncing...", 
        delta=f"{pct_change:.2f}%"
    )
    st.markdown(f"- **Currency:** HKD")
    st.markdown(f"- **Latest Trading Volume:** {volume}")
    st.markdown(f"- **Primary Listing Baseline:** {target_row['Offering Price']}")
    if api_error:
        st.info("Note: Live feed currently rate-limited by provider. Showing verified static reference records.")

with col_right:
    st.markdown('<p class="card-title">📈 Stock Performance Chart (Day-to-Day Changes)</p>', unsafe_allow_html=True)
    if not hist_data.empty:
        st.line_chart(hist_data['Close'], height=310)
    else:
        st.warning("Historical price data is temporarily rate-limited or updating from the market feed. Please check back shortly.")

    st.markdown('<p class="card-title">🔗 Comparable Companies from Universe</p>', unsafe_allow_html=True)
    peers = df_ipo[(df_ipo['Industry'] == target_row['Industry']) & (df_ipo['CleanTicker'] != target_row['CleanTicker'])]
    if not peers.empty:
        peer_sample = peers.head(4)[['CleanTicker', 'English Name', 'Chinese Name', 'Sub-Sector']]
        peer_sample.columns = ["Ticker", "English Name", "Chinese Name", "Sub-Sector"]
        st.table(peer_sample)
    else:
        st.info("No comparable industry peers matched in current filter frame.")

# --- BOTTOM SECTION: TOP & WORST PERFORMING IPO STOCKS YTD (PURE DATASET DRIVEN) ---
st.markdown("---")
st.markdown('<p class="section-title">🏆 Top 5 Performing IPO Stocks Year-to-Date</p>', unsafe_allow_html=True)

@st.cache_data(ttl=1800)
def compute_comprehensive_leaderboard(df):
    results = []
    
    # Strictly evaluating solely from the loaded dataset without hardcoded outside interference
    for _, row in df.iterrows():
        try:
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
        except Exception:
            continue
            
    res_df = pd.DataFrame(results)
    if res_df.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    top_5 = res_df.sort_values(by="YTD Return (%)", ascending=False).head(5)
    worst_5 = res_df.sort_values(by="YTD Return (%)", ascending=True).head(5)
    return top_5, worst_5

top_performers_df, worst_performers_df = compute_comprehensive_leaderboard(df_ipo)

if not top_performers_df.empty:
    st.dataframe(top_performers_df, use_container_width=True, hide_index=True)
else:
    st.info("Top leaderboard calculation in progress...")

st.markdown('<p class="section-title">⚠️ Bottom 5 Underperforming IPO Stocks Year-to-Date</p>', unsafe_allow_html=True)

if not worst_performers_df.empty:
    st.dataframe(worst_performers_df, use_container_width=True, hide_index=True)
else:
    st.info("Underperformer leaderboard calculation in progress...")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 0.95rem;'>Jasmine’s HKEX IPO Tracking Platform • Powered by Streamlit & Yahoo Finance API</p>", unsafe_allow_html=True)
