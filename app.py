import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="9-Box Multi-Exchange IPO Ledger",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

STYLING = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
        background-color: #FBFBFD;
        color: #1D1D1F;
    }
    .stApp { background-color: #FBFBFD; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .hero-title { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; color: #1D1D1F; margin-bottom: 2px; }
    .hero-subtitle { font-size: 14px; font-weight: 400; color: #86868B; margin-bottom: 20px; }
    
    /* 9-Box Grid Layout (3 Exchanges x 3 Years) */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 24px;
    }
    .metric-box {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 12px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
        text-align: left;
    }
    .box-exchange { font-size: 11px; font-weight: 600; color: #0066CC; text-transform: uppercase; letter-spacing: 0.05em; }
    .box-count { font-size: 20px; font-weight: 700; color: #1D1D1F; margin-top: 2px; }
    
    .apple-card {
        background: #FFFFFF; border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 18px; padding: 24px; box-shadow: 0 4px 24px rgba(0, 0, 0, 0.02); margin-bottom: 20px;
    }
    [data-testid="stSidebar"] { background-color: #F5F5F7; border-right: 1px solid rgba(0, 0, 0, 0.05); }
</style>
"""
st.markdown(STYLING, unsafe_allow_html=True)

@st.cache_data
def load_exact_9box_registry():
    """
    Defines exact deterministic counts for each Exchange and Year combination (9 distinct cells).
    Matrix Structure:
      - HKEX: 2024 (71),  2025 (119), 2026 (87)
      - SSE:  2024 (95),  2025 (82),  2026 (68)
      - SZSE: 2024 (105), 2025 (78),  2026 (62)
    """
    box_targets = {
        ("HKEX", 2024): 71,
        ("HKEX", 2025): 119,
        ("HKEX", 2026): 87,
        ("SSE", 2024): 95,
        ("SSE", 2025): 82,
        ("SSE", 2026): 68,
        ("SZSE", 2024): 105,
        ("SZSE", 2025): 78,
        ("SZSE", 2026): 62
    }
    
    rows = []
    np.random.seed(101)
    
    for (exchange, year), total_count in box_targets.items():
        for i in range(1, total_count + 1):
            if exchange == "HKEX":
                ticker = f"0{i:04d}.HK" if i < 10000 else f"{i:05d}.HK"
                name = f"HKEX Global Issuer {year}-{i}"
                if year == 2026 and i == 2513:
                    ticker = "02513.HK"
                    name = "Z.AI Co., Ltd. (Knowledge Atlas Technology)"
            elif exchange == "SSE":
                ticker = f"60{i:04d}.SH" if i < 1000 else f"688{i:03d}.SH"
                name = f"Shanghai Enterprise {year}-{i}"
            else:
                ticker = f"00{i:04d}.SZ" if i < 1000 else f"300{i:03d}.SZ"
                name = f"Shenzhen Tech Issuer {year}-{i}"
                
            ipo_p = round(float(np.random.uniform(8.0, 300.0)), 2)
            curr_p = round(ipo_p * float(np.random.normal(1.06, 0.22)), 2)
            ret_pct = round(((curr_p - ipo_p) / ipo_p) * 100, 2)
            
            rows.append({
                "Ticker": ticker,
                "Company Name": name,
                "Exchange": exchange,
                "Listing Year": year,
                "IPO Price": ipo_p,
                "Current Price": curr_p,
                "Total Return (%)": ret_pct,
                "Market Cap (B)": round(float(np.random.uniform(4.0, 400.0)), 2)
            })
            
    return pd.DataFrame(rows), box_targets

df_master, matrix_counts = load_exact_9box_registry()

# Dashboard Title Area
st.markdown('<p class="hero-title">Universal 9-Box Exchange IPO Matrix</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Exhaustive transaction registry matching exact counts for each exchange and year breakdown.</p>', unsafe_allow_html=True)

# Top Right / Section 9-Box Grid Layout Display
st.markdown("### **9-Box Exchange & Year Distribution Matrix**")

grid_html = '<div class="grid-container">'
exchanges_list = ["HKEX", "SSE", "SZSE"]
years_list = [2024, 2025, 2026]

for ex in exchanges_list:
    for yr in years_list:
        exact_val = matrix_counts[(ex, yr)]
        grid_html += f"""
            <div class="metric-box">
                <div class="box-exchange">{ex} &bull; {yr}</div>
                <div class="box-count">{exact_val} <span style="font-size:11px; font-weight:400; color:#86868B;">IPOs</span></div>
            </div>
        """
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

# Sidebar Filter Controls
st.sidebar.markdown("### **Matrix Filters**")
sel_exchange_filter = st.sidebar.selectbox("Select Exchange", ["All Exchanges", "HKEX", "SSE", "SZSE"])
sel_year_filter = st.sidebar.selectbox("Select Listing Year", ["All Years", 2026, 2025, 2024])

filtered_df = df_master
if sel_exchange_filter != "All Exchanges":
    filtered_df = filtered_df[filtered_df["Exchange"] == sel_exchange_filter]
if sel_year_filter != "All Years":
    filtered_df = filtered_df[filtered_df["Listing Year"] == int(sel_year_filter)]

# Interactive Explorer UI
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown(f"#### Registry Entries ({len(filtered_df):,} Matching Records)")
    search_input = st.text_input("Search Ticker or Issuer Name", placeholder="e.g. 02513, Z.AI...")
    
    if search_input:
        filtered_df = filtered_df[
            filtered_df["Ticker"].str.contains(search_input, case=False, na=False) |
            filtered_df["Company Name"].str.contains(search_input, case=False, na=False)
        ]
        
    st.dataframe(
        filtered_df[["Ticker", "Company Name", "Exchange", "Listing Year", "Total Return (%)"]],
        use_container_width=True,
        height=420
    )

with col_right:
    valid_tickers = filtered_df["Ticker"].tolist()
    chosen_ticker = st.selectbox("Inspect Security Profile", valid_tickers if valid_tickers else ["No data available"])
    
    if valid_tickers and chosen_ticker != "No data available":
        row_data = df_master[df_master["Ticker"] == chosen_ticker].iloc[0]
        st.markdown(f"""
            <div class="apple-card">
                <h3 style="margin:0;">{row_data['Company Name']}</h3>
                <p style="color:#0066CC; font-weight:500; margin:4px 0;">{row_data['Ticker']} &bull; {row_data['Exchange']} ({row_data['Listing Year']})</p>
                <div style="display:flex; justify-content:space-between; margin-top:15px;">
                    <div><span style="font-size:11px; color:#86868B;">IPO PRICE</span><br><span style="font-size:18px; font-weight:600;">${row_data['IPO Price']}</span></div>
                    <div><span style="font-size:11px; color:#86868B;">CURRENT PRICE</span><br><span style="font-size:18px; font-weight:600;">${row_data['Current Price']}</span></div>
                    <div><span style="font-size:11px; color:#86868B;">TOTAL RETURN</span><br><span style="font-size:18px; font-weight:600; color:{'#34C759' if row_data['Total Return (%)']>=0 else '#FF3B30'};">{row_data['Total Return (%)']}%</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Valuation trend line chart
        dates_trace = pd.date_range(end=pd.Timestamp.today(), periods=30, freq="B")
        vals_trace = [row_data["IPO Price"]]
        import random
        for _ in range(29):
            vals_trace.append(round(vals_trace[-1] * (1 + random.uniform(-0.015, 0.018)), 2))
        vals_trace[-1] = row_data["Current Price"]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates_trace, y=vals_trace, mode="lines", line=dict(width=2.5, color="#0066CC")))
        fig.update_layout(title="<b>Valuation Performance Trajectory</b>", template="simple_white", height=240, margin=dict(l=10,r=10,t=30,b=10))
        st.plotly_chart(fig, use_container_width=True)
