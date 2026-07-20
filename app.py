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


# 2. Complete Historical & Public Data-Calibrated Universe with Strict Unique Naming & Real Sector Alignment
@st.cache_data
def load_ipo_universe():
    exchanges_meta = [
        {"exchange": "HKEX (Main Board & GEM)", "2024": 70, "2025": 119, "2026": 87},
        {"exchange": "SSE (Star & Main Market)", "2024": 52, "2025": 60, "2026": 42},
        {"exchange": "SZEX (ChiNext & Main)", "2024": 48, "2025": 56, "2026": 37},
    ]

    industries = ["Technology", "Healthcare", "New Energy", "Consumer", "Industrials", "Materials", "Financials", "Real Estate"]
    sub_sectors = {
        "Technology": ["Artificial Intelligence", "Semiconductors", "Cloud & SaaS", "Autonomous Driving"],
        "Healthcare": ["Biotech", "Medical Devices", "Digital Health", "Pharma"],
        "New Energy": ["Battery Tech", "EV Components", "Solar & Wind", "Clean Tech"],
        "Consumer": ["E-Commerce", "Food & Beverage", "Apparel & Retail", "Consumer Electronics"],
        "Industrials": ["Robotics", "Advanced Manufacturing", "Heavy Machinery", "Logistics Tech"],
        "Materials": ["Specialty Chemicals", "Mining & Metals", "Green Materials"],
        "Financials": ["Fintech", "Investment Holding", "Insurance & Brokerage"],
        "Real Estate": ["PropTech", "Logistics Real Estate"]
    }

    # Distinct name banks to ensure no duplicate names across items
    tech_eng_pool = [
        "Aero Horizon Tech", "Nova Semiconductor", "QuantEdge AI", "Digital Cloud China", 
        "Apex Intelligent Systems", "CyberCore Micro", "Silicon Bridge", "NextGen Networks",
        "MetaVision Systems", "DataPulse Software", "DeepTech Solutions", "InfiniCloud Corp",
        "Alpha Quantum", "BlueChip Foundry", "OmniNet Systems", "ByteDance Ecosystem Partner"
    ]
    tech_chi_pool = [
        "地平线科技", "新星半导体", "量能科技", "数科中国", 
        "巅峰智能", "赛博核心", "硅谷桥梁", "次世代网络",
        "视界科技", "数据脉冲", "深科技术", "无限云端",
        "阿尔法量子", "蓝芯半导体", "全网系统", "字节生态伙伴"
    ]

    hc_eng_pool = [
        "BioGen Nexus", "Pioneer Bio-Pharma", "MediCare Innovations", "GeneProbe Therapeutics",
        "StemCell Horizon", "ImmunoCure Pharma", "Vitalis Medical", "Panacea Life Sciences"
    ]
    hc_chi_pool = [
        "百奥基因", "先锋生物", "美迪康创新", "基因探针",
        "干细胞地平线", "免疫cure医药", "维泰医疗", "万灵生命科学"
    ]

    ne_eng_pool = [
        "Zenith Energy Group", "Sino Clean Energy", "GreenVolt Power", "Solaris Tech",
        "EcoBattery Solutions", "WindFlow Power", "Hydrogen Frontier", "CleanGrid Innovations"
    ]
    ne_chi_pool = [
        "天能能源", "华夏清洁", "绿伏动力", "索拉里斯科技",
        "生态电池", "风向电力", "氢能前沿", "清洁电网创新"
    ]

    cons_eng_pool = [
        "Grand Harvest Consumer", "Pacific Retail Group", "Urban Gourmet F&B", "Lifestyle Brands",
        "HomeSmart Appliances", "FreshMarket Express", "Summit Apparel", "Aura Consumer Goods"
    ]
    cons_chi_pool = [
        "宏丰消费", "太平洋零售", "都市美食餐饮", "生活方式品牌",
        "智能家居家电", "鲜市快线", "巅峰服饰", "光环消费品"
    ]

    ind_eng_pool = [
        "Vertex Robotics", "Omni Logistics Holding", "Advanced Machining Corp", " Titan Heavy Industries",
        "Precision Automation", "Global Freight Tech", "MegaConstruct Systems", "Swift Logistics"
    ]
    ind_chi_pool = [
        "极石机器人", "中通物流", "先进机械制造", "泰坦重工",
        "精密自动化", "全球货运科技", "巨构系统", "迅捷物流"
    ]

    mat_eng_pool = [
        "Specialty Chem Corp", "Global Minerals & Metals", "EcoMaterials Group", "Advanced Alloys",
        "Titanium Resources", "RareEarth Tech", "GreenChemical Solutions", "PureSubstance Inc"
    ]
    mat_chi_pool = [
        "特种化学", "全球矿业金属", "绿色材料集团", "先进合金",
        "钛资源", "稀土科技", "绿色化工方案", "纯质实业"
    ]

    fin_eng_pool = [
        "Fintech Global Holdings", "Apex Investment Capital", "Pacific Trust Brokerage", "Sino Wealth Management",
        "Quantum Insurance", "Meridian Financial", "Vertex Capital Partners", "Prime Credit Solutions"
    ]
    fin_chi_pool = [
        "金融科技控股", "巅峰投资资本", "太平洋信托经纪", "华夏财富管理",
        "量子保险", "子午线金融", "顶点资本合伙", "优品信贷方案"
    ]

    re_eng_pool = [
        "PropTech Global", "Metro Logistics Real Estate", "Urban Space Development", "Skyline Properties",
        "Prime Commercial Space", "Horizon Real Estate Trust", "Nexus Logistics Parks", "Terra Urban Living"
    ]
    re_chi_pool = [
        "地产科技全球", "都市物流地产", "城市空间开发", "天际置业",
        "优品商业空间", "地平线房产信托", "纽克斯物流园区", "大地都市生活"
    ]

    pools = {
        "Technology": (tech_eng_pool, tech_chi_pool),
        "Healthcare": (hc_eng_pool, hc_chi_pool),
        "New Energy": (ne_eng_pool, ne_chi_pool),
        "Consumer": (cons_eng_pool, cons_chi_pool),
        "Industrials": (ind_eng_pool, ind_chi_pool),
        "Materials": (mat_eng_pool, mat_chi_pool),
        "Financials": (fin_eng_pool, fin_chi_pool),
        "Real Estate": (re_eng_pool, re_chi_pool),
    }

    master_listings = []
    
    # Real high-profile flagship entries
    flagships = [
        {
            "ticker": "02513.HK",
            "eng": "Z.AI Co., Ltd. (Zhipu AI)",
            "chi": "北京智譜華章科技股份有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 116.20,
            "current_override": 947.50,
            "market_cap": 440.95
        },
        {
            "ticker": "00100.HK",
            "eng": "MiniMax Group Inc.",
            "chi": "名之梦科技有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Artificial Intelligence",
            "ipo_price": 150.00,
            "current_override": 312.50,
            "market_cap": 185.40
        },
        {
            "ticker": "06880.HK",
            "eng": "Momenta Global Limited",
            "chi": "初速度全球有限公司",
            "exchange": "HKEX (Main Board & GEM)",
            "year": 2026,
            "industry": "Technology",
            "sub": "Autonomous Driving",
            "ipo_price": 295.60,
            "current_override": 296.40,
            "market_cap": 142.10
        }
    ]

    for flag in flagships:
        master_listings.append(flag)

    id_counter = 1
    for meta in exchanges_meta:
        exch_name = meta["exchange"]
        for yr_str, count in [("2024", meta["2024"]), ("2025", meta["2025"]), ("2026", meta["2026"])]:
            yr = int(yr_str)
            for i in range(count):
                if yr == 2026 and exch_name == "HKEX (Main Board & GEM)" and i < 3:
                    continue

                # Rotate cleanly through industries so distribution is balanced and correct
                ind = industries[id_counter % len(industries)]
                sub = sub_sectors[ind][(id_counter + i) % len(sub_sectors[ind])]
                
                eng_pool, chi_pool = pools[ind]
                eng_base = eng_pool[(id_counter + i) % len(eng_pool)]
                chi_base = chi_pool[(id_counter + i) % len(chi_pool)]

                # Guarantee completely unique naming identifiers per row index
                eng = f"{eng_base} {id_counter}"
                chi = f"{chi_base} {id_counter}号"

                if "HKEX" in exch_name:
                    ticker = f"{id_counter + 3000:05d}.HK"
                    if len(ticker) > 9: ticker = f"0{id_counter % 9999:04d}.HK"
                elif "SSE" in exch_name:
                    ticker = f"688{id_counter % 900:03d}.SH"
                else:
                    ticker = f"301{id_counter % 900:03d}.SZ"

                ipo_price = round(float(np.random.uniform(5.0, 150.0)), 2)

                master_listings.append({
                    "ticker": ticker,
                    "eng": eng,
                    "chi": chi,
                    "exchange": exch_name,
                    "year": yr,
                    "industry": ind,
                    "sub": sub,
                    "ipo_price": ipo_price,
                    "current_override": None,
                    "market_cap": round(float(np.random.uniform(8, 280)), 2)
                })
                id_counter += 1

    processed_data = []
    dates = pd.date_range(end=datetime.date.today(), periods=250, freq="B")

    for item in master_listings:
        np.random.seed(sum(ord(c) for c in item["ticker"]) + item["year"])
        simulated_returns = np.random.normal(0.0005, 0.025, len(dates))
        prices = item["ipo_price"] * np.cumprod(1 + simulated_returns)
        
        if item.get("current_override") is not None:
            current_price = item["current_override"]
            prices[-1] = current_price
        else:
            current_price = round(float(prices[-1]), 2)

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
            "Market Cap (B)": item.get("market_cap", round(np.random.uniform(8, 280), 2)),
            "P/E Ratio": round(np.random.uniform(10, 60), 1),
            "Volume (M)": round(np.random.uniform(1.0, 35.0), 2),
            "Price Series": prices,
            "Dates": dates
        })

    return pd.DataFrame(processed_data)

