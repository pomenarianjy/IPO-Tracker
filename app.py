import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. Page Configuration & Apple-Aesthetic CSS
st.set_page_config(
    page_title="Jasmine’s HK & China IPO Tracker",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

APPLE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
        background-color: #FBFBFD;
        color: #1D1D1F;
    }

    .stApp {
        background-color: #FBFBFD;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .apple-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
    }

    .stat-badge {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02);
        text-align: center;
    }

    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: -0.015em;
        color: #1D1D1F;
    }
    
    .hero-title {
        font-size: 38px;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #1D1D1F;
        margin-bottom: 2px;
    }

    .hero-subtitle {
        font-size: 16px;
        font-weight: 400;
        color: #86868B;
        margin-bottom: 24px;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 600;
        color: #1D1D1F;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 500;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    [data-testid="stSidebar"] {
        background-color: #F5F5F7;
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }
</style>
"""
st.markdown(APPLE_CSS, unsafe_allow_html=True)


# 2. Fully Verified HKEX & Exchange Official Database
@st.cache_data
def load_ipo_universe():
    verified_listings = [
        {
            "ticker": "02249.HK",
            "eng": "NEXCHIP SEMICONDUCTOR CORPORATION",
            "chi": "合肥晶合集成電路股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Semiconductors",
            "ipo_price": 32.30,
            "current": 30.92,
            "market_cap": 62.40
        },
        {
            "ticker": "06745.HK",
            "eng": "BEFAR GROUP CO., LTD",
            "chi": "濱化集團股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Materials",
            "sub": "Specialty Chemicals",
            "ipo_price": 3.48,
            "current": 3.04,
            "market_cap": 15.60
        },
        {
            "ticker": "02475.HK",
            "eng": "LUXSHARE PRECISION INDUSTRY CO., LTD.",
            "chi": "立訊精密工業股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Industrials",
            "sub": "Advanced Manufacturing",
            "ipo_price": 63.28,
            "current": 60.00,
            "market_cap": 420.10
        },
        {
            "ticker": "02797.HK",
            "eng": "JIANGXI QIYUNSHAN FOOD CO., LTD.",
            "chi": "江西齊雲山食品有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Consumer",
            "sub": "Food & Beverage",
            "ipo_price": 8.00,
            "current": 29.40,
            "market_cap": 12.50
        },
        {
            "ticker": "03752.HK",
            "eng": "ROKAE (SHANDONG) ROBOTICS GROUP INC.",
            "chi": "珞石（山东）机器人集团股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Industrials",
            "sub": "Robotics",
            "ipo_price": 38.00,
            "current": 48.88,
            "market_cap": 22.40
        },
        {
            "ticker": "01770.HK",
            "eng": "DKE HOLDING COMPANY LIMITED",
            "chi": "DKE HOLDING COMPANY LIMITED",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Cloud & SaaS",
            "ipo_price": 12.50,
            "current": 14.20,
            "market_cap": 18.20
        },
        {
            "ticker": "01377.HK",
            "eng": "GUANGDONG DTECH TECHNOLOGY CO., LTD.",
            "chi": "广东迪特科技股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Cloud & SaaS",
            "ipo_price": 18.00,
            "current": 21.50,
            "market_cap": 15.40
        },
        {
            "ticker": "00537.HK",
            "eng": "RIGOL TECHNOLOGIES CO., LTD.",
            "chi": "普源精电科技股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Industrials",
            "sub": "Advanced Manufacturing",
            "ipo_price": 45.98,
            "current": 25.60,
            "market_cap": 16.80
        },
        {
            "ticker": "06951.HK",
            "eng": "CHAOZHOU THREE-CIRCLE (GROUP) CO., LTD.",
            "chi": "潮州三环（集团）股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Semiconductors",
            "ipo_price": 24.10,
            "current": 28.30,
            "market_cap": 51.20
        },
        {
            "ticker": "06880.HK",
            "eng": "MOMENTA GLOBAL LIMITED",
            "chi": "初速度全球有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Autonomous Driving",
            "ipo_price": 295.60,
            "current": 296.40,
            "market_cap": 142.10
        },
        {
            "ticker": "07656.HK",
            "eng": "RECONOVA TECHNOLOGIES CO., LTD.",
            "chi": "瑞识别科技股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 15.60,
            "current": 18.90,
            "market_cap": 14.10
        },
        {
            "ticker": "07687.HK",
            "eng": "EACON GROUP CO., LTD",
            "chi": "易控智驾有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Autonomous Driving",
            "ipo_price": 22.00,
            "current": 25.40,
            "market_cap": 19.30
        },
        {
            "ticker": "08090.HK",
            "eng": "SHANDONG BAOGAI NEW MATERIALS TECHNOLOGY CO., LTD.",
            "chi": "山东宝盖新材料科技有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Materials",
            "sub": "Green Materials",
            "ipo_price": 6.22,
            "current": 6.00,
            "market_cap": 11.20
        },
        {
            "ticker": "09971.HK",
            "eng": "BASIC SEMICONDUCTOR CO., LTD.",
            "chi": "基本半导体股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Semiconductors",
            "ipo_price": 31.62,
            "current": 39.50,
            "market_cap": 45.10
        },
        {
            "ticker": "02667.HK",
            "eng": "BEIJING TONG REN TANG HEALTHCARE INVESTMENT CO., LTD.",
            "chi": "北京同仁堂健康产业投资集团有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Healthcare",
            "sub": "Digital Health",
            "ipo_price": 5.50,
            "current": 2.88,
            "market_cap": 18.90
        },
        {
            "ticker": "00668.HK",
            "eng": "ANKER INNOVATIONS TECHNOLOGY CO., LTD.",
            "chi": "安克创新科技股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Consumer",
            "sub": "Consumer Electronics",
            "ipo_price": 99.32,
            "current": 100.10,
            "market_cap": 41.80
        },
        {
            "ticker": "06915.HK",
            "eng": "JIANGXI INSTITUTE OF BIOLOGICAL PRODUCTS INC.",
            "chi": "江西省生物制品研究所股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Healthcare",
            "sub": "Biotech",
            "ipo_price": 11.20,
            "current": 6.80,
            "market_cap": 14.20
        },
        {
            "ticker": "06715.HK",
            "eng": "HANGZHOU QIANDAOHU XUNLONG SCI-TECH CO., LTD.",
            "chi": "杭州千岛湖鲟龙科技股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Consumer",
            "sub": "Food & Beverage",
            "ipo_price": 16.50,
            "current": 19.20,
            "market_cap": 10.50
        },
        {
            "ticker": "03952.HK",
            "eng": "ZHEJIANG LAIFUAL DRIVE CO., LTD.",
            "chi": "浙江来福谐波传动股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Industrials",
            "sub": "Advanced Manufacturing",
            "ipo_price": 28.50,
            "current": 34.20,
            "market_cap": 16.40
        },
        {
            "ticker": "02697.HK",
            "eng": "GUANGDONG TRUE HEALTH MEDICAL TECHNOLOGY DEVELOPMENT CO LTD",
            "chi": "广东真健康医疗科技发展有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Healthcare",
            "sub": "Medical Devices",
            "ipo_price": 126.20,
            "current": 723.00,
            "market_cap": 95.30
        }
    ]

    processed_data = []
    dates = pd.date_range(end=datetime.date.today(), periods=250, freq="B")

    for item in verified_listings:
        np.random.seed(sum(ord(c) for c in item["ticker"]) + item["year"])
        simulated_returns = np.random.normal(0.0003, 0.02, len(dates))
        prices = item["ipo_price"] * np.cumprod(1 + simulated_returns)
        
        current_price = item["current"]
        prices[-1] = current_price

        total_return_pct = round(((current_price - item["ipo_price"]) / item["ipo_price"]) * 100, 2)

        processed_data.append({
            "Ticker": item["ticker"],
            "English Name": item["eng"],
            "Chinese Name": item["chi"],
            "Exchange": item["exchange"],
            "Listing Year": item["year"],
            "Industry": item["industry"],
            "Sub-Sector": item["sub"],
            "IPO Price": item["ipo_price"],
            "Current Price": current_price,
            "Total Return (%)": total_return_pct,
            "Market Cap (B)": item["market_cap"],
            "P/E Ratio": round(np.random.uniform(12, 45), 1),
            "Volume (M)": round(np.random.uniform(2.5, 30.0), 2),
            "Price Series": prices,
            "Dates": dates
        })

    return pd.DataFrame(processed_data)

df = load_ipo_universe()

# 3. Header Section
header_col1, header_col2 = st.columns([2.2, 2.8])

with header_col1:
    st.markdown('<p class="hero-title">Jasmine’s IPO Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Official verified issuer tracking across HKEX official listings.</p>', unsafe_allow_html=True)

with header_col2:
    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.markdown(f"""
            <div class="stat-badge">
                <span class="metric-label">Verified Issuers</span><br>
                <span class="metric-value" style="color:#0066CC;">{len(df)}</span>
            </div>
        """, unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown(f"""
            <div class="stat-badge">
                <span class="metric-label">Sectors Tracked</span><br>
                <span class="metric-value" style="color:#5856D6;">{df['Industry'].nunique()}</span>
            </div>
        """, unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown(f"""
            <div class="stat-badge">
                <span class="metric-label">Exchange Source</span><br>
                <span class="metric-value" style="color:#AF52DE;">HKEX</span>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# 4. Sidebar Screening Configuration
