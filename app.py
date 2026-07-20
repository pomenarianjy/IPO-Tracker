import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime

# --- PAGE CONFIGURATION & APPLE-INSPIRED DESIGN SYSTEM ---
st.set_page_config(
    page_title="Jasmine’s Greater China IPO Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Apple Product Page Aesthetic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #F5F5F7;
        color: #1D1D1F;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main {
        padding: 2rem 3rem;
    }

    .apple-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .apple-card:hover {
        box-shadow: 0 6px 32px rgba(0, 0, 0, 0.08);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 700;
        letter-spacing: -0.015em;
        color: #1D1D1F;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-size: 18px;
        font-weight: 400;
        color: #86868B;
        margin-bottom: 32px;
    }

    .section-header {
        font-size: 24px;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: #1D1D1F;
        margin-top: 24px;
        margin-bottom: 16px;
    }

    .badge-hkex { background-color: #E8F2FF; color: #0066CC; padding: 4px 10px; border-radius: 6px; font-weight: 500; font-size: 12px; }
    .badge-sse { background-color: #FFEAEA; color: #FF3B30; padding: 4px 10px; border-radius: 6px; font-weight: 500; font-size: 12px; }
    .badge-szse { background-color: #FFF4E5; color: #FF9500; padding: 4px 10px; border-radius: 6px; font-weight: 500; font-size: 12px; }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #D2D2D7;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA UNIVERSE INITIALIZATION ---
@st.cache_data
def load_ipo_universe():
    data = [
        # HKEX Universe (Sample representing the ~85 listings)
        {"ticker": "02525.HK", "name_en": "Hesai Group", "name_cn": "禾赛科技", "exchange": "HKEX", "industry": "Technology", "subsector": "AI & LiDAR Hardware", "ipo_date": "2026-01-15", "issue_price": 28.50},
        {"ticker": "02475.HK", "name_en": "Luxshare ICT", "name_cn": "立讯精密", "exchange": "HKEX", "industry": "Technology", "subsector": "Consumer Electronics", "ipo_date": "2026-02-10", "issue_price": 34.20},
        {"ticker": "06880.HK", "name_en": "Momenta-W", "name_cn": "初速度", "exchange": "HKEX", "industry": "Automotive", "subsector": "Autonomous Driving", "ipo_date": "2026-03-05", "issue_price": 18.00},
        {"ticker": "03752.HK", "name_en": "Rokae Robotics", "name_cn": "珞石机器人", "exchange": "HKEX", "industry": "Industrials", "subsector": "Robotics & Automation", "ipo_date": "2026-03-12", "issue_price": 22.40},
        {"ticker": "02249.HK", "name_en": "Nexchip Semiconductor", "name_cn": "合肥晶合集成", "exchange": "HKEX", "industry": "Technology", "subsector": "Semiconductors", "ipo_date": "2026-04-18", "issue_price": 12.60},
        {"ticker": "02667.HK", "name_en": "Tongrentang Care", "name_cn": "同仁堂健康", "exchange": "HKEX", "industry": "Healthcare", "subsector": "Traditional Biotech", "ipo_date": "2026-04-25", "issue_price": 15.80},
        {"ticker": "07687.HK", "name_en": "Eacon Mining", "name_cn": "易控智驾", "exchange": "HKEX", "industry": "Automotive", "subsector": "Autonomous Mining", "ipo_date": "2026-05-10", "issue_price": 25.00},
        {"ticker": "09971.HK", "name_en": "BasicSemi", "name_cn": "基本半导体", "exchange": "HKEX", "industry": "Technology", "subsector": "Power Semiconductors", "ipo_date": "2026-05-22", "issue_price": 40.00},
        
        # SSE Universe (Main Board & STAR - Sample representing the ~19 listings)
        {"ticker": "688797.SS", "name_en": "Chongqing Genori Technology", "name_cn": "臻宝科技", "exchange": "SSE", "industry": "Technology", "subsector": "Advanced Materials", "ipo_date": "2026-06-24", "issue_price": 45.00},
        {"ticker": "688311.SS", "name_en": "Mingsheng Electronics", "name_cn": "盟升电子", "exchange": "SSE", "industry": "Telecommunications", "subsector": "Satellite Communications", "ipo_date": "2026-05-14", "issue_price": 38.50},
        {"ticker": "688017.SS", "name_en": "Leader Harmonious Drive", "name_cn": "绿的谐波", "exchange": "SSE", "industry": "Industrials", "subsector": "Precision Reducers", "ipo_date": "2026-04-11", "issue_price": 62.00},
        {"ticker": "603352.SS", "name_en": "Chongqing Zhixin Industrial", "name_cn": "智欣实业", "exchange": "SSE", "industry": "Industrials", "subsector": "Building Materials", "ipo_date": "2026-03-20", "issue_price": 14.20},
        {"ticker": "688523.SS", "name_en": "Aerospace Hanyu", "name_cn": "航天环宇", "exchange": "SSE", "industry": "Aerospace & Defense", "subsector": "Aviation Equipment", "ipo_date": "2026-02-19", "issue_price": 21.30},

        # SZSE Universe (Main Board & ChiNext - Sample representing the ~16 listings)
        {"ticker": "301500.SZ", "name_en": "HKC Corporation", "name_cn": "惠科股份", "exchange": "SZSE", "industry": "Technology", "subsector": "Display Panels", "ipo_date": "2026-06-05", "issue_price": 26.40},
        {"ticker": "301400.SZ", "name_en": "Seeya Technology", "name_cn": "视涯科技", "exchange": "SZSE", "industry": "Technology", "subsector": "Micro-OLED Displays", "ipo_date": "2026-05-08", "issue_price": 31.00},
        {"ticker": "001300.SZ", "name_en": "Zhongce Rubber Group", "name_cn": "中策橡胶", "exchange": "SZSE", "industry": "Consumer Cyclical", "subsector": "Automotive Tyres", "ipo_date": "2026-04-02", "issue_price": 48.00},
        {"ticker": "301200.SZ", "name_en": "Tianyouwei Electronics", "name_cn": "天有为电子", "exchange": "SZSE", "industry": "Technology", "subsector": "Automotive Electronics", "ipo_date": "2026-03-15", "issue_price": 19.50}
    ]
    return pd.DataFrame(data)

df_ipo = load_ipo_universe()

# --- HEADER SECTION ---
st.markdown("<div class='hero-title'>Jasmine’s Greater China IPO Tracker</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Live tracking, performance analytics, and institutional-grade screening for HKEX, SSE, and SZSE listings.</div>", unsafe_allow_html=True)

# --- FILTER CONTROLS BAR ---
with st.container():
    st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        exchanges = ["All Exchanges"] + list(df_ipo["exchange"].unique())
        selected_exchange = st.selectbox("Exchange Venue", exchanges)
        
    with f_col2:
        industries = ["All Industries"] + list(df_ipo["industry"].unique())
        selected_industry = st.selectbox("Industry Sector", industries)
        
    with f_col3:
        subsectors = ["All Sub-sectors"] + list(df_ipo["subsector"].unique())
        selected_subsector = st.selectbox("Sub-sector Focus", subsectors)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Apply Filters
filtered_df = df_ipo.copy()
if selected_exchange != "All Exchanges":
    filtered_df = filtered_df[filtered_df["exchange"] == selected_exchange]
if selected_industry != "All Industries":
    filtered_df = filtered_df[filtered_df["industry"] == selected_industry]
if selected_subsector != "All Sub-sectors":
    filtered_df = filtered_df[filtered_df["subsector"] == selected_subsector]

# --- LIVE DATA FETCHING VIA YAHOO FINANCE ---
@st.cache_data(ttl=300)
def fetch_live_performance(tickers):
    performance_data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="max")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change_pct = ((current_price - prev_close) / prev_close) * 100
                history_df = hist[['Close']].reset_index()
                history_df.columns = ['Date', 'Close']
                performance_data[ticker] = {
                    "price": float(current_price),
                    "change": float(change_pct),
                    "history": history_df,
                    "market_cap": float(stock.info.get("marketCap", 0) or 0),
                    "pe_ratio": str(stock.info.get("trailingPE", "N/A")),
                    "volume": int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0
                }
            else:
                performance_data[ticker] = {"price": 0.0, "change": 0.0, "history": pd.DataFrame(), "market_cap": 0.0, "pe_ratio": "N/A", "volume": 0}
        except Exception:
            performance_data[ticker] = {"price": 0.0, "change": 0.0, "history": pd.DataFrame(), "market_cap": 0.0, "pe_ratio": "N/A", "volume": 0}
    return performance_data

live_data = fetch_live_performance(filtered_df["ticker"].tolist())

# Safely enrich dataframe columns to avoid typing exceptions
filtered_df["live_price"] = [live_data[t]["price"] for t in filtered_df["ticker"]]
filtered_df["change_pct"] = [live_data[t]["change"] for t in filtered_df["ticker"]]
filtered_df["market_cap"] = [live_data[t]["market_cap"] for t in filtered_df["ticker"]]
filtered_df["pe_ratio"] = [live_data[t]["pe_ratio"] for t in filtered_df["ticker"]]

# --- MAIN LAYOUT ---
left_col, right_col = st.columns([1.2, 1.8], gap="large")

with left_col:
    st.markdown("<div class='section-header'>IPO Full Menu</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #86868B; font-size: 14px; margin-top: -10px; margin-bottom: 16px;'>Select a company to analyze live performance & comparable assets.</p>", unsafe_allow_html=True)
    
    stock_options = filtered_df.apply(lambda r: f"{r['ticker']} — {r['name_en']} ({r['name_cn']})", axis=1).tolist()
    
    if not stock_options:
        st.warning("No listings match the current filter parameters.")
        selected_stock_str = None
    else:
        selected_stock_str = st.selectbox("Directory Selection", stock_options, label_visibility="collapsed")
        
        for idx, row in filtered_df.iterrows():
            badge_class = f"badge-{row['exchange'].lower()}"
            chg = live_data[row['ticker']]['change']
            chg_color = "#34C759" if chg >= 0 else "#FF3B30"
            chg_sign = "+" if chg >= 0 else ""
            
            st.markdown(f"""
            <div class='apple-card' style='padding: 16px; margin-bottom: 12px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <span class='{badge_class}'>{row['exchange']}</span>
                        <span style='font-weight: 600; font-size: 16px; margin-left: 8px;'>{row['name_en']}</span>
                        <span style='color: #86868B; font-size: 14px; margin-left: 4px;'>{row['name_cn']}</span>
                    </div>
                    <div style='text-align: right;'>
                        <div style='font-weight: 600; font-size: 15px;'>{row['ticker']}</div>
                        <div style='color: {chg_color}; font-size: 13px; font-weight: 500;'>{chg_sign}{chg:.2f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with right_col:
    st.markdown("<div class='section-header'>Deep-Dive Analytics Panel</div>", unsafe_allow_html=True)
    
    if selected_stock_str:
        selected_ticker = selected_stock_str.split(" — ")[0]
        selected_row = df_ipo[df_ipo["ticker"] == selected_ticker].iloc[0]
        metrics = live_data[selected_ticker]
        
        st.markdown(f"""
        <div class='apple-card'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                <div>
                    <span class='badge-{selected_row['exchange'].lower()}'>{selected_row['exchange']}</span>
                    <h2 style='margin: 8px 0 4px 0; font-size: 28px; font-weight: 700;'>{selected_row['name_en']} <span style='color: #86868B; font-weight: 400;'>{selected_row['name_cn']}</span></h2>
                    <p style='color: #86868B; font-size: 14px; margin: 0;'>Ticker: <b>{selected_row['ticker']}</b> &bull; Industry: {selected_row['industry']} ({selected_row['subsector']})</p>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 26px; font-weight: 700;'>${metrics['price']:.2f}</div>
                    <div style='color: {'#34C759' if metrics['change'] >= 0 else '#FF3B30'}; font-weight: 600; font-size: 15px;'>
                        {'+' if metrics['change'] >= 0 else ''}{metrics['change']:.2f}% Live Today
                    </div>
                </div>
            </div>
            
            <hr style='border: none; border-top: 1px solid #E5E5EA; margin: 20px 0;'>
            
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <div style='color: #86868B; font-size: 12px; font-weight: 500;'>IPO Issue Price</div>
                    <div style='font-weight: 600; font-size: 16px;'>${selected_row['issue_price']:.2f}</div>
                </div>
                <div>
                    <div style='color: #86868B; font-size: 12px; font-weight: 500;'>Listing Date</div>
                    <div style='font-weight: 600; font-size: 16px;'>{selected_row['ipo_date']}</div>
                </div>
                <div>
                    <div style='color: #86868B; font-size: 12px; font-weight: 500;'>Market Capitalization</div>
                    <div style='font-weight: 600; font-size: 16px;'>${metrics['market_cap']:,.0f}</div>
                </div>
                <div>
                    <div style='color: #86868B; font-size: 12px; font-weight: 500;'>P/E Ratio</div>
                    <div style='font-weight: 600; font-size: 16px;'>{metrics['pe_ratio']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top: 0; font-size: 17px; font-weight: 600;'>Post-IPO Performance Trajectory</h4>", unsafe_allow_html=True)
        
        hist_df = metrics["history"]
        if not hist_df.empty:
            st.line_chart(hist_df.set_index('Date')['Close'], color="#0066CC", height=280)
        else:
            st.info("Performance chart history compiling from Yahoo Finance feed...")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top: 0; font-size: 17px; font-weight: 600;'>Comparable Universe Peers</h4>", unsafe_allow_html=True)
        
        peers = df_ipo[(df_ipo["industry"] == selected_row["industry"]) & (df_ipo["ticker"] != selected_ticker)]
        if peers.empty:
            peers = df_ipo[df_ipo["ticker"] != selected_ticker].head(3)
            
        peer_cols = st.columns(min(len(peers), 3))
        for idx, (_, peer) in enumerate(peers.head(3).iterrows()):
            p_metrics = live_data[peer['ticker']]
            p_chg = p_metrics['change']
            with peer_cols[idx]:
                st.markdown(f"""
                <div style='background: #F5F5F7; padding: 14px; border-radius: 12px;'>
                    <div style='font-size: 12px; color: #86868B;'>{peer['exchange']}</div>
                    <div style='font-weight: 600; font-size: 14px;'>{peer['name_en']}</div>
                    <div style='font-size: 13px; font-weight: 500; color: {'#34C759' if p_chg >= 0 else '#FF3B30'};'>
                        {'+' if p_chg >= 0 else ''}{p_chg:.2f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- BOTTOM SECTION: TOP PERFORMING STOCKS LEADERBOARDS ---
st.markdown("<hr style='border: none; border-top: 1px solid #D2D2D7; margin: 40px 0;'>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>Market Performance Leaderboards</div>", unsafe_allow_html=True)

leaderboard_df = df_ipo.copy()
leaderboard_df["current_price"] = [live_data[t]["price"] for t in leaderboard_df["ticker"]]
leaderboard_df["performance"] = [live_data[t]["change"] for t in leaderboard_df["ticker"]]

l_col1, l_col2, l_col3, l_col4 = st.columns(4)

def render_leaderboard_card(title, data_slice):
    html_content = f"<div class='apple-card'><b>{title}</b><hr style='margin: 8px 0; border-top: 1px solid #E5E5EA;'>"
    for _, row in data_slice.iterrows():
        p_chg = live_data[row['ticker']]['change']
        color = "#34C759" if p_chg >= 0 else "#FF3B30"
        html_content += f"""
        <div style='display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 8px;'>
            <span>{row['name_en']} ({row['exchange']})</span>
            <span style='color: {color}; font-weight: 600;'>{'+' if p_chg >= 0 else ''}{p_chg:.2f}%</span>
        </div>
        """
    html_content += "</div>"
    return html_content

top_overall = leaderboard_df.sort_values(by="performance", ascending=False).head(3)
top_hkex = leaderboard_df[leaderboard_df["exchange"] == "HKEX"].sort_values(by="performance", ascending=False).head(3)
top_sse = leaderboard_df[leaderboard_df["exchange"] == "SSE"].sort_values(by="performance", ascending=False).head(3)
top_szse = leaderboard_df[leaderboard_df["exchange"] == "SZSE"].sort_values(by="performance", ascending=False).head(3)

with l_col1:
    st.markdown(render_leaderboard_card("🏆 Top Overall YTD", top_overall), unsafe_allow_html=True)
with l_col2:
    st.markdown(render_leaderboard_card("🇭🇰 HKEX Leaders (~85)", top_hkex), unsafe_allow_html=True)
with l_col3:
    st.markdown(render_leaderboard_card("🇨🇳 SSE Leaders (~19)", top_sse), unsafe_allow_html=True)
with l_col4:
    st.markdown(render_leaderboard_card("🇨🇳 SZSE Leaders (~16)", top_szse), unsafe_allow_html=True)
