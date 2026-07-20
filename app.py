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

    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: -0.015em;
        color: #1D1D1F;
    }
    
    .hero-title {
        font-size: 42px;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #1D1D1F;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-size: 17px;
        font-weight: 400;
        color: #86868B;
        margin-bottom: 32px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: #1D1D1F;
    }
    .metric-label {
        font-size: 13px;
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


# 2. Comprehensive Multi-Sector Dataset Generator (2024-2026)
@st.cache_data
def load_ipo_universe():
    master_listings = [
        # --- 2026 Listings ---
        {
            "ticker": "02249.HK",
            "eng": "Nexchip Semiconductor",
            "chi": "中芯集成",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Semiconductors",
            "ipo_price": 32.30,
        },
        {
            "ticker": "02475.HK",
            "eng": "Luxshare Precision",
            "chi": "立讯精密",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Industrials",
            "sub": "Precision Components",
            "ipo_price": 63.28,
        },
        {
            "ticker": "03752.HK",
            "eng": "Rokae Robotics Group",
            "chi": "珞石机器人",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 38.00,
        },
        {
            "ticker": "06880.HK",
            "eng": "Momenta Global Limited",
            "chi": "初速度",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Autonomous Driving AI",
            "ipo_price": 295.60,
        },
        {
            "ticker": "06745.HK",
            "eng": "Befar Group Co., Ltd",
            "chi": "滨化集团",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Materials",
            "sub": "Specialty Chemicals",
            "ipo_price": 3.48,
        },
        {
            "ticker": "02797.HK",
            "eng": "Jiangxi Qiyunshan Food",
            "chi": "齐云山食品",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Consumer",
            "sub": "Food & Beverage",
            "ipo_price": 8.00,
        },
        {
            "ticker": "01770.HK",
            "eng": "DKE Holding Company",
            "chi": "大科控股",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Financials",
            "sub": "Investment Holding",
            "ipo_price": 78.64,
        },
        {
            "ticker": "00537.HK",
            "eng": "Rigol Technologies",
            "chi": "普源精电",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Industrials",
            "sub": "Electronic Test Instruments",
            "ipo_price": 45.98,
        },
        {
            "ticker": "301400.SZ",
            "eng": "Guangdong Intelligent Tech",
            "chi": "广东智能科技",
            "exchange": "SZEX (ChiNext)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 24.50,
        },
        {
            "ticker": "688300.SH",
            "eng": "Suzhou Nano Core",
            "chi": "苏州纳米核心",
            "exchange": "SSE (Star Market)",
            "year": 2026,
            "industry": "Healthcare",
            "sub": "Biotech & Nanotech",
            "ipo_price": 51.20,
        },
        {
            "ticker": "02667.HK",
            "eng": "Beijing Tong Ren Tang Healthcare",
            "chi": "同仁堂医疗",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Healthcare",
            "sub": "Traditional & Modern Pharma",
            "ipo_price": 5.50,
        },
        {
            "ticker": "00668.HK",
            "eng": "Anker Innovations Technology",
            "chi": "安克创新",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Consumer",
            "sub": "Smart Hardware",
            "ipo_price": 99.32,
        },
        {
            "ticker": "06915.HK",
            "eng": "Jiangxi Institute of Biological Products",
            "chi": "江西生物制品",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Healthcare",
            "sub": "Biologics & Vaccines",
            "ipo_price": 11.20,
        },
        {
            "ticker": "03952.HK",
            "eng": "Zhejiang Laifual Drive",
            "chi": "来福谐波",
            "exchange": "HKEX (Main Board)",
            "year": 2026,
            "industry": "Industrials",
            "sub": "Robotics Components",
            "ipo_price": 85.50,
        },

        # --- 2025 Listings ---
        {
            "ticker": "03700.HK",
            "eng": "Contemporary Amperex Technology",
            "chi": "宁德时代",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "New Energy",
            "sub": "Battery Tech",
            "ipo_price": 210.00,
        },
        {
            "ticker": "02607.HK",
            "eng": "Seres Group Co Ltd",
            "chi": "赛力斯",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "New Energy",
            "sub": "EV & Components",
            "ipo_price": 55.00,
        },
        {
            "ticker": "688111.SH",
            "eng": "Jiangsu Hengrui Pharmaceuticals",
            "chi": "恒瑞医药",
            "exchange": "SSE (Star Market)",
            "year": 2025,
            "industry": "Healthcare",
            "sub": "Innovative Pharma",
            "ipo_price": 45.30,
        },
        {
            "ticker": "09688.HK",
            "eng": "Pony AI Inc.",
            "chi": "小马智行",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Technology",
            "sub": "Autonomous Driving",
            "ipo_price": 38.40,
        },
        {
            "ticker": "301200.SZ",
            "eng": "Wuhan Optics Valley Bio",
            "chi": "武汉光谷生物",
            "exchange": "SZEX (ChiNext)",
            "year": 2025,
            "industry": "Healthcare",
            "sub": "Digital Health",
            "ipo_price": 19.80,
        },
        {
            "ticker": "02199.HK",
            "eng": "Zijin Gold International",
            "chi": "紫金黄金国际",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Materials",
            "sub": "Mining & Metals",
            "ipo_price": 44.20,
        },
        {
            "ticker": "01810.HK",
            "eng": "Sany Heavy Industry",
            "chi": "三一重工",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Industrials",
            "sub": "Heavy Machinery",
            "ipo_price": 18.50,
        },
        {
            "ticker": "01428.HK",
            "eng": "Zhejiang Sanhua Intelligent",
            "chi": "三花智控",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Industrials",
            "sub": "Thermal Management",
            "ipo_price": 26.40,
        },
        {
            "ticker": "02319.HK",
            "eng": "Foshan Haitian Flavouring",
            "chi": "海天味业",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Consumer",
            "sub": "Food & Beverage",
            "ipo_price": 48.90,
        },
        {
            "ticker": "09860.HK",
            "eng": "WeRide Inc.",
            "chi": "文远知行",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Technology",
            "sub": "Autonomous Driving",
            "ipo_price": 52.00,
        },
        {
            "ticker": "01688.HK",
            "eng": "Chery Automobile Co Ltd",
            "chi": "奇瑞汽车",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "New Energy",
            "sub": "Automotive",
            "ipo_price": 31.00,
        },
        {
            "ticker": "09988.HK",
            "eng": "Mirxes Holding Company",
            "chi": "觅瑞",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Healthcare",
            "sub": "Cancer Diagnostics",
            "ipo_price": 22.50,
        },
        {
            "ticker": "02588.HK",
            "eng": "IFBH Limited",
            "chi": "IFBH",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Consumer",
            "sub": "Beverages & Agri",
            "ipo_price": 11.40,
        },
        {
            "ticker": "01999.HK",
            "eng": "Nanshan Aluminium International",
            "chi": "南山铝业国际",
            "exchange": "HKEX (Main Board)",
            "year": 2025,
            "industry": "Materials",
            "sub": "Aluminum Products",
            "ipo_price": 15.80,
        },

        # --- 2024 Listings ---
        {
            "ticker": "02511.HK",
            "eng": "Horizon Robotics",
            "chi": "地平线机器人",
            "exchange": "HKEX (Main Board)",
            "year": 2024,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 3.99,
        },
        {
            "ticker": "09660.HK",
            "eng": "Black Sesame Technologies",
            "chi": "黑芝麻智能",
            "exchange": "HKEX (Main Board)",
            "year": 2024,
            "industry": "Technology",
            "sub": "Autonomous Chips",
            "ipo_price": 28.00,
        },
        {
            "ticker": "688520.SH",
            "eng": "Aerospatial High-Tech",
            "chi": "航天高科",
            "exchange": "SSE (Star Market)",
            "year": 2024,
            "industry": "New Energy",
            "sub": "Solar & Aerospace",
            "ipo_price": 42.10,
        },
        {
            "ticker": "02500.HK",
            "eng": "Rici Healthcare Group",
            "chi": "瑞慈医疗",
            "exchange": "HKEX (Main Board)",
            "year": 2024,
            "industry": "Healthcare",
            "sub": "Medical Services",
            "ipo_price": 14.20,
        },
        {
            "ticker": "02451.HK",
            "eng": "Shanghai ChicMax Cosmetic",
            "chi": "上美股份",
            "exchange": "HKEX (Main Board)",
            "year": 2024,
            "industry": "Consumer",
            "sub": "Beauty & Personal Care",
            "ipo_price": 25.20,
        },
        {
            "ticker": "02459.HK",
            "eng": "Keeping Ltd",
            "chi": "卡淘科技",
            "exchange": "HKEX (Main Board)",
            "year": 2024,
            "industry": "Consumer",
            "sub": "Digital E-Commerce",
            "ipo_price": 10.50,
        },
        {
            "ticker": "09898.HK",
            "eng": "Mobvoi Inc.",
            "chi": "出门问问",
            "exchange": "HKEX (Main Board)",
            "year": 2024,
            "industry": "Technology",
            "sub": "Conversational AI",
            "ipo_price": 3.80,
        },
        {
            "ticker": "02555.HK",
            "eng": "Jingdong Property",
            "chi": "京东产发",
            "exchange": "HKEX (Main Board)",
            "year": 2024,
            "industry": "Real Estate",
            "sub": "Logistics Real Estate",
            "ipo_price": 18.30,
        },
    ]

    processed_data = []
    dates = pd.date_range(end=datetime.date.today(), periods=300, freq="B")

    for item in master_listings:
        np.random.seed(sum(ord(c) for c in item["ticker"]))
        simulated_returns = np.random.normal(0.0008, 0.022, len(dates))
        prices = item["ipo_price"] * np.cumprod(1 + simulated_returns)
        current_price = round(float(prices[-1]), 2)
        total_return_pct = round(
            ((current_price - item["ipo_price"]) / item["ipo_price"]) * 100, 2
        )

        processed_data.append(
            {
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
                "Market Cap (B)": round(np.random.uniform(15, 350), 2),
                "P/E Ratio": round(np.random.uniform(12, 58), 1),
                "Volume (M)": round(np.random.uniform(1.5, 40.0), 2),
                "Price Series": prices,
                "Dates": dates,
            }
        )

    return pd.DataFrame(processed_data)


df = load_ipo_universe()

# 3. Header Section
st.markdown('<p class="hero-title">Jasmine’s IPO Intelligence</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Comprehensive multi-sector tracking across HKEX and Mainland China exchanges (2024–2026).</p>',
    unsafe_allow_html=True,
)

# 4. Sidebar Screening Configuration (Restricted strictly to 2024-2026)
st.sidebar.markdown("### **Filters & Controls**")
st.sidebar.markdown(
    '<p style="font-size:12px; color:#86868B;">Filtered for 2024–2026 IPO cohort.</p>',
    unsafe_allow_html=True,
)

selected_exchanges = st.sidebar.multiselect(
    "Stock Exchange",
    options=df["Exchange"].unique().tolist(),
    default=df["Exchange"].unique().tolist(),
)

selected_years = st.sidebar.multiselect(
    "Listing Year",
    options=[2026, 2025, 2024],
    default=[2026, 2025, 2024],
)

selected_industries = st.sidebar.multiselect(
    "Industry Sector",
    options=df["Industry"].unique().tolist(),
    default=df["Industry"].unique().tolist(),
)

# Filter Dataframe
filtered_df = df[
    df["Exchange"].isin(selected_exchanges)
    & df["Listing Year"].isin(selected_years)
    & df["Industry"].isin(selected_industries)
]

# 5. Main Content Layout: Split Panel
col_left, col_right = st.columns([1.1, 1.4], gap="large")

with col_left:
    st.markdown("### **Full Market Directory**")
    st.markdown(
        '<p style="font-size:13px; color:#86868B;">Select a company row or search below to review indicators.</p>',
        unsafe_allow_html=True,
    )

    search_query = st.text_input(
        "Quick Search", placeholder="Search ticker, English or Chinese name..."
    )

    display_df = filtered_df[
        filtered_df["Ticker"].str.contains(search_query, case=False, na=False)
        | filtered_df["English Name"].str.contains(
            search_query, case=False, na=False
        )
        | filtered_df["Chinese Name"].str.contains(
            search_query, case=False, na=False
        )
    ]

    menu_table = display_df[
        [
            "Ticker",
            "English Name",
            "Industry",
            "Listing Year",
            "Total Return (%)",
        ]
    ].reset_index(drop=True)

    if not display_df.empty:
        selected_ticker = st.selectbox(
            "Choose Company for Deep Dive",
            options=display_df["Ticker"].tolist(),
            format_func=lambda x: f"{x} - {display_df[display_df['Ticker'] == x]['English Name'].values[0]} ({display_df[display_df['Ticker'] == x]['Chinese Name'].values[0]})",
        )
    else:
        selected_ticker = None
        st.warning(
            "No companies match your active filters. Please adjust the sidebar options."
        )

    st.dataframe(menu_table, use_container_width=True, height=400)

with col_right:
    st.markdown("### **Deep-Dive Analytics Panel**")

    if selected_ticker:
        stock_info = df[df["Ticker"] == selected_ticker].iloc[0]

        st.markdown(
            f"""
            <div class="apple-card">
                <h2 style="margin:0; font-size:24px;">{stock_info['English Name']} <span style="color:#86868B; font-weight:400;">{stock_info['Chinese Name']}</span></h2>
                <p style="margin:4px 0 16px 0; font-size:14px; color:#0066CC; font-weight:500;">{stock_info['Ticker']} &bull; {stock_info['Exchange']} &bull; Listed {stock_info['Listing Year']} ({stock_info['Industry']} / {stock_info['Sub-Sector']})</p>
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
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("Market Cap", f"${stock_info['Market Cap (B)']}B")
        m2.metric("P/E Ratio", f"{stock_info['P/E Ratio']}x")
        m3.metric("Daily Volume", f"{stock_info['Volume (M)']}M shares")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=stock_info["Dates"],
                y=stock_info["Price Series"],
                mode="lines",
                name="Post-IPO Performance",
                line=dict(
                    color=(
                        "#34C759"
                        if stock_info["Total Return (%)"] >= 0
                        else "#FF3B30"
                    ),
                    width=2.5,
                ),
            )
        )
        fig.add_hline(
            y=stock_info["IPO Price"],
            line_dash="dot",
            line_color="#86868B",
            annotation_text="IPO Baseline",
            annotation_position="bottom right",
        )

        fig.update_layout(
            title="<b>Price Trajectory (IPO to Date)</b>",
            template="simple_white",
            margin=dict(l=10, r=10, t=40, b=10),
            height=300,
            hovermode="x unified",
            font=dict(family="-apple-system, BlinkMacSystemFont, sans-serif"),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### **Comparable Sector Peers**")
        peers = df[
            (df["Industry"] == stock_info["Industry"])
            & (df["Ticker"] != stock_info["Ticker"])
        ].head(3)
        if not peers.empty:
            peer_display = peers[
                [
                    "Ticker",
                    "English Name",
                    "Exchange",
                    "Total Return (%)",
                    "P/E Ratio",
                ]
            ]
            st.dataframe(peer_display, use_container_width=True)
        else:
            st.info("No direct peers available in the current active filter.")

# 6. Global & Exchange-Specific Top Performers Section
st.markdown("---")
st.markdown("### **Top Performing IPOs (2024-2026 Cohort)**")

col_top1, col_top2, col_top3, col_top4 = st.columns(4)

with col_top1:
    st.markdown("#### **Overall Leaders**")
    top_overall = df.nlargest(3, "Total Return (%)")
    for _, row in top_overall.iterrows():
        st.markdown(
            f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#34C759; font-weight:600;'>+{row['Total Return (%)']}%</span>",
            unsafe_allow_html=True,
        )

exchanges_list = df["Exchange"].unique().tolist()
for idx, exch in enumerate(exchanges_list[:3]):
    col = [col_top2, col_top3, col_top4][idx]
    with col:
        st.markdown(f"#### **{exch.split()[0]} Leaders**")
        exch_top = df[df["Exchange"] == exch].nlargest(3, "Total Return (%)")
        for _, row in exch_top.iterrows():
            st.markdown(
                f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#34C759; font-weight:600;'>+{row['Total Return (%)']}%</span>",
                unsafe_allow_html=True,
            )
