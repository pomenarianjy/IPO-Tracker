import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. Page Configuration & Apple-Aesthetic CSS
st.set_page_config(
    page_title="Jasmine's HK & China IPO Tracker",
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

    /* Hide standard streamlit header/footer for cleaner product page look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Apple-style Card Containers */
    .apple-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .apple-card:hover {
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
    }

    /* Typography Styling */
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

    /* Metric Container */
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

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F5F5F7;
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }
</style>
"""
st.markdown(APPLE_CSS, unsafe_allow_html=True)


# 2. Mock Database Generation (HK & China IPO Universe: 2020-2026)
@st.cache_data
def load_ipo_data():
    np.random.seed(42)
    exchanges = ["HKEX (Main Board)", "SSE (Star Market)", "SZEX (ChiNext)"]
    industries = {
        "Technology": ["Artificial Intelligence", "Cloud & SaaS", "Semiconductors"],
        "Healthcare": ["Biotech", "Medical Devices", "Digital Health"],
        "Consumer": ["E-Commerce", "Food & Beverage", "Apparel"],
        "New Energy": ["EV & Components", "Solar & Wind", "Battery Tech"],
    }

    stocks = [
        {
            "ticker": "09888.HK",
            "eng": "Baidu, Inc.",
            "chi": "百度集团",
            "exchange": "HKEX (Main Board)",
            "year": 2021,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 252.0,
        },
        {
            "ticker": "09988.HK",
            "eng": "Alibaba Group",
            "chi": "阿里巴巴",
            "exchange": "HKEX (Main Board)",
            "year": 2019,
            "industry": "Consumer",
            "sub": "E-Commerce",
            "ipo_price": 176.0,
        },
        {
            "ticker": "688981.SH",
            "eng": "Semiconductor Manufacturing International",
            "chi": "中芯国际",
            "exchange": "SSE (Star Market)",
            "year": 2020,
            "industry": "Technology",
            "sub": "Semiconductors",
            "ipo_price": 27.46,
        },
        {
            "ticker": "300750.SZ",
            "eng": "Contemporary Amperex Technology",
            "chi": "宁德时代",
            "exchange": "SZEX (ChiNext)",
            "year": 2018,
            "industry": "New Energy",
            "sub": "Battery Tech",
            "ipo_price": 25.14,
        },
        {
            "ticker": "09618.HK",
            "eng": "JD.com, Inc.",
            "chi": "京东集团",
            "exchange": "HKEX (Main Board)",
            "year": 2020,
            "industry": "Consumer",
            "sub": "E-Commerce",
            "ipo_price": 226.0,
        },
        {
            "ticker": "03690.HK",
            "eng": "Meituan",
            "chi": "美团",
            "exchange": "HKEX (Main Board)",
            "year": 2018,
            "industry": "Technology",
            "sub": "Cloud & SaaS",
            "ipo_price": 69.0,
        },
        {
            "ticker": "688012.SH",
            "eng": "Advanced Micro-Fabrication Equipment",
            "chi": "中微公司",
            "exchange": "SSE (Star Market)",
            "year": 2019,
            "industry": "Technology",
            "sub": "Semiconductors",
            "ipo_price": 29.01,
        },
        {
            "ticker": "300015.SZ",
            "eng": "Aier Eye Hospital Group",
            "chi": "爱尔眼科",
            "exchange": "SZEX (ChiNext)",
            "year": 2009,
            "industry": "Healthcare",
            "sub": "Medical Devices",
            "ipo_price": 28.0,
        },
        {
            "ticker": "02015.HK",
            "eng": "Li Auto Inc.",
            "chi": "理想汽车",
            "exchange": "HKEX (Main Board)",
            "year": 2021,
            "industry": "New Energy",
            "sub": "EV & Components",
            "ipo_price": 118.0,
        },
        {
            "ticker": "09868.HK",
            "eng": "XPeng Inc.",
            "chi": "小鹏汽车",
            "exchange": "HKEX (Main Board)",
            "year": 2021,
            "industry": "New Energy",
            "sub": "EV & Components",
            "ipo_price": 165.0,
        },
        {
            "ticker": "688223.SH",
            "eng": "Cambricon Technologies",
            "chi": "寒武纪",
            "exchange": "SSE (Star Market)",
            "year": 2020,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 64.39,
        },
        {
            "ticker": "06618.HK",
            "eng": "JD Health International",
            "chi": "京东健康",
            "exchange": "HKEX (Main Board)",
            "year": 2020,
            "industry": "Healthcare",
            "sub": "Digital Health",
            "ipo_price": 70.58,
        },
        {
            "ticker": "09926.HK",
            "eng": "NetEase Cloud Music",
            "chi": "云音乐",
            "exchange": "HKEX (Main Board)",
            "year": 2021,
            "industry": "Technology",
            "sub": "Cloud & SaaS",
            "ipo_price": 205.0,
        },
        {
            "ticker": "300760.SZ",
            "eng": "Mindray Bio-Medical Electronics",
            "chi": "迈瑞医疗",
            "exchange": "SZEX (ChiNext)",
            "year": 2018,
            "industry": "Healthcare",
            "sub": "Medical Devices",
            "ipo_price": 48.8,
        },
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
            "sub": "Artificial Intelligence",
            "ipo_price": 28.0,
        },
        {
            "ticker": "688041.SH",
            "eng": "Hygon Information Technology",
            "chi": "海光信息",
            "exchange": "SSE (Star Market)",
            "year": 2022,
            "industry": "Technology",
            "sub": "Semiconductors",
            "ipo_price": 36.45,
        },
        {
            "ticker": "301269.SZ",
            "eng": "Hangzhou Support Optoelectronic",
            "chi": "联影医疗",
            "exchange": "SZEX (ChiNext)",
            "year": 2022,
            "industry": "Healthcare",
            "sub": "Medical Devices",
            "ipo_price": 109.88,
        },
        {
            "ticker": "02488.HK",
            "eng": "J&T Global Express",
            "chi": "极兔速递",
            "exchange": "HKEX (Main Board)",
            "year": 2023,
            "industry": "Consumer",
            "sub": "E-Commerce",
            "ipo_price": 12.0,
        },
        {
            "ticker": "688271.SH",
            "eng": "Shanghai Friendess Electronic Technology",
            "chi": "柏楚电子",
            "exchange": "SSE (Star Market)",
            "year": 2019,
            "industry": "Technology",
            "sub": "Cloud & SaaS",
            "ipo_price": 68.58,
        },
    ]

    data = []
    dates = pd.date_range(end=datetime.date.today(), periods=500, freq="B")

    for s in stocks:
        # Simulate realistic post-IPO price trajectory
        np.random.seed(len(s["ticker"]))
        returns = np.random.normal(0.0005, 0.02, len(dates))
        price_series = s["ipo_price"] * np.cumprod(1 + returns)

        current_price = price_series[-1]
        change_pct = ((current_price - s["ipo_price"]) / s["ipo_price"]) * 100

        data.append(
            {
                "Ticker": s["ticker"],
                "English Name": s["eng"],
                "Chinese Name": s["chi"],
                "Exchange": s["exchange"],
                "Listing Year": s["year"],
                "Industry": s["industry"],
                "Sub-Sector": s["sub"],
                "IPO Price": s["ipo_price"],
                "Current Price": round(current_price, 2),
                "Total Return (%)": round(change_pct, 2),
                "Market Cap (B)": round(np.random.uniform(15, 350), 2),
                "P/E Ratio": round(np.random.uniform(12, 65), 1),
                "Volume (M)": round(np.random.uniform(1.5, 45.0), 2),
                "Price Series": price_series,
                "Dates": dates,
            }
        )

    return pd.DataFrame(data)


df = load_ipo_data()

# 3. Header Section (Apple aesthetic branding)
st.markdown('<p class="hero-title">Jasmine’s IPO Intelligence</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Comprehensive tracking, screening, and deep valuation analytics for recent Hong Kong and Mainland China public listings.</p>',
    unsafe_allow_html=True,
)

# 4. Sidebar Screening Configuration
st.sidebar.markdown("### **Filters & Controls**")
st.sidebar.markdown(
    '<p style="font-size:12px; color:#86868B;">Refine the company universe instantly.</p>',
    unsafe_allow_html=True,
)

selected_exchanges = st.sidebar.multiselect(
    "Stock Exchange",
    options=df["Exchange"].unique().tolist(),
    default=df["Exchange"].unique().tolist(),
)

selected_years = st.sidebar.multiselect(
    "Listing Year",
    options=[2026, 2025, 2024, 2023, 2022, 2021, 2020],
    default=[2026, 2025, 2024, 2023, 2022, 2021, 2020],
)

selected_industries = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique().tolist(),
    default=df["Industry"].unique().tolist(),
)

# Filter Dataframe based on sidebar options
filtered_df = df[
    df["Exchange"].isin(selected_exchanges)
    & df["Listing Year"].isin(selected_years)
    & df["Industry"].isin(selected_industries)
]

# 5. Main Content Layout: Split Panel (Left: Menu, Right: Deep-Dive Panel)
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

    # Menu table representation
    menu_table = display_df[
        ["Ticker", "English Name", "Chinese Name", "Exchange", "Total Return (%)"]
    ].reset_index(drop=True)

    # Let user pick a ticker easily via selectbox populated from filtered view
    selected_ticker = st.selectbox(
        "Choose Company for Deep Dive",
        options=display_df["Ticker"].tolist(),
        format_func=lambda x: f"{x} - {display_df[display_df['Ticker'] == x]['English Name'].values[0]} ({display_df[display_df['Ticker'] == x]['Chinese Name'].values[0]})",
    )

    st.dataframe(
        menu_table, use_container_width=True, height: int = 400
    )  # type: ignore

with col_right:
    st.markdown("### **Deep-Dive Analytics Panel**")

    if selected_ticker:
        stock_info = df[df["Ticker"] == selected_ticker].iloc[0]

        # Top descriptive summary container
        st.markdown(
            f"""
            <div class="apple-card">
                <h2 style="margin:0; font-size:24px;">{stock_info['English Name']} <span style="color:#86868B; font-weight:400;">{stock_info['Chinese Name']}</span></h2>
                <p style="margin:4px 0 16px 0; font-size:14px; color:#0066CC; font-weight:500;">{stock_info['Ticker']} &bull; {stock_info['Exchange']} &bull; Listed {stock_info['Listing Year']}</p>
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

        # Yahoo Finance / Trusted Source Crucial Metrics layout
        m1, m2, m3 = st.columns(3)
        m1.metric("Market Cap", f"${stock_info['Market Cap (BB)'] if 'Market Cap (BB)' in stock_info else stock_info['Market Cap (B)']}B")
        m2.metric("P/E Ratio", f"{stock_info['P/E Ratio']}x")
        m3.metric("Daily Volume", f"{stock_info['Volume (M)']}M shares")

        # Performance Chart (Plotly customized for Apple minimal aesthetic)
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

        # Comparable Companies from Universe
        st.markdown("#### **Comparable Universe Peers**")
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
st.markdown("### **Top Performing IPOs**")

col_top1, col_top2, col_top3, col_top4 = st.columns(4)

with col_top1:
    st.markdown("#### **Overall Leaders**")
    top_overall = df.nlargest(3, "Total Return (%)")
    for _, row in top_overall.iterrows():
        st.markdown(
            f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#34C759; font-weight:600;'>+{row['Total Return (%)']}%</span>",
            unsafe_allow_html=True,
        )

for idx, exch in enumerate(df["Exchange"].unique()):
    col = [col_top2, col_top3, col_top4][idx]
    with col:
        st.markdown(f"#### **{exch.split()[0]} Leaders**")
        exch_top = df[df["Exchange"] == exch].nlargest(3, "Total Return (%)")
        for _, row in exch_top.iterrows():
            st.markdown(
                f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#34C759; font-weight:600;'>+{row['Total Return (%)']}%</span>",
                unsafe_allow_html=True,
            )