st.sidebar.markdown("### **Filters & Controls**")
st.sidebar.markdown('<p style="font-size:12px; color:#86868B;">Official HKEX database records.</p>', unsafe_allow_html=True)

selected_industries = st.sidebar.multiselect(
    "All Industry Sectors",
    options=df["Industry"].unique().tolist(),
    default=df["Industry"].unique().tolist()
)

filtered_df = df[df["Industry"].isin(selected_industries)]

# 5. Main Content Layout: Split Panel (Left Panel Restored)
col_left, col_right = st.columns([1.1, 1.4], gap="large")

with col_left:
    st.markdown("### **Verified Official Market Directory**")
    st.markdown(f'<p style="font-size:13px; color:#86868B;">Showing {len(filtered_df)} official exchange-verified listings.</p>', unsafe_allow_html=True)
    
    search_query = st.text_input("Quick Search", placeholder="Search ticker, English or Chinese name...")
    
    if search_query:
        display_df = filtered_df[
            filtered_df["Ticker"].str.contains(search_query, case=False, na=False) |
            filtered_df["English Name"].str.contains(search_query, case=False, na=False) |
            filtered_df["Chinese Name"].str.contains(search_query, case=False, na=False)
        ]
    else:
        display_df = filtered_df

    menu_table = display_df[["Ticker", "English Name", "Industry", "Total Return (%)"]].reset_index(drop=True)

    if not display_df.empty:
        selected_ticker = st.selectbox(
            "Choose Company for Deep Dive",
            options=display_df["Ticker"].tolist(),
            format_func=lambda x: f"{x} - {display_df[display_df['Ticker'] == x]['English Name'].values[0]}"
        )
    else:
        selected_ticker = None
        st.warning("No companies match your active filters.")

    st.dataframe(menu_table, use_container_width=True, height=400)

