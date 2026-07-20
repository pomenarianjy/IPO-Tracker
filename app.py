import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Import the verified full database from the separate file
from ipo_data import load_verified_hk_ipos

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Jasmine’s HKEX IPO Tracker",
    page_icon="🇭🇰",
    layout="wide",
)

# --- TITLE & BRANDING ---
st.title("🇭🇰 Jasmine’s Verified HKEX IPO Tracker")
st.markdown(
    "Live performance tracking dashboard for verified Hong Kong Exchanges and"
    " Clearing (HKEX) listings linked directly with **Yahoo Finance**."
)
st.markdown("---")

# --- LOAD DATA ---
df_ipo = pd.DataFrame(load_verified_hk_ipos())

# --- SCREENING CONTROLS (MAIN APP INTERFACE) ---
st.markdown("### 🔍 Market Screening & Filter Options")
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
  exchanges = ["All"] + list(df_ipo["Exchange"].unique())
  selected_exchange = st.selectbox("Filter by Exchange Tier", exchanges)

with filter_col2:
  industries = ["All"] + list(df_ipo["Industry"].unique())
  selected_industry = st.selectbox("Filter by Industry", industries)

with filter_col3:
  if selected_industry != "All":
    sub_sectors = ["All"] + list(
        df_ipo[df_ipo["Industry"] == selected_industry]["Sub-Sector"].unique()
    )
  else:
    sub_sectors = ["All"] + list(df_ipo["Sub-Sector"].unique())
  selected_sub_sector = st.selectbox("Filter by Sub-Sector", sub_sectors)

st.markdown("---")


# --- YAHOO FINANCE LIVE CONNECTOR (AUTO-FORMATTING FOR 4-DIGIT API VALIDITY) ---
@st.cache_data(ttl=600)
def fetch_live_data(tickers):
  live_data = {}
  for t in tickers:
    # Extract numeric string out of '02249.HK' or '2249.HK'
    clean_code = t.replace(".HK", "").strip()

    # Create candidate list for Yahoo's specific formatting structures
    # Primary: Stripped integer 4-digit formatting (e.g., 2249.HK)
    # Secondary: 5-digit zero padded fallback (e.g., 02249.HK)
    try:
      stripped_code = str(int(clean_code))
    except ValueError:
      stripped_code = clean_code

    variations = [f"{stripped_code}.HK", f"{clean_code.zfill(5)}.HK", f"{t}"]

    success = False
    for candidate in variations:
      try:
        stock = yf.Ticker(candidate)
        hist = stock.history(period="6m")  # Fetch recent 6 months trajectory
        info = stock.info
        if not hist.empty:
          current_price = hist["Close"].iloc[-1]
          live_data[t] = {
              "Current Price": current_price,
              "History": hist,
              "Info": info,
              "ResolvedTicker": candidate,
          }
          success = True
          break
      except Exception:
        continue

    if not success:
      live_data[t] = None
  return live_data


tickers_to_fetch = df_ipo["Ticker"].tolist()
live_market_data = fetch_live_data(tickers_to_fetch)

# Calculate performance metrics
performance_rows = []
for index, row in df_ipo.iterrows():
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

# Filter display dataframe based on filter settings
if selected_exchange != "All":
  df_display = df_display[df_display["Exchange"] == selected_exchange]
if selected_industry != "All":
  df_display = df_display[df_display["Industry"] == selected_industry]
if selected_sub_sector != "All":
  df_display = df_display[df_display["Sub-Sector"] == selected_sub_sector]


# --- LAYOUT: STUCK LEFT PANEL & RIGHT ANALYTICS PANEL ---
col_menu, col_panel = st.columns([1.1, 1.3])

with col_menu:
  st.subheader("📋 Listed Universe Directory")

  if df_display.empty:
    st.warning("No companies match the chosen filters.")
    selected_clean_ticker = None
    full_ticker = None
  else:
    # MOVED DROPDOWN SELECTION BOX TO STICK ON TOP OF THE WHOLE LIST
    selected_clean_ticker = st.selectbox(
        "🎯 Select Stock to Analyze",
        df_display["Ticker"].tolist(),
        key="selector_top",
    )

    menu_view = df_display[
        ["Ticker", "English Name", "Chinese Name", "Gain/Loss (%)"]
    ]
    st.dataframe(menu_view, use_container_width=True, height=450, hide_index=True)

    selected_row = df_display[df_display["Ticker"] == selected_clean_ticker].iloc[
        0
    ]
    full_ticker = selected_row["Full Ticker"]

