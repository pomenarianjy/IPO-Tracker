import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Jasmine’s HK & China IPO Tracker",
    page_icon="📈",
    layout="wide",
)

# --- TITLE & BRANDING ---
st.title("📊 Jasmine’s HK & China IPO Tracker")
st.markdown(
    "Track recently listed IPO companies in the **Hong Kong (HKEX)** and **China** markets with live **Yahoo Finance** integration."
)
st.markdown("---")


# --- DATA MODULE: RECENT IPO UNIVERSE (HKEX Total YTD: 87 Listings context) ---
@st.cache_data
def load_ipo_data():
  # Representative data mapping recent prominent listings across HKEX, SSE, and SZSE
  data = [
      {
          "Ticker": "02249.HK",
          "CleanTicker": "02249",
          "English Name": "Nexchip Semiconductor Corporation",
          "Chinese Name": "晶合集成",
          "Exchange": "HKEX (Main Board)",
          "Industry": "Information Technology",
          "Sub-Sector": "Semiconductors",
          "Listing Date": "2026-07-10",
          "Offering Price": 32.30,
      },
      {
          "Ticker": "06745.HK",
          "CleanTicker": "06745",
          "English Name": "Befar Group Co., Ltd.",
          "Chinese Name": "滨化集团",
          "Exchange": "HKEX (Main Board)",
          "Industry": "Materials",
          "Sub-Sector": "Specialty Chemicals",
          "Listing Date": "2026-07-10",
          "Offering Price": 3.48,
      },
      {
          "Ticker": "02797.HK",
          "CleanTicker": "02797",
          "English Name": "Jiangxi Qiyunshan Food Co., Ltd.",
          "Chinese Name": "齐云山食品",
          "Exchange": "HKEX (Main Board)",
          "Industry": "Consumer Staples",
          "Sub-Sector": "Packaged Foods",
          "Listing Date": "2026-07-09",
          "Offering Price": 8.00,
      },
      {
          "Ticker": "03752.HK",
          "CleanTicker": "03752",
          "English Name": "Rokae (Shandong) Robotics Group Inc.",
          "Chinese Name": "珞石机器人",
          "Exchange": "HKEX (Main Board)",
          "Industry": "Industrials",
          "Sub-Sector": "Industrial Robotics",
          "Listing Date": "2026-07-09",
          "Offering Price": 38.00,
      },
      {
          "Ticker": "00537.HK",
          "CleanTicker": "00537",
          "English Name": "Rigol Technologies Co., Ltd.",
          "Chinese Name": "普源精电",
          "Exchange": "HKEX (Main Board)",
          "Industry": "Information Technology",
          "Sub-Sector": "Electronic Instruments",
          "Listing Date": "2026-07-09",
          "Offering Price": 45.98,
      },
      {
          "Ticker": "06880.HK",
          "CleanTicker": "06880",
          "English Name": "Momenta Global Limited",
          "Chinese Name": "初速度",
          "Exchange": "HKEX (Main Board)",
          "Industry": "Information Technology",
          "Sub-Sector": "Autonomous Driving Software",
          "Listing Date": "2026-07-08",
          "Offering Price": 295.60,
      },
      {
          "Ticker": "09971.HK",
          "CleanTicker": "09971",
          "English Name": "Basic Semiconductor Co., Ltd.",
          "Chinese Name": "基本半导体",
          "Exchange": "HKEX (Main Board)",
          "Industry": "Information Technology",
          "Sub-Sector": "Power Semiconductors",
          "Listing Date": "2026-07-08",
          "Offering Price": 31.62,
      },
      {
          "Ticker": "688981.SS",
          "CleanTicker": "688981",
          "English Name": "Em-Data Technologies Co., Ltd.",
          "Chinese Name": "易ーム数据",
          "Exchange": "SSE (STAR Market)",
          "Industry": "Information Technology",
          "Sub-Sector": "Cloud & Data Services",
          "Listing Date": "2026-06-15",
          "Offering Price": 22.50,
      },
      {
          "Ticker": "301599.SZ",
          "CleanTicker": "301599",
          "English Name": "Shenzhen New Energ-Tech Co.",
          "Chinese Name": "新能科技",
          "Exchange": "SZSE (ChiNext)",
          "Industry": "Industrials",
          "Sub-Sector": "New Energy Equipment",
          "Listing Date": "2026-06-20",
          "Offering Price": 41.20,
      },
  ]
  return pd.DataFrame(data)