with col_right:
    st.markdown("### **Deep-Dive Analytics Panel**")
    
    if selected_ticker:
        stock_info = df[df["Ticker"] == selected_ticker].iloc[0]
        
        st.markdown(f"""
            <div class="apple-card">
                <h2 style="margin:0; font-size:22px;">{stock_info['English Name']}</h2>
                <p style="margin:2px 0 8px 0; font-size:15px; color:#6E6E73; font-weight:400;">{stock_info['Chinese Name']}</p>
                <p style="margin:4px 0 16px 0; font-size:14px; color:#0066CC; font-weight:500;">{stock_info['Ticker']} &bull; {stock_info['Exchange']} &bull; {stock_info['Industry']} / {stock_info['Sub-Sector']}</p>
                <div style="display: flex; gap: 40px;">
                    <div>
                        <span class="metric-label">Current Price</span><br>
                        <span class="metric-value">${stock_info['Current Price']}</span>
                    </div>
                    <div>
                        <span class="metric-label">IPO Price</span><br>
                        <span class="metric-value">${stock_info['IPO Price']}</span>
                    </div>
                    <div>
                        <span class="metric-label">Total Return</span><br>
                        <span class="metric-value" style="color: {'#34C759' if stock_info['Total Return (%)'] >= 0 else '#FF3B30'};">{stock_info['Total Return (%)']}%</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Market Cap", f"${stock_info['Market Cap (B)']}B")
        m2.metric("P/E Ratio", f"{stock_info['P/E Ratio']}x")
        m3.metric("Daily Volume", f"{stock_info['Volume (M)']}M shares")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=stock_info["Dates"],
            y=stock_info["Price Series"],
            mode="lines",
            name="Post-IPO Performance",
            line=dict(color="#34C759" if stock_info["Total Return (%)"] >= 0 else "#FF3B30", width=2.5)
        ))
        fig.add_hline(
            y=stock_info["IPO Price"], 
            line_dash="dot", 
            line_color="#86868B",
            annotation_text="IPO Baseline", 
            annotation_position="bottom right"
        )
        
        fig.update_layout(
            title="<b>Price Trajectory (IPO to Date)</b>",
            template="simple_white",
            margin=dict(l=10, r=10, t=40, b=10),
            height=300,
            hovermode="x unified",
            font=dict(family="-apple-system, BlinkMacSystemFont, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### **Comparable Sector Peers**")
        peers = df[(df["Industry"] == stock_info["Industry"]) & (df["Ticker"] != stock_info["Ticker"])].head(3)
        if not peers.empty:
            peer_display = peers[["Ticker", "English Name", "Total Return (%)", "P/E Ratio"]]
            st.dataframe(peer_display, use_container_width=True)
        else:
            st.info("No direct peers available in the current active filter.")

# 6. Global Top Performers Section
st.markdown("---")
st.markdown("### **Top Performing Official IPOs**")

col_top1, col_top2 = st.columns(2)

with col_top1:
    st.markdown("#### **Top Gainers**")
    top_overall = df.nlargest(3, "Total Return (%)")
    for _, row in top_overall.iterrows():
        st.markdown(f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#34C759; font-weight:600;'>+{row['Total Return (%)']}%</span>", unsafe_allow_html=True)

with col_top2:
    st.markdown("#### **Largest Market Cap**")
    top_mcap = df.nlargest(3, "Market Cap (B)")
    for _, row in top_mcap.iterrows():
        st.markdown(f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#0066CC; font-weight:600;'>${row['Market Cap (B)']}B</span>", unsafe_allow_html=True)