with col_panel:
  if selected_clean_ticker and full_ticker:
    st.subheader(f"📈 Analytics Panel: {selected_clean_ticker}")

    if full_ticker in live_market_data and live_market_data[full_ticker]:
      m_data = live_market_data[full_ticker]
      info = m_data["Info"]
      hist = m_data["History"]

      col1, col2, col3 = st.columns(3)
      col1.metric(
          "Current Price",
          f"{selected_row['Current Price']} HKD",
          f"{selected_row['Gain/Loss (%)']}%",
      )
      col2.metric("Offering Price", f"{selected_row['Offering Price']} HKD")
      col3.metric(
          "Market Cap",
          f"{info.get('marketCap', 0):,} HKD"
          if info.get("marketCap")
          else "N/A",
      )

      st.markdown("---")
      st.markdown("**Post-IPO Price Performance Chart**")
      fig = px.line(
          hist,
          x=hist.index,
          y="Close",
          title=f"{selected_row['English Name']} ({full_ticker}) Trajectory",
          labels={"Close": "Price (HKD)", "index": "Date"},
      )
      fig.add_hline(
          y=selected_row["Offering Price"],
          line_dash="dash",
          line_color="red",
          annotation_text="Offering Price",
      )
      st.plotly_chart(fig, use_container_width=True)

      st.markdown("### 📊 Crucial Information & Fundamentals")
      info_col1, info_col2 = st.columns(2)
      with info_col1:
        st.write(
            f"**Exchange Board:**"
            f" {info.get('exchange', selected_row['Exchange'])}"
        )
        st.write(
            f"**Industry Sector:**"
            f" {info.get('sector', selected_row['Industry'])}"
        )
        st.write(f"**Sub-Sector:** {selected_row['Sub-Sector']}")
        st.write(f"**Listing Date:** {selected_row['Listing Date']}")
      with info_col2:
        st.write(
            f"**Volume Traded:** {info.get('volume', 'N/A'):,}"
            if info.get("volume")
            else "**Volume:** N/A"
        )
        st.write(f"**52-Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.write(f"**52-Week Low:** {info.get('fiftyTwoWeekLow', 'N/A')}")
        st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")

      st.markdown("---")
      st.markdown("### 🏢 Comparable Companies (Listed Universe)")
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
        st.info("No comparable peers in the current sub-sector view.")

    else:
      # Handled fallback gracefully using database static prices if Yahoo's API fails
      st.warning(
          f"Real-time Yahoo connection timeout for {full_ticker}. Displaying"
          " base listing metadata metrics below."
      )
      col1, col2 = st.columns(2)
      col1.metric("Offering Price", f"{selected_row['Offering Price']} HKD")
      col2.metric("Listing Date", f"{selected_row['Listing Date']}")

      st.markdown("### 📊 Static Listing Profile")
      st.write(f"**English Corporate Name:** {selected_row['English Name']}")
      st.write(f"**Chinese Corporate Name:** {selected_row['Chinese Name']}")
      st.write(f"**Assigned Board Structure:** {selected_row['Exchange']}")
      st.write(f"**Industry Group Cluster:** {selected_row['Industry']}")
      st.write(f"**Sub-Sector Specialty:** {selected_row['Sub-Sector']}")
  else:
    st.info("Please adjust filters or select a valid company from the directory.")

# --- BOTTOM SECTION: TOP PERFORMING STOCKS ---
st.markdown("---")
st.subheader("🏆 Top Performing IPO Stocks Overall & By Exchange Tier")

if not df_display.empty:
  bot_col1, bot_col2 = st.columns(2)

  with bot_col1:
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

  with bot_col2:
    st.markdown("#### 🏛️ Top Performer by Exchange Board")
    best_per_exchange = df_display.loc[
        df_display.groupby("Exchange")["Gain/Loss (%)"].idxmax()
    ]
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

st.markdown("---")
st.caption(
    "Jasmine’s HKEX IPO Tracker • Powered by Streamlit & Yahoo Finance API"
)