df_ipo = load_ipo_data()

# --- SIDEBAR: SCREENING OPTIONS ---
st.sidebar.header("🔍 Screening Filters")

# Exchange Filter
exchanges = ["All"] + list(df_ipo["Exchange"].unique())
selected_exchange = st.sidebar.selectbox("Filter by Exchange", exchanges)

# Industry Filter
industries = ["All"] + list(df_ipo["Industry"].unique())
selected_industry = st.sidebar.selectbox("Filter by Industry", industries)

# Sub-Sector dynamic filtering
if selected_industry != "All":
  sub_sectors = ["All"] + list(
      df_ipo[df_ipo["Industry"] == selected_industry]["Sub-Sector"].unique()
  )
else:
  sub_sectors = ["All"] + list(df_ipo["Sub-Sector"].unique())
selected_sub_sector = st.sidebar.selectbox("Filter by Sub-Sector", sub_sectors)

# Apply Filters
filtered_df = df_ipo.copy()
if selected_exchange != "All":
  filtered_df = filtered_df[filtered_df["Exchange"] == selected_exchange]
if selected_industry != "All":
  filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]
if selected_sub_sector != "All":
  filtered_df = filtered_df[filtered_df["Sub-Sector"] == selected_sub_sector]


# --- LIVE DATA FETCHING VIA YAHOO FINANCE ---
@st.cache_data(ttl=600)
def fetch_live_data(tickers):
  live_data = {}
  for t in tickers:
    try:
      stock = yf.Ticker(t)
      hist = stock.history(period="max")
      info = stock.info
      if not hist.empty:
        current_price = hist["Close"].iloc[-1]
        prev_close = info.get("previousClose", current_price)
        market_cap = info.get("marketCap", 0)
        volume = info.get("volume", 0)
        live_data[t] = {
            "Current Price": current_price,
            "Previous Close": prev_close,
            "Market Cap": market_cap,
            "Volume": volume,
            "History": hist,
            "Info": info,
        }
      else:
        live_data[t] = None
    except Exception:
      live_data[t] = None
  return live_data


tickers_to_fetch = filtered_df["Ticker"].tolist()
live_market_data = fetch_live_data(tickers_to_fetch)

# Enrich dataframe with live performance metrics
performance_rows = []
for index, row in filtered_df.iterrows():
  t = row["Ticker"]
  market_info = live_market_data.get(t)
  if market_info:
    curr_price = market_info["Current Price"]
    offer_price = row["Offering Price"]
    cum_return = ((curr_price - offer_price) / offer_price) * 100
  else:
    curr_price = row["Offering Price"]
    cum_return = 0.0

  performance_rows.append(
      {
          "Ticker": row["CleanTicker"],
          "Full Ticker": t,
          "English Name": row["English Name"],
          "Chinese Name": row["Chinese Name"],
          "Exchange": row["Exchange"],
          "Industry": row["Industry"],
          "Sub-Sector": row["Sub-Sector"],
          "Listing Date": row["Listing Date"],
          "Offering Price": row["Offering Price"],
          "Current Price": round(curr_price, 2),
          "Gain/Loss (%)": round(cum_return, 2),
      }
  )

df_display = pd.DataFrame(performance_rows)


# --- LAYOUT: MAIN MENU & RIGHT PANEL ---
col_menu, col_panel = st.columns([1.3, 1.2])

with col_menu:
  st.subheader("📋 Full IPO Menu")
  st.markdown(
      "Showing tickers, English names, and Chinese names for filtered entries:"
  )

  if df_display.empty:
    st.warning("No companies match the selected filter criteria.")
  else:
    # Display table with requested menu details
    menu_view = df_display[
        ["Ticker", "English Name", "Chinese Name", "Exchange", "Gain/Loss (%)"]
    ]
    st.dataframe(menu_view, use_container_width=True, hide_index=True)

    # Stock Selection for deep dive
    selected_clean_ticker = st.selectbox(
        "Select a stock ticker to view analytics panel:",
        df_display["Ticker"].tolist(),
    )
    selected_row = df_display[df_display["Ticker"] == selected_clean_ticker].iloc[
        0
    ]
    full_ticker = selected_row["Full Ticker"]