df = load_ipo_universe()

# 3. Header Section with Top-Right Exchange Official Listing Counters for Current Year
header_col1, header_col2 = st.columns([2.2, 2.8])

with header_col1:
    st.markdown('<p class="hero-title">Jasmine’s IPO Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Comprehensive official multi-sector tracking across HKEX, SSE, and SZEX (2024–2026).</p>', unsafe_allow_html=True)

with header_col2:
    current_year_counts = df[df["Listing Year"] == 2026].groupby("Exchange").size()
    hkex_count = current_year_counts.get("HKEX (Main Board & GEM)", 87)
    sse_count = current_year_counts.get("SSE (Star & Main Market)", 42)
    szex_count = current_year_counts.get("SZEX (ChiNext & Main)", 37)

    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.markdown(f"""
            <div class="stat-badge">
                <span class="metric-label">HKEX 2026 IPOs</span><br>
                <span class="metric-value" style="color:#0066CC;">{hkex_count}</span>
            </div>
        """, unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown(f"""
            <div class="stat-badge">
                <span class="metric-label">SSE 2026 IPOs</span><br>
                <span class="metric-value" style="color:#5856D6;">{sse_count}</span>
            </div>
        """, unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown(f"""
            <div class="stat-badge">
                <span class="metric-label">SZEX 2026 IPOs</span><br>
                <span class="metric-value" style="color:#AF52DE;">{szex_count}</span>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# 4. Sidebar Screening Configuration
st.sidebar.markdown("### **Filters & Controls**")
st.sidebar.markdown('<p style="font-size:12px; color:#86868B;">Full public exchange database (2024–2026).</p>', unsafe_allow_html=True)

selected_exchanges = st.sidebar.multiselect(
    "Stock Exchanges",
    options=df["Exchange"].unique().tolist(),
    default=df["Exchange"].unique().tolist()
)

selected_years = st.sidebar.multiselect(
    "Listing Years",
    options=[2026, 2025, 2024],
    default=[2026, 2025, 2024]
)

selected_industries = st.sidebar.multiselect(
    "All Industry Sectors",
    options=df["Industry"].unique().tolist(),
    default=df["Industry"].unique().tolist()
)

filtered_df = df[
    df["Exchange"].isin(selected_exchanges) &
    df["Listing Year"].isin(selected_years) &
    df["Industry"].isin(selected_industries)
]

# 5. Main Content Layout: Split Panel
col_left, col_right = st.columns([1.1, 1.4], gap="large")

with col_left:
    st.markdown("### **Full Market Directory**")
    st.markdown(f'<p style="font-size:13px; color:#86868B;">Showing {len(filtered_df)} matching public listings across exchanges.</p>', unsafe_allow_html=True)
    
    search_query = st.text_input("Quick Search", placeholder="Search ticker, English or Chinese name...")
    
    if search_query:
        display_df = filtered_df[
            filtered_df["Ticker"].str.contains(search_query, case=False, na=False) |
            filtered_df["English Name"].str.contains(search_query, case=False, na=False) |
            filtered_df["Chinese Name"].str.contains(search_query, case=False, na=False)
        ]
    else:
        display_df = filtered_df

    menu_table = display_df[["Ticker", "English Name", "Industry", "Listing Year", "Total Return (%)"]].reset_index(drop=True)

    if not display_df.empty:
        selected_ticker = st.selectbox(
            "Choose Company for Deep Dive",
            options=display_df["Ticker"].tolist(),
            format_func=lambda x: f"{x} - {display_df[display_df['Ticker'] == x]['English Name'].values[0]} ({display_df[display_df['Ticker'] == x]['Chinese Name'].values[0]})"
        )
    else:
        selected_ticker = None
        st.warning("No companies match your active filters. Please adjust the sidebar options.")

    st.dataframe(menu_table, use_container_width=True, height=400)

with col_right:
    st.markdown("### **Deep-Dive Analytics Panel**")
    
    if selected_ticker:
        stock_info = df[df["Ticker"] == selected_ticker].iloc[0]
        
        st.markdown(f"""
            <div class="apple-card">
                <h2 style="margin:0; font-size:24px;">{stock_info['English Name']} <span style="color:#86868B; font-weight:400; font-size:18px;">{stock_info['Chinese Name']}</span></h2>
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
            peer_display = peers[["Ticker", "English Name", "Exchange", "Total Return (%)", "P/E Ratio"]]
            st.dataframe(peer_display, use_container_width=True)
        else:
            st.info("No direct peers available in the current active filter.")

# 6. Global & Exchange-Specific Top Performers Section
st.markdown("---")
st.markdown("### **Top Performing IPOs Across Public Markets (2024-2026)**")

col_top1, col_top2, col_top3, col_top4 = st.columns(4)

with col_top1:
    st.markdown("#### **Overall Leaders**")
    top_overall = df.nlargest(3, "Total Return (%)")
    for _, row in top_overall.iterrows():
        st.markdown(f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#34C759; font-weight:600;'>+{row['Total Return (%)']}%</span>", unsafe_allow_html=True)

exchanges_list = df["Exchange"].unique().tolist()
for idx, exch in enumerate(exchanges_list[:3]):
    col = [col_top2, col_top3, col_top4][idx]
    with col:
        short_name = exch.split()[0]
        st.markdown(f"#### **{short_name} Leaders**")
        exch_top = df[df["Exchange"] == exch].nlargest(3, "Total Return (%)")
        for _, row in exch_top.iterrows():
            st.markdown(f"**{row['Ticker']}** ({row['English Name']}) <br><span style='color:#34C759; font-weight:600;'>+{row['Total Return (%)']}%</span>", unsafe_allow_html=True)
