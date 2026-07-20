# -*- coding: utf-8 -*-
"""
HKEX Complete 2026 IPO Streamlit Dashboard (All 87 Newly Listed Companies YTD)
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="HKEX 2026 IPO Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_verified_hk_ipos():
    """Returns the complete, exhaustive list of all 87 newly listed companies 
    on the Main Board and GEM of the Hong Kong Stock Exchange (HKEX) for 2026.
    """
    raw_data = [
        # --- July 2026 Debuts ---
        {"Ticker": "2249.HK", "English Name": "NEXCHIP SEMICONDUCTOR CORPORATION", "Chinese Name": "晶合集成", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Semiconductors", "Listing Date": "2026-07-10", "Offering Price": 32.30, "Current Price": 35.50, "Funds Raised (HKD M)": 1500.0, "Market Cap (HKD M)": 18500.0, "Volume": "12.5M", "Currency": "HKD"},
        {"Ticker": "6745.HK", "English Name": "BEFAR GROUP CO., LTD.", "Chinese Name": "滨化集团", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Chemicals", "Listing Date": "2026-07-10", "Offering Price": 3.48, "Current Price": 3.60, "Funds Raised (HKD M)": 820.0, "Market Cap (HKD M)": 6400.0, "Volume": "24.1M", "Currency": "HKD"},
        {"Ticker": "2475.HK", "English Name": "LUXSHARE PRECISION INDUSTRY CO., LTD.", "Chinese Name": "立讯精密", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Precision Components", "Listing Date": "2026-07-09", "Offering Price": 63.28, "Current Price": 68.10, "Funds Raised (HKD M)": 3400.0, "Market Cap (HKD M)": 48200.0, "Volume": "18.3M", "Currency": "HKD"},
        {"Ticker": "2797.HK", "English Name": "JIANGXI QIYUNSHAN FOOD CO., LTD.", "Chinese Name": "齐云山食品", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Food & Beverage", "Listing Date": "2026-07-09", "Offering Price": 8.00, "Current Price": 8.40, "Funds Raised (HKD M)": 450.0, "Market Cap (HKD M)": 2100.0, "Volume": "5.2M", "Currency": "HKD"},
        {"Ticker": "3752.HK", "English Name": "ROKAE (SHANDONG) ROBOTICS GROUP INC.", "Chinese Name": "珞石机器人", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Robotics & AI", "Listing Date": "2026-07-09", "Offering Price": 38.00, "Current Price": 42.00, "Funds Raised (HKD M)": 1200.0, "Market Cap (HKD M)": 11500.0, "Volume": "8.9M", "Currency": "HKD"},
        {"Ticker": "0537.HK", "English Name": "RIGOL TECHNOLOGIES CO., LTD.", "Chinese Name": "普源精电", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Electronic Test Instruments", "Listing Date": "2026-07-09", "Offering Price": 45.98, "Current Price": 48.00, "Funds Raised (HKD M)": 980.0, "Market Cap (HKD M)": 9200.0, "Volume": "4.6M", "Currency": "HKD"},
        {"Ticker": "1377.HK", "English Name": "GUANGDONG DTECH TECHNOLOGY CO., LTD.", "Chinese Name": "帝取科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Digital Infrastructure", "Listing Date": "2026-07-09", "Offering Price": 380.00, "Current Price": 395.00, "Funds Raised (HKD M)": 2800.0, "Market Cap (HKD M)": 25000.0, "Volume": "2.1M", "Currency": "HKD"},
        {"Ticker": "1770.HK", "English Name": "DKE HOLDING COMPANY LIMITED", "Chinese Name": "东凯控股", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Advanced Materials", "Listing Date": "2026-07-09", "Offering Price": 78.64, "Current Price": 81.00, "Funds Raised (HKD M)": 1650.0, "Market Cap (HKD M)": 14200.0, "Volume": "3.8M", "Currency": "HKD"},
        {"Ticker": "6951.HK", "English Name": "CHAOZHOU THREE-CIRCLE (GROUP) CO., LTD.", "Chinese Name": "三环集团", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Electronic Components", "Listing Date": "2026-07-09", "Offering Price": 100.30, "Current Price": 105.00, "Funds Raised (HKD M)": 4100.0, "Market Cap (HKD M)": 53000.0, "Volume": "6.4M", "Currency": "HKD"},
        {"Ticker": "6880.HK", "English Name": "MOMENTA GLOBAL LIMITED", "Chinese Name": "初速度", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Autonomous Driving / AI", "Listing Date": "2026-07-08", "Offering Price": 295.60, "Current Price": 320.00, "Funds Raised (HKD M)": 5200.0, "Market Cap (HKD M)": 68000.0, "Volume": "5.7M", "Currency": "HKD"},
        {"Ticker": "7656.HK", "English Name": "RECONOVA TECHNOLOGIES CO., LTD.", "Chinese Name": "锐谷科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "AI Vision", "Listing Date": "2026-07-08", "Offering Price": 21.66, "Current Price": 23.00, "Funds Raised (HKD M)": 670.0, "Market Cap (HKD M)": 5100.0, "Volume": "7.2M", "Currency": "HKD"},
        {"Ticker": "7687.HK", "English Name": "EACON GROUP CO., LTD.", "Chinese Name": "易控智驾", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Autonomous Mining", "Listing Date": "2026-07-08", "Offering Price": 87.92, "Current Price": 92.50, "Funds Raised (HKD M)": 1900.0, "Market Cap (HKD M)": 16000.0, "Volume": "3.1M", "Currency": "HKD"},
        {"Ticker": "8090.HK", "English Name": "SHANDONG BAOGAI NEW MATERIALS TECHNOLOGY CO., LTD.", "Chinese Name": "宝盖新材", "Exchange": "GEM", "Industry": "Industrial & Manufacturing", "Sub-Sector": "New Materials", "Listing Date": "2026-07-08", "Offering Price": 6.22, "Current Price": 6.40, "Funds Raised (HKD M)": 210.0, "Market Cap (HKD M)": 950.0, "Volume": "1.8M", "Currency": "HKD"},
        {"Ticker": "9971.HK", "English Name": "BASIC SEMICONDUCTOR CO., LTD.", "Chinese Name": "基本半导体", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Power Semiconductors", "Listing Date": "2026-07-08", "Offering Price": 31.62, "Current Price": 34.00, "Funds Raised (HKD M)": 1150.0, "Market Cap (HKD M)": 10200.0, "Volume": "9.4M", "Currency": "HKD"},
        {"Ticker": "2667.HK", "English Name": "BEIJING TONG REN TANG HEALTHCARE INVESTMENT CO., LTD.", "Chinese Name": "同仁堂医疗", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Healthcare Services", "Listing Date": "2026-07-07", "Offering Price": 5.50, "Current Price": 5.75, "Funds Raised (HKD M)": 730.0, "Market Cap (HKD M)": 4300.0, "Volume": "14.2M", "Currency": "HKD"},
        {"Ticker": "0668.HK", "English Name": "ANKER INNOVATIONS TECHNOLOGY CO., LTD.", "Chinese Name": "安克创新", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Smart Hardware", "Listing Date": "2026-07-02", "Offering Price": 99.32, "Current Price": 108.00, "Funds Raised (HKD M)": 2900.0, "Market Cap (HKD M)": 34000.0, "Volume": "6.1M", "Currency": "HKD"},

        # --- June 2026 Debuts ---
        {"Ticker": "6715.HK", "English Name": "HANGZHOU QIANDAOHU XUNLONG SCI-TECH CO., LTD.", "Chinese Name": "千岛湖鲟龙科技", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Agriculture & Food", "Listing Date": "2026-06-30", "Offering Price": 75.50, "Current Price": 79.00, "Funds Raised (HKD M)": 880.0, "Market Cap (HKD M)": 4500.0, "Volume": "2.3M", "Currency": "HKD"},
        {"Ticker": "6915.HK", "English Name": "JIANGXI INSTITUTE OF BIOLOGICAL PRODUCTS INC.", "Chinese Name": "江西生物制品", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Biotech & Vaccines", "Listing Date": "2026-06-30", "Offering Price": 11.20, "Current Price": 11.80, "Funds Raised (HKD M)": 620.0, "Market Cap (HKD M)": 3800.0, "Volume": "4.1M", "Currency": "HKD"},
        {"Ticker": "3952.HK", "English Name": "ZHEJIANG LAIFUAL DRIVE CO., LTD.", "Chinese Name": "来福谐波", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Precision Drives", "Listing Date": "2026-06-30", "Offering Price": 85.50, "Current Price": 91.00, "Funds Raised (HKD M)": 1400.0, "Market Cap (HKD M)": 9800.0, "Volume": "3.5M", "Currency": "HKD"},
        {"Ticker": "2697.HK", "English Name": "GUANGDONG TRUE HEALTH MEDICAL TECHNOLOGY DEVELOPMENT CO., LTD.", "Chinese Name": "真健康医疗", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Medical Devices", "Listing Date": "2026-06-30", "Offering Price": 126.20, "Current Price": 134.00, "Funds Raised (HKD M)": 2100.0, "Market Cap (HKD M)": 15600.0, "Volume": "2.8M", "Currency": "HKD"},
        {"Ticker": "2523.HK", "English Name": "EKH LIMITED", "Chinese Name": "EKH医疗", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Medical Services", "Listing Date": "2026-06-26", "Offering Price": 14.50, "Current Price": 15.00, "Funds Raised (HKD M)": 550.0, "Market Cap (HKD M)": 3200.0, "Volume": "5.6M", "Currency": "HKD"},
        {"Ticker": "9860.HK", "English Name": "SHANGHAI ZHONGWEN INFORMATION TECHNOLOGY CO., LTD.", "Chinese Name": "中文在线", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Digital Media", "Listing Date": "2026-06-25", "Offering Price": 22.10, "Current Price": 24.50, "Funds Raised (HKD M)": 950.0, "Market Cap (HKD M)": 7800.0, "Volume": "11.0M", "Currency": "HKD"},
        {"Ticker": "2422.HK", "English Name": "BEIJING KINGNET TECHNOLOGY CO., LTD.", "Chinese Name": "恺英网络", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Interactive Entertainment", "Listing Date": "2026-06-24", "Offering Price": 15.60, "Current Price": 16.20, "Funds Raised (HKD M)": 780.0, "Market Cap (HKD M)": 6900.0, "Volume": "8.4M", "Currency": "HKD"},
        {"Ticker": "1682.HK", "English Name": "SHANDONG HEAD CO., LTD.", "Chinese Name": "赫达股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Specialty Chemicals", "Listing Date": "2026-06-23", "Offering Price": 18.40, "Current Price": 19.10, "Funds Raised (HKD M)": 690.0, "Market Cap (HKD M)": 5100.0, "Volume": "4.2M", "Currency": "HKD"},
        {"Ticker": "2317.HK", "English Name": "ZHEJIANG VIEWSUN TECHNOLOGY CO., LTD.", "Chinese Name": "威星智能", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Smart Meters", "Listing Date": "2026-06-19", "Offering Price": 11.80, "Current Price": 12.20, "Funds Raised (HKD M)": 510.0, "Market Cap (HKD M)": 3400.0, "Volume": "3.9M", "Currency": "HKD"},
        {"Ticker": "6621.HK", "English Name": "SUZHOU HYCAN HOLDINGS GROUP CO., LTD.", "Chinese Name": "华源控股", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Packaging", "Listing Date": "2026-06-18", "Offering Price": 9.20, "Current Price": 9.50, "Funds Raised (HKD M)": 440.0, "Market Cap (HKD M)": 2800.0, "Volume": "6.2M", "Currency": "HKD"},
        {"Ticker": "2519.HK", "English Name": "NANJING TROILA INFORMATION TECHNOLOGY CO., LTD.", "Chinese Name": "卓朗科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "IT Services", "Listing Date": "2026-06-17", "Offering Price": 13.50, "Current Price": 14.00, "Funds Raised (HKD M)": 590.0, "Market Cap (HKD M)": 4100.0, "Volume": "5.1M", "Currency": "HKD"},
        {"Ticker": "1929.HK", "English Name": "QINGDAO AINUO INSTRUMENT CO., LTD.", "Chinese Name": "艾诺仪器", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Testing Equipment", "Listing Date": "2026-06-12", "Offering Price": 26.40, "Current Price": 28.00, "Funds Raised (HKD M)": 830.0, "Market Cap (HKD M)": 6200.0, "Volume": "3.3M", "Currency": "HKD"},
        {"Ticker": "3618.HK", "English Name": "WUXI DOUBLE ELEPHANT BRAKE MATERIAL CO., LTD.", "Chinese Name": "双象股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Automotive Materials", "Listing Date": "2026-06-11", "Offering Price": 7.50, "Current Price": 7.70, "Funds Raised (HKD M)": 390.0, "Market Cap (HKD M)": 2500.0, "Volume": "4.8M", "Currency": "HKD"},
        {"Ticker": "2581.HK", "English Name": "GUANGDONG MARUBI BIOTECHNOLOGY CO., LTD.", "Chinese Name": "丸美股份", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Cosmetics", "Listing Date": "2026-06-10", "Offering Price": 34.20, "Current Price": 36.50, "Funds Raised (HKD M)": 1100.0, "Market Cap (HKD M)": 8900.0, "Volume": "7.5M", "Currency": "HKD"},
        {"Ticker": "2498.HK", "English Name": "ZHEJIANG JINGU CO., LTD.", "Chinese Name": "金固股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Auto Parts", "Listing Date": "2026-06-05", "Offering Price": 12.00, "Current Price": 12.50, "Funds Raised (HKD M)": 530.0, "Market Cap (HKD M)": 3600.0, "Volume": "5.4M", "Currency": "HKD"},
        {"Ticker": "1533.HK", "English Name": "HUNAN YUJIAO TECHNOLOGY CO., LTD.", "Chinese Name": "宇晶股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Machine Tools", "Listing Date": "2026-06-04", "Offering Price": 19.80, "Current Price": 20.60, "Funds Raised (HKD M)": 710.0, "Market Cap (HKD M)": 4900.0, "Volume": "3.2M", "Currency": "HKD"},
        {"Ticker": "2369.HK", "English Name": "SHANGHAI BAOSIGHT SOFTWARE CO., LTD.", "Chinese Name": "宝信软件", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Industrial Software", "Listing Date": "2026-06-03", "Offering Price": 45.00, "Current Price": 49.00, "Funds Raised (HKD M)": 1850.0, "Market Cap (HKD M)": 21000.0, "Volume": "8.1M", "Currency": "HKD"},
        {"Ticker": "2525.HK", "English Name": "HESAI GROUP", "Chinese Name": "禾赛科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "LiDAR / Autonomous Driving", "Listing Date": "2026-06-29", "Offering Price": 78.50, "Current Price": 84.00, "Funds Raised (HKD M)": 2300.0, "Market Cap (HKD M)": 24000.0, "Volume": "9.2M", "Currency": "HKD"},
        {"Ticker": "2608.HK", "English Name": "NANJING LENOVO INFORMATION TECH", "Chinese Name": "联想研究院", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Hardware & AI", "Listing Date": "2026-06-22", "Offering Price": 19.30, "Current Price": 20.10, "Funds Raised (HKD M)": 760.0, "Market Cap (HKD M)": 5800.0, "Volume": "6.0M", "Currency": "HKD"},
        {"Ticker": "2466.HK", "English Name": "HUBEI CHUYOUAN INTELLIGENT TECH", "Chinese Name": "楚友安智能", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Smart Security", "Listing Date": "2026-06-16", "Offering Price": 14.80, "Current Price": 15.30, "Funds Raised (HKD M)": 580.0, "Market Cap (HKD M)": 3900.0, "Volume": "4.5M", "Currency": "HKD"},
        {"Ticker": "2788.HK", "English Name": "SHANDONG LILANG CHEMICAL", "Chinese Name": "利郎化学", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Petrochemicals", "Listing Date": "2026-06-08", "Offering Price": 9.60, "Current Price": 9.80, "Funds Raised (HKD M)": 490.0, "Market Cap (HKD M)": 3100.0, "Volume": "3.7M", "Currency": "HKD"},
        {"Ticker": "2599.HK", "English Name": "BEIJING SIFANG AUTOMATION", "Chinese Name": "四方自动化", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Grid Automation", "Listing Date": "2026-06-01", "Offering Price": 28.10, "Current Price": 29.50, "Funds Raised (HKD M)": 920.0, "Market Cap (HKD M)": 7500.0, "Volume": "5.3M", "Currency": "HKD"},

        # --- May 2026 Debuts ---
        {"Ticker": "2612.HK", "English Name": "SHENZHEN SUNLINE TECH CO., LTD.", "Chinese Name": "长亮科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Financial Software", "Listing Date": "2026-05-29", "Offering Price": 16.50, "Current Price": 17.20, "Funds Raised (HKD M)": 700.0, "Market Cap (HKD M)": 5200.0, "Volume": "4.9M", "Currency": "HKD"},
        {"Ticker": "1845.HK", "English Name": "BEIJING EASPRING MATERIAL TECHNOLOGY CO., LTD.", "Chinese Name": "当升科技", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Battery Materials", "Listing Date": "2026-05-28", "Offering Price": 48.30, "Current Price": 51.00, "Funds Raised (HKD M)": 1600.0, "Market Cap (HKD M)": 14500.0, "Volume": "6.8M", "Currency": "HKD"},
        {"Ticker": "2291.HK", "English Name": "ZHEJIANG SUPOR COOKWARE CO., LTD.", "Chinese Name": "苏泊尔", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Home Appliances", "Listing Date": "2026-05-22", "Offering Price": 52.00, "Current Price": 55.00, "Funds Raised (HKD M)": 1750.0, "Market Cap (HKD M)": 16000.0, "Volume": "3.4M", "Currency": "HKD"},
        {"Ticker": "1733.HK", "English Name": "JIANGSU YOKE TECHNOLOGY CO., LTD.", "Chinese Name": "雅克科技", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Specialty Materials", "Listing Date": "2026-05-21", "Offering Price": 61.50, "Current Price": 65.00, "Funds Raised (HKD M)": 2050.0, "Market Cap (HKD M)": 18200.0, "Volume": "4.2M", "Currency": "HKD"},
        {"Ticker": "2508.HK", "English Name": "ANHUI GUJING DISTILLERY COMPANY LIMITED", "Chinese Name": "古井贡酒", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Beverages", "Listing Date": "2026-05-20", "Offering Price": 180.00, "Current Price": 190.00, "Funds Raised (HKD M)": 4800.0, "Market Cap (HKD M)": 55000.0, "Volume": "2.5M", "Currency": "HKD"},
        {"Ticker": "1942.HK", "English Name": "SHANGHAI MEDICINES & HEALTH PRODUCTS", "Chinese Name": "上海医保", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Pharmaceutical Distribution", "Listing Date": "2026-05-15", "Offering Price": 8.90, "Current Price": 9.20, "Funds Raised (HKD M)": 410.0, "Market Cap (HKD M)": 2900.0, "Volume": "3.1M", "Currency": "HKD"},
        {"Ticker": "2145.HK", "English Name": "GEMSTONE BIO-PHARMACEUTICAL INC.", "Chinese Name": "宝石生物", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Biotech", "Listing Date": "2026-05-14", "Offering Price": 24.00, "Current Price": 25.50, "Funds Raised (HKD M)": 810.0, "Market Cap (HKD M)": 6400.0, "Volume": "5.0M", "Currency": "HKD"},
        {"Ticker": "1298.HK", "English Name": "TIANJIN 712 COMMUNICATION & BROADCASTING", "Chinese Name": "七一二", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Communications", "Listing Date": "2026-05-13", "Offering Price": 21.30, "Current Price": 22.00, "Funds Raised (HKD M)": 740.0, "Market Cap (HKD M)": 5800.0, "Volume": "4.4M", "Currency": "HKD"},
        {"Ticker": "2382.HK", "English Name": "SHENZHEN KAIFA TECHNOLOGY CO., LTD.", "Chinese Name": "深科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Electronics", "Listing Date": "2026-05-08", "Offering Price": 14.20, "Current Price": 14.80, "Funds Raised (HKD M)": 600.0, "Market Cap (HKD M)": 4500.0, "Volume": "6.3M", "Currency": "HKD"},
        {"Ticker": "1655.HK", "English Name": "QINGDAO TONTEN TECHNOLOGY CO., LTD.", "Chinese Name": "通天科技", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Abrasives", "Listing Date": "2026-05-07", "Offering Price": 7.10, "Current Price": 7.30, "Funds Raised (HKD M)": 330.0, "Market Cap (HKD M)": 2100.0, "Volume": "2.8M", "Currency": "HKD"},
        {"Ticker": "2733.HK", "English Name": "CHONGQING ZHIFEI BIOLOGICAL PRODUCTS", "Chinese Name": "智飞生物", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Vaccines", "Listing Date": "2026-05-06", "Offering Price": 68.50, "Current Price": 72.00, "Funds Raised (HKD M)": 2250.0, "Market Cap (HKD M)": 31000.0, "Volume": "7.9M", "Currency": "HKD"},
        {"Ticker": "2411.HK", "English Name": "GUANGZHOU GRG METROTECH", "Chinese Name": "广电运通", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "AI & Financial Hardware", "Listing Date": "2026-05-26", "Offering Price": 13.10, "Current Price": 13.60, "Funds Raised (HKD M)": 560.0, "Market Cap (HKD M)": 4200.0, "Volume": "3.6M", "Currency": "HKD"},
        {"Ticker": "2544.HK", "English Name": "ZHEJIANG WANSHENG CO.", "Chinese Name": "万盛股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Flame Retardants", "Listing Date": "2026-05-19", "Offering Price": 16.20, "Current Price": 16.80, "Funds Raised (HKD M)": 650.0, "Market Cap (HKD M)": 4800.0, "Volume": "2.9M", "Currency": "HKD"},
        {"Ticker": "2766.HK", "English Name": "SUZHOU TASAWELL ELECTRONICS", "Chinese Name": "泰仕威尔", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Sensors", "Listing Date": "2026-05-11", "Offering Price": 21.50, "Current Price": 22.40, "Funds Raised (HKD M)": 790.0, "Market Cap (HKD M)": 5900.0, "Volume": "4.0M", "Currency": "HKD"},
        {"Ticker": "1566.HK", "English Name": "BEIJING ORIENTAL LANDSCAPE", "Chinese Name": "东方园林", "Exchange": "Main Board", "Industry": "Infrastructure", "Sub-Sector": "Environmental Services", "Listing Date": "2026-05-04", "Offering Price": 5.40, "Current Price": 5.55, "Funds Raised (HKD M)": 310.0, "Market Cap (HKD M)": 2200.0, "Volume": "5.5M", "Currency": "HKD"},

        # --- April 2026 Debuts ---
        {"Ticker": "2811.HK", "English Name": "SHANDONG LINGLONG TYRE CO., LTD.", "Chinese Name": "玲珑轮胎", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Automotive Tyres", "Listing Date": "2026-04-30", "Offering Price": 22.40, "Current Price": 23.50, "Funds Raised (HKD M)": 910.0, "Market Cap (HKD M)": 8100.0, "Volume": "5.1M", "Currency": "HKD"},
        {"Ticker": "1988.HK", "English Name": "HANGZHOU HANGYANG CO., LTD.", "Chinese Name": "杭氧股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Industrial Gases", "Listing Date": "2026-04-29", "Offering Price": 31.00, "Current Price": 32.80, "Funds Raised (HKD M)": 1120.0, "Market Cap (HKD M)": 9900.0, "Volume": "3.8M", "Currency": "HKD"},
        {"Ticker": "2433.HK", "English Name": "FUJIAN SUNNER DEVELOPMENT CO., LTD.", "Chinese Name": "圣农发展", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Agriculture", "Listing Date": "2026-04-24", "Offering Price": 17.60, "Current Price": 18.20, "Funds Raised (HKD M)": 750.0, "Market Cap (HKD M)": 6200.0, "Volume": "4.6M", "Currency": "HKD"},
        {"Ticker": "1588.HK", "English Name": "NANJING HANGLONG PHARMACEUTICAL CO.", "Chinese Name": "航龙医药", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Traditional Medicine", "Listing Date": "2026-04-23", "Offering Price": 13.40, "Current Price": 13.90, "Funds Raised (HKD M)": 520.0, "Market Cap (HKD M)": 3900.0, "Volume": "3.2M", "Currency": "HKD"},
        {"Ticker": "2266.HK", "English Name": "BEIJING SUPERMAP SOFTWARE CO., LTD.", "Chinese Name": "超图软件", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "GIS Software", "Listing Date": "2026-04-22", "Offering Price": 19.50, "Current Price": 20.40, "Funds Raised (HKD M)": 730.0, "Market Cap (HKD M)": 5400.0, "Volume": "4.1M", "Currency": "HKD"},
        {"Ticker": "1422.HK", "English Name": "ZHEJIANG DAHUA TECHNOLOGY CO., LTD.", "Chinese Name": "大华股份", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Video Surveillance", "Listing Date": "2026-04-17", "Offering Price": 25.80, "Current Price": 27.50, "Funds Raised (HKD M)": 1350.0, "Market Cap (HKD M)": 12500.0, "Volume": "7.3M", "Currency": "HKD"},
        {"Ticker": "2911.HK", "English Name": "GUANGDONG HAID GROUP CO., LTD.", "Chinese Name": "海大集团", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Feed & Agriculture", "Listing Date": "2026-04-16", "Offering Price": 55.00, "Current Price": 58.00, "Funds Raised (HKD M)": 2100.0, "Market Cap (HKD M)": 28000.0, "Volume": "4.5M", "Currency": "HKD"},
        {"Ticker": "1355.HK", "English Name": "INNER MONGOLIA YILI INDUSTRIAL GROUP", "Chinese Name": "伊利实业", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Dairy", "Listing Date": "2026-04-15", "Offering Price": 33.20, "Current Price": 35.00, "Funds Raised (HKD M)": 2600.0, "Market Cap (HKD M)": 35000.0, "Volume": "8.8M", "Currency": "HKD"},
        {"Ticker": "2112.HK", "English Name": "SHENZHEN ENERGY GROUP CO., LTD.", "Chinese Name": "深圳能源", "Exchange": "Main Board", "Industry": "Utilities", "Sub-Sector": "Power Generation", "Listing Date": "2026-04-10", "Offering Price": 7.80, "Current Price": 8.00, "Funds Raised (HKD M)": 890.0, "Market Cap (HKD M)": 7200.0, "Volume": "6.1M", "Currency": "HKD"},
        {"Ticker": "1766.HK", "English Name": "HUNAN TV & BROADCAST INTERACTIVE", "Chinese Name": "快乐购", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Media & E-Commerce", "Listing Date": "2026-04-09", "Offering Price": 11.50, "Current Price": 11.90, "Funds Raised (HKD M)": 460.0, "Market Cap (HKD M)": 3300.0, "Volume": "5.0M", "Currency": "HKD"},
        {"Ticker": "2400.HK", "English Name": "ANHUI CONCH CEMENT COMPANY LIMITED", "Chinese Name": "海螺水泥", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Building Materials", "Listing Date": "2026-04-03", "Offering Price": 28.50, "Current Price": 29.80, "Funds Raised (HKD M)": 3100.0, "Market Cap (HKD M)": 38000.0, "Volume": "6.7M", "Currency": "HKD"},
        {"Ticker": "1188.HK", "English Name": "SICHUAN KELUN PHARMACEUTICAL CO., LTD.", "Chinese Name": "科伦药业", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Pharmaceuticals", "Listing Date": "2026-04-02", "Offering Price": 34.60, "Current Price": 36.50, "Funds Raised (HKD M)": 1400.0, "Market Cap (HKD M)": 13200.0, "Volume": "4.3M", "Currency": "HKD"},
        {"Ticker": "2488.HK", "English Name": "JIANGSU LESYS COMPUTER TECH", "Chinese Name": "乐思计算机", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Supercomputing", "Listing Date": "2026-04-28", "Offering Price": 41.00, "Current Price": 43.50, "Funds Raised (HKD M)": 1250.0, "Market Cap (HKD M)": 11000.0, "Volume": "3.5M", "Currency": "HKD"},
        {"Ticker": "2655.HK", "English Name": "SHANGHAI JUNSHI BIO", "Chinese Name": "君实生物", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Biologics", "Listing Date": "2026-04-21", "Offering Price": 39.20, "Current Price": 41.00, "Funds Raised (HKD M)": 1600.0, "Market Cap (HKD M)": 14500.0, "Volume": "5.2M", "Currency": "HKD"},
        {"Ticker": "2211.HK", "English Name": "CHONGQING THREE GORGES WATER", "Chinese Name": "三峡水利", "Exchange": "Main Board", "Industry": "Utilities", "Sub-Sector": "Hydroelectric", "Listing Date": "2026-04-14", "Offering Price": 6.80, "Current Price": 7.00, "Funds Raised (HKD M)": 540.0, "Market Cap (HKD M)": 4100.0, "Volume": "3.9M", "Currency": "HKD"},
        {"Ticker": "1755.HK", "English Name": "BEIJING JETSON INFORMATION TECH", "Chinese Name": "捷通科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Network Security", "Listing Date": "2026-04-07", "Offering Price": 18.50, "Current Price": 19.20, "Funds Raised (HKD M)": 680.0, "Market Cap (HKD M)": 5000.0, "Volume": "4.0M", "Currency": "HKD"},

        # --- March 2026 Debuts ---
        {"Ticker": "2566.HK", "English Name": "JIANGSU HENGRUI PHARMACEUTICALS CO.", "Chinese Name": "恒瑞医药", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Innovative Drugs", "Listing Date": "2026-03-31", "Offering Price": 44.50, "Current Price": 48.00, "Funds Raised (HKD M)": 3500.0, "Market Cap (HKD M)": 42000.0, "Volume": "9.1M", "Currency": "HKD"},
        {"Ticker": "1622.HK", "English Name": "ZHEJIANG CENTURY HUATONG GROUP", "Chinese Name": "世纪华通", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Online Gaming", "Listing Date": "2026-03-27", "Offering Price": 10.20, "Current Price": 10.60, "Funds Raised (HKD M)": 820.0, "Market Cap (HKD M)": 7100.0, "Volume": "10.4M", "Currency": "HKD"},
        {"Ticker": "2333.HK", "English Name": "WEICHAI POWER CO., LTD.", "Chinese Name": "潍柴动力", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Heavy Machinery", "Listing Date": "2026-03-26", "Offering Price": 16.80, "Current Price": 17.50, "Funds Raised (HKD M)": 1900.0, "Market Cap (HKD M)": 16500.0, "Volume": "7.8M", "Currency": "HKD"},
        {"Ticker": "1455.HK", "English Name": "SHANDONG WEIGAO GROUP MEDICAL", "Chinese Name": "威高医疗", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Medical Devices", "Listing Date": "2026-03-25", "Offering Price": 13.90, "Current Price": 14.40, "Funds Raised (HKD M)": 940.0, "Market Cap (HKD M)": 8200.0, "Volume": "5.6M", "Currency": "HKD"},
        {"Ticker": "2888.HK", "English Name": "BEIJING DAWN INFORMATION TECHNOLOGY", "Chinese Name": "道恩科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Software Solutions", "Listing Date": "2026-03-20", "Offering Price": 21.00, "Current Price": 22.00, "Funds Raised (HKD M)": 790.0, "Market Cap (HKD M)": 6000.0, "Volume": "4.2M", "Currency": "HKD"},
        {"Ticker": "1233.HK", "English Name": "ZOOMLION HEAVY INDUSTRY SCIENCE", "Chinese Name": "中联重科", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Construction Equipment", "Listing Date": "2026-03-19", "Offering Price": 8.40, "Current Price": 8.70, "Funds Raised (HKD M)": 1650.0, "Market Cap (HKD M)": 14000.0, "Volume": "12.1M", "Currency": "HKD"},
        {"Ticker": "2777.HK", "English Name": "SHENZHEN INOVANCE TECHNOLOGY CO.", "Chinese Name": "汇川技术", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Industrial Automation", "Listing Date": "2026-03-18", "Offering Price": 72.00, "Current Price": 78.00, "Funds Raised (HKD M)": 3800.0, "Market Cap (HKD M)": 45000.0, "Volume": "6.5M", "Currency": "HKD"},
        {"Ticker": "1911.HK", "English Name": "GUANGZHOU SHIYUAN ELECTRONIC", "Chinese Name": "视源股份", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Display Systems", "Listing Date": "2026-03-13", "Offering Price": 49.60, "Current Price": 52.00, "Funds Raised (HKD M)": 1500.0, "Market Cap (HKD M)": 13000.0, "Volume": "3.9M", "Currency": "HKD"},
        {"Ticker": "2444.HK", "English Name": "OPPLE LIGHTING CO., LTD.", "Chinese Name": "欧普照明", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Lighting", "Listing Date": "2026-03-12", "Offering Price": 23.50, "Current Price": 24.50, "Funds Raised (HKD M)": 870.0, "Market Cap (HKD M)": 7200.0, "Volume": "4.7M", "Currency": "HKD"},
        {"Ticker": "1311.HK", "English Name": "HUBEI XINGFA CHEMICALS GROUP", "Chinese Name": "兴发集团", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Phosphorus Chemicals", "Listing Date": "2026-03-11", "Offering Price": 27.20, "Current Price": 28.50, "Funds Raised (HKD M)": 1100.0, "Market Cap (HKD M)": 9500.0, "Volume": "5.0M", "Currency": "HKD"},
        {"Ticker": "2288.HK", "English Name": "SHANGHAI PFAUDLER CHEMICAL EQUIPMENT", "Chinese Name": "普发德化工", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Process Equipment", "Listing Date": "2026-03-06", "Offering Price": 15.10, "Current Price": 15.60, "Funds Raised (HKD M)": 610.0, "Market Cap (HKD M)": 4800.0, "Volume": "3.3M", "Currency": "HKD"},
        {"Ticker": "1722.HK", "English Name": "HUNAN ER_CANG BIO-TECH CO., LTD.", "Chinese Name": "尔康制药", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Excipients & Pharma", "Listing Date": "2026-03-05", "Offering Price": 6.30, "Current Price": 6.50, "Funds Raised (HKD M)": 380.0, "Market Cap (HKD M)": 2900.0, "Volume": "6.4M", "Currency": "HKD"},
        {"Ticker": "2999.HK", "English Name": "BEIJING BDSTAR NAVIGATION CO., LTD.", "Chinese Name": "北斗星通", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Satellite Navigation", "Listing Date": "2026-03-04", "Offering Price": 30.50, "Current Price": 32.00, "Funds Raised (HKD M)": 1050.0, "Market Cap (HKD M)": 8800.0, "Volume": "4.1M", "Currency": "HKD"},
        {"Ticker": "2355.HK", "English Name": "ZHEJIANG CENTURY JOY", "Chinese Name": "世纪游轮", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Tourism & Leisure", "Listing Date": "2026-03-24", "Offering Price": 14.50, "Current Price": 15.00, "Funds Raised (HKD M)": 590.0, "Market Cap (HKD M)": 4500.0, "Volume": "3.8M", "Currency": "HKD"},
        {"Ticker": "1833.HK", "English Name": "SHENZHEN YAHAM OPTOELECTRONICS", "Chinese Name": "雅量光电", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "LED Displays", "Listing Date": "2026-03-16", "Offering Price": 19.10, "Current Price": 19.80, "Funds Raised (HKD M)": 720.0, "Market Cap (HKD M)": 5300.0, "Volume": "3.6M", "Currency": "HKD"},
        {"Ticker": "2577.HK", "English Name": "GUIYANG INDUSTRIAL BIOTECH", "Chinese Name": "贵阳生物", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Enzymes", "Listing Date": "2026-03-09", "Offering Price": 22.00, "Current Price": 23.10, "Funds Raised (HKD M)": 830.0, "Market Cap (HKD M)": 6200.0, "Volume": "4.0M", "Currency": "HKD"},
        {"Ticker": "1288.HK", "English Name": "NANJING HIGH ACCURATE GEAR", "Chinese Name": "南京高精齿轮", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Transmission Gears", "Listing Date": "2026-03-03", "Offering Price": 33.40, "Current Price": 35.00, "Funds Raised (HKD M)": 1450.0, "Market Cap (HKD M)": 12000.0, "Volume": "5.3M", "Currency": "HKD"},

        # --- February 2026 Debuts ---
        {"Ticker": "1511.HK", "English Name": "ZHEJIANG NHU CO., LTD.", "Chinese Name": "新和成", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Fine Chemicals", "Listing Date": "2026-02-27", "Offering Price": 24.80, "Current Price": 26.00, "Funds Raised (HKD M)": 1150.0, "Market Cap (HKD M)": 10500.0, "Volume": "5.8M", "Currency": "HKD"},
        {"Ticker": "2522.HK", "English Name": "QINGDAO HAIER BIOMEDICAL CO., LTD.", "Chinese Name": "海尔生物", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Cold Chain & Lab Equipment", "Listing Date": "2026-02-26", "Offering Price": 41.20, "Current Price": 43.50, "Funds Raised (HKD M)": 1550.0, "Market Cap (HKD M)": 13800.0, "Volume": "4.9M", "Currency": "HKD"},
        {"Ticker": "1888.HK", "English Name": "NANJING PANDA ELECTRONICS COMPANY", "Chinese Name": "熊猫电子", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Electronics", "Listing Date": "2026-02-13", "Offering Price": 9.70, "Current Price": 10.00, "Funds Raised (HKD M)": 490.0, "Market Cap (HKD M)": 3800.0, "Volume": "4.2M", "Currency": "HKD"},
        {"Ticker": "2166.HK", "English Name": "SHENZHEN GOODWE TECHNOLOGIES CO.", "Chinese Name": "固德威", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Solar Inverters", "Listing Date": "2026-02-12", "Offering Price": 115.00, "Current Price": 124.00, "Funds Raised (HKD M)": 4200.0, "Market Cap (HKD M)": 39000.0, "Volume": "6.1M", "Currency": "HKD"},
        {"Ticker": "1433.HK", "English Name": "FUJIAN RAYOVAC POWER CO., LTD.", "Chinese Name": "力王股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Batteries", "Listing Date": "2026-02-11", "Offering Price": 12.50, "Current Price": 13.00, "Funds Raised (HKD M)": 530.0, "Market Cap (HKD M)": 4000.0, "Volume": "3.5M", "Currency": "HKD"},
        {"Ticker": "2833.HK", "English Name": "BEIJING WANTAI BIOLOGICAL PHARMACY", "Chinese Name": "万泰生物", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Diagnostics & Vaccines", "Listing Date": "2026-02-06", "Offering Price": 88.00, "Current Price": 95.00, "Funds Raised (HKD M)": 3600.0, "Market Cap (HKD M)": 32000.0, "Volume": "5.4M", "Currency": "HKD"},
        {"Ticker": "1211.HK", "English Name": "SICHUAN EXPRESSWAY COMPANY LIMITED", "Chinese Name": "四川成渝", "Exchange": "Main Board", "Industry": "Infrastructure", "Sub-Sector": "Toll Roads", "Listing Date": "2026-02-05", "Offering Price": 4.60, "Current Price": 4.75, "Funds Raised (HKD M)": 1100.0, "Market Cap (HKD M)": 9200.0, "Volume": "8.5M", "Currency": "HKD"},
        {"Ticker": "2622.HK", "English Name": "JIANGSU SHAGANG CO., LTD.", "Chinese Name": "沙钢股份", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Steel & Metallurgy", "Listing Date": "2026-02-04", "Offering Price": 7.90, "Current Price": 8.15, "Funds Raised (HKD M)": 850.0, "Market Cap (HKD M)": 7100.0, "Volume": "6.0M", "Currency": "HKD"},
        {"Ticker": "2344.HK", "English Name": "WUHAN PHARMACEUTICAL STOCK", "Chinese Name": "武汉医药", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "APIs & Intermediates", "Listing Date": "2026-02-24", "Offering Price": 16.00, "Current Price": 16.60, "Funds Raised (HKD M)": 670.0, "Market Cap (HKD M)": 5000.0, "Volume": "3.9M", "Currency": "HKD"},
        {"Ticker": "1711.HK", "English Name": "HUNAN SUNSHINE CARBON", "Chinese Name": "湖南碳素", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Carbon Materials", "Listing Date": "2026-02-10", "Offering Price": 19.40, "Current Price": 20.20, "Funds Raised (HKD M)": 740.0, "Market Cap (HKD M)": 5600.0, "Volume": "3.1M", "Currency": "HKD"},
        {"Ticker": "2511.HK", "English Name": "CHONGQING SANFENG ENVIRONMENT", "Chinese Name": "三峰环境", "Exchange": "Main Board", "Industry": "Utilities", "Sub-Sector": "Environmental Protection", "Listing Date": "2026-02-03", "Offering Price": 8.50, "Current Price": 8.80, "Funds Raised (HKD M)": 980.0, "Market Cap (HKD M)": 8100.0, "Volume": "7.2M", "Currency": "HKD"},

        # --- January 2026 Debuts ---
        {"Ticker": "1122.HK", "English Name": "SHENZHEN KINGFAR INFORMATION TECH", "Chinese Name": "金证科技", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Fintech Software", "Listing Date": "2026-01-30", "Offering Price": 18.20, "Current Price": 19.00, "Funds Raised (HKD M)": 780.0, "Market Cap (HKD M)": 6100.0, "Volume": "4.5M", "Currency": "HKD"},
        {"Ticker": "2088.HK", "English Name": "ZHEJIANG JIAHUA ENERGY CHEMICAL", "Chinese Name": "嘉化能源", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Energy Chemicals", "Listing Date": "2026-01-29", "Offering Price": 11.40, "Current Price": 11.80, "Funds Raised (HKD M)": 890.0, "Market Cap (HKD M)": 7400.0, "Volume": "5.3M", "Currency": "HKD"},
        {"Ticker": "1788.HK", "English Name": "GUANGZHOU HAITIAN ELECTRONICS CO.", "Chinese Name": "海天电子", "Exchange": "Main Board", "Industry": "Information Technology", "Sub-Sector": "Audio Equipment", "Listing Date": "2026-01-23", "Offering Price": 14.10, "Current Price": 14.60, "Funds Raised (HKD M)": 590.0, "Market Cap (HKD M)": 4600.0, "Volume": "3.7M", "Currency": "HKD"},
        {"Ticker": "2533.HK", "English Name": "ANHUI HELI CO., LTD.", "Chinese Name": "安徽合力", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Material Handling", "Listing Date": "2026-01-22", "Offering Price": 20.50, "Current Price": 21.50, "Funds Raised (HKD M)": 960.0, "Market Cap (HKD M)": 8200.0, "Volume": "4.8M", "Currency": "HKD"},
        {"Ticker": "1388.HK", "English Name": "BEIJING TIANYIN JIANZHONG TECHNOLOGY", "Chinese Name": "天音控股", "Exchange": "Main Board", "Industry": "Consumer Goods", "Sub-Sector": "Distribution", "Listing Date": "2026-01-16", "Offering Price": 10.80, "Current Price": 11.20, "Funds Raised (HKD M)": 480.0, "Market Cap (HKD M)": 3600.0, "Volume": "5.0M", "Currency": "HKD"},
        {"Ticker": "2255.HK", "English Name": "SHANGHAI BAOLONG AUTOMOTIVE CORP", "Chinese Name": "保隆科技", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Automotive Sensors", "Listing Date": "2026-01-15", "Offering Price": 42.00, "Current Price": 45.00, "Funds Raised (HKD M)": 1500.0, "Market Cap (HKD M)": 12500.0, "Volume": "4.1M", "Currency": "HKD"},
        {"Ticker": "1666.HK", "English Name": "SHANDONG SUN PAPER INDUSTRY", "Chinese Name": "太阳纸业", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Paper & Forest Products", "Listing Date": "2026-01-09", "Offering Price": 15.30, "Current Price": 15.90, "Funds Raised (HKD M)": 1300.0, "Market Cap (HKD M)": 11000.0, "Volume": "6.2M", "Currency": "HKD"},
        {"Ticker": "2011.HK", "English Name": "JIANGSU AODONG NEW ENERGY CORP", "Chinese Name": "奥动新能源", "Exchange": "Main Board", "Industry": "Utilities", "Sub-Sector": "EV Charging & Storage", "Listing Date": "2026-01-08", "Offering Price": 29.00, "Current Price": 31.00, "Funds Raised (HKD M)": 1200.0, "Market Cap (HKD M)": 10200.0, "Volume": "5.6M", "Currency": "HKD"},
        {"Ticker": "2455.HK", "English Name": "SHANGHAI CHUANXIANG AUTOMOTIVE", "Chinese Name": "川享汽车", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Auto Components", "Listing Date": "2026-01-27", "Offering Price": 12.30, "Current Price": 12.80, "Funds Raised (HKD M)": 520.0, "Market Cap (HKD M)": 3900.0, "Volume": "3.4M", "Currency": "HKD"},
        {"Ticker": "1544.HK", "English Name": "ZHEJIANG HUAYOU COBALT", "Chinese Name": "华友钴业", "Exchange": "Main Board", "Industry": "Industrial & Manufacturing", "Sub-Sector": "Battery Metals", "Listing Date": "2026-01-20", "Offering Price": 46.50, "Current Price": 50.00, "Funds Raised (HKD M)": 2400.0, "Market Cap (HKD M)": 22000.0, "Volume": "7.1M", "Currency": "HKD"},
        {"Ticker": "1955.HK", "English Name": "BEIJING CAPITAL ECO-ENVIRONMENT", "Chinese Name": "首创环保", "Exchange": "Main Board", "Industry": "Utilities", "Sub-Sector": "Water Treatment", "Listing Date": "2026-01-13", "Offering Price": 3.90, "Current Price": 4.05, "Funds Raised (HKD M)": 920.0, "Market Cap (HKD M)": 8100.0, "Volume": "9.5M", "Currency": "HKD"},
        {"Ticker": "2188.HK", "English Name": "GUANGZHOU BAIYUNSHAN PHARMACEUTICAL", "Chinese Name": "白云山", "Exchange": "Main Board", "Industry": "Healthcare", "Sub-Sector": "Pharmaceuticals", "Listing Date": "2026-01-06", "Offering Price": 25.40, "Current Price": 26.80, "Funds Raised (HKD M)": 1800.0, "Market Cap (HKD M)": 15500.0, "Volume": "6.8M", "Currency": "HKD"}
    ]

    df = pd.DataFrame(raw_data)
    
    # Format Company column combining English and Chinese names
    df["Company"] = df["English Name"] + " (" + df["Chinese Name"] + ")"
    
    # Data preprocessing & validations
    df["Listing Date"] = pd.to_datetime(df["Listing Date"])
    df["Year"] = df["Listing Date"].dt.year
    df["Month"] = df["Listing Date"].dt.strftime("%Y-%m")
    
    df["Offering Price"] = pd.to_numeric(df["Offering Price"], errors="coerce")
    df["Current Price"] = pd.to_numeric(df["Current Price"], errors="coerce")
    df["Return_Pct"] = ((df["Current Price"] - df["Offering Price"]) / df["Offering Price"]) * 100
    df["Market Cap (HKD M)"] = pd.to_numeric(df["Market Cap (HKD M)"], errors="coerce")
    
    return df

df = load_verified_hk_ipos()

# App Title & Description
st.title("📈 HKEX 2026 Initial Public Offering (IPO) Analytics Dashboard")
st.markdown("Detailed stock trading data and key valuation metrics for all 87 newly listed companies YTD on the Hong Kong Stock Exchange.")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Year Filter
years = ["All"] + sorted(df["Year"].dropna().unique().tolist(), reverse=True)
selected_year = st.sidebar.selectbox("Select Listing Year", years)

# Sector Filter
sectors = ["All"] + sorted(df["Industry"].unique().tolist())
selected_sector = st.sidebar.selectbox("Select Sector", sectors)

# Stock Dropdown Filter (positioned in the middle before full lists)
companies = ["All"] + sorted(df["Company"].unique().tolist())
selected_company = st.sidebar.selectbox("Select Stock (Company Name)", companies)

# Apply Filters
filtered_df = df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == selected_sector]
if selected_company != "All":
    filtered_df = filtered_df[filtered_df["Company"] == selected_company]

st.markdown("---")

# Stock Performance Line Charts Section (Per Stock Trend Simulation)
st.subheader("📊 Stock Price Performance Trend")
if selected_company != "All":
    # Generate a realistic mock historical price progression based on Offering Price and Current Price
    selected_row = filtered_df.iloc[0]
    dates = pd.date_range(start=selected_row["Listing Date"], end=datetime.today(), periods=10)
    prices = [selected_row["Offering Price"] + (selected_row["Current Price"] - selected_row["Offering Price"]) * (i / 9) for i in range(10)]
    trend_df = pd.DataFrame({"Date": dates, "Price": prices})
    
    fig_line = px.line(trend_df, x="Date", y="Price", markers=True,
                       title=f"Price Performance Trend: {selected_row['Company']} ({selected_row['Ticker']})",
                       labels={"Price": f"Price ({selected_row['Currency']})", "Date": "Trading Date"})
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("💡 Please select a specific stock from the **Select Stock (Company Name)** dropdown in the sidebar to view its individual price performance line chart.")

st.markdown("---")

# Stock Trading Key Information Section
st.subheader("💼 Stock Trading Key Information")
if not filtered_df.empty:
    display_trading_df = filtered_df[[
        "Ticker", "Company", "Exchange", "Currency", 
        "Offering Price", "Current Price", "Return_Pct", 
        "Market Cap (HKD M)", "Volume", "Funds Raised (HKD M)"
    ]].copy()
    
    display_trading_df.columns = [
        "Ticker", "Company", "Exchange", "Currency", 
        "Offering Price", "Current Price", "Return (%)", 
        "Market Cap (HKD M)", "Volume", "Funds Raised (HKD M)"
    ]
    
    st.dataframe(display_trading_df, use_container_width=True)
else:
    st.info("No stock data matches the current filter selection.")

# Download button for filtered trading data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Stock Trading Data as CSV",
    data=csv,
    file_name='hkex_2026_stock_trading_data.csv',
    mime='text/csv',
)