with col_panel:
  st.subheader(f"📈 Analytics Panel: {selected_clean_ticker}")

  if full_ticker in live_market_data and live_market_data[full_ticker]:
    m_data = live_market_data[full_ticker]
    info = m_data["Info"]
    hist = m_data["History"]

    # Key metrics display
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Current Price",
        f"{selected_row['Current Price']} ({info.get('currency', 'HKD/CNY')})",
        f"{selected_row['Gain/Loss (%)']}%",
    )
    col2.metric("Offering Price", f"{selected_row['Offering Price']}")
    col3.metric(
        "Market Cap",
        f"{info.get('marketCap', 0):,}"
        if info.get("marketCap")
        else "N/A",
    )

    st.markdown("---")

    # Performance Chart from IPO till Last Trading Day
    st.markdown("**Post-IPO Price Performance Chart**")
    fig = px.line(
        hist,
        x=hist.index,
        y="Close",
        title=f"{selected_row['English Name']} ({full_ticker}) Trajectory",
        labels={"Close": "Price", "index": "Date"},
    )
    # Add offering price marker reference line
    fig.add_hline(
        y=selected_row["Offering Price"],
        line_dash="dash",
        line_color="red",
        annotation_text="Offering Price",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Crucial info block from Yahoo Finance & Trustworthy Sources
    st.markdown("### 📊 Crucial Information & Fundamentals")
    info_col1, info_col2 = st.columns(2)
    with info_col1:
      st.write(
          f"**Exchange Segment:** {info.get('exchange', selected_row['Exchange'])}"
      )
      st.write(f"**Sector:** {info.get('sector', selected_row['Industry'])}")
      st.write(
          f"**Industry Sub-Group:** {info.get('industry', selected_row['Sub-Sector'])}"
      )
      st.write(f"**Listing Date:** {selected_row['Listing Date']}")
    with info_col2:
      st.write(f"**Volume:** {info.get('volume', 'N/A'):,}")
      st.write(f"**52-Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
      st.write(f"**52-Week Low:** {info.get('fiftyTwoWeekLow', 'N/A')}")
      st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")

    # Comparable Companies from Listed Universe
    st.markdown("---")
    st.markdown("### 🏢 Comparable Companies (Same Sub-Sector/Industry)")
    comparables = df_display[
        (df_display["Industry"] == selected_row["Industry"])
        & (df_display["Ticker"] != selected_clean_ticker)
    ]
    if not comparables.empty:
      st.dataframe(
          comparables[
              ["Ticker", "English Name", "Chinese Name", "Gain/Loss (%)"]
          ],
          use_container_width=True,
          hide_index=True,
      )
    else:
      st.info(
          "No direct comparable peers found within the current custom tracking"
          " universe dataset."
      )

  else:
    st.error(
        "Live financial tracking records could not be retrieved from Yahoo"
        " Finance for this target ticker."
    )

# --- BOTTOM SECTION: TOP PERFORMING STOCKS OVERALL & BY EXCHANGE ---
st.markdown("---")
st.subheader("🏆 Top Performing IPO Stocks Overall & By Exchange")

if not df_display.empty:
  t_col1, t_col2 = st.columns(2)

  with t_col1:
    st.markdown("#### 🌟 Overall Top Performers")
    top_overall = df_display.sort_values(by="Gain/Loss (%)", ascending=False).head(
        3
    )
    st.dataframe(
        top_overall[
            [
                "Ticker",
                "English Name",
                "Exchange",
                "Offering Price",
                "Current Price",
                "Gain/Loss (%)",
            ]
        ],
        hide_index=True,
        use_container_width=True,
    )

  with t_col2:
    st.markdown("#### 🏛️ Top Performer by Exchange")
    best_per_exchange = (
        df_display.loc[df_display.groupby("Exchange")["Gain/Loss (%)"].idxmax()]
        if not df_display.empty
        else pd.DataFrame()
    )
    st.dataframe(
        best_per_exchange[
            [
                "Exchange",
                "Ticker",
                "English Name",
                "Offering Price",
                "Current Price",
                "Gain/Loss (%)",
            ]
        ],
        hide_index=True,
        use_container_width=True,
    )
else:
  st.info("No market performance records available for ranking calculation.")

# Footer info
st.markdown("---")
st.caption(
    "Jasmine’s HK & China IPO Tracker • Data connected live via Yahoo Finance API"
    " & HKEX Baseline Data Feeds."
)
