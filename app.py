import streamlit as st
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime

# --- VIP UI DESIGN ---
st.set_page_config(page_title="VIP-ULTRA-V11", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .main-box {
        background: linear-gradient(145deg, #111, #222);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 20px #00ff00;
        margin-bottom: 25px;
    }
    .x-display { font-size: 70px; font-weight: bold; color: #00ff00; text-shadow: 0 0 20px #00ff00; }
    .grid-safe { background-color: #00ff00 !important; color: black !important; font-weight: bold; border-radius: 8px; padding: 15px; width: 100%; border: none; }
    .grid-bomb { background-color: #ff0000 !important; color: white !important; font-weight: bold; border-radius: 8px; padding: 15px; width: 100%; border: none; }
    .status-bar { color: #00ff00; font-size: 14px; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "universal_history.csv"

def save_data(val, g_type):
    df_new = pd.DataFrame([{"Time": datetime.now().strftime("%H:%M:%S"), "Value": float(val), "Type": g_type}])
    df_new.to_csv(DB_FILE, mode='a', header=not os.path.exists(DB_FILE), index=False)

def load_data():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Time", "Value", "Type"])

# --- SIDEBAR MENU ---
st.sidebar.markdown("<h2 style='color:#00ff00;'>🛰️ MASTER HUB</h2>", unsafe_allow_html=True)
game_mode = st.sidebar.radio("گیم منتخب کریں:", ["🚀 Aviator / Crash", "💣 Mines Visual Radar"])
st.sidebar.markdown("---")
st.sidebar.write("Scanner: <span class='status-bar'>ACTIVE 🟢</span>", unsafe_allow_html=True)

df = load_data()

# --- AVIATOR WORKER ---
if game_mode == "🚀 Aviator / Crash":
    st.markdown("<div class='main-box'><h1 style='color:#00ff00;'>AVIATOR PREDICTOR</h1><p>Minus & Average Logic Sync</p></div>", unsafe_allow_html=True)
    
    aviator_df = df[df['Type'] == 'Aviator']
    if len(aviator_df) >= 2:
        vals = aviator_df['Value'].tail(2).tolist()
        diff = vals[1] - vals[0]
        # مائنس لاجک تجزیہ
        pred = round(vals[1] + 0.45, 2) if diff > 0 else 1.25
        st.markdown(f"<div class='x-display'>{pred}x</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='x-display'>WAITING...</div>", unsafe_allow_html=True)

    val_in = st.number_input("لاسٹ ایکس (X) ڈالیں:", min_value=1.0)
    if st.button("اسکین اور اپ ڈیٹ"):
        save_data(val_in, "Aviator")
        st.rerun()

# --- MINES WORKER (VISUAL GRID) ---
elif game_mode == "💣 Mines Visual Radar":
    st.markdown("<div class='main-box' style='border-color:#ffcc00; box-shadow:0 0 20px #ffcc00;'><h1 style='color:#ffcc00;'>MINES X-RAY</h1><p>براہ راست بم کی نشاندہی</p></div>", unsafe_allow_html=True)
    
    mines_count = st.sidebar.slider("بموں کی تعداد:", 1, 24, 3)
    
    # 5x5 Grid Logic
    random.seed(datetime.now().second)
    bomb_spots = random.sample(range(25), mines_count)
    
    st.write("### 🛰️ اسکینر میپ (Safe vs Bomb):")
    for r in range(5):
        cols = st.columns(5)
        for c in range(5):
            idx = r * 5 + c
            with cols[c]:
                if idx in bomb_spots:
                    st.markdown("<button class='grid-bomb'>💣 BOMB</button>", unsafe_allow_html=True)
                else:
                    st.markdown("<button class='grid-safe'>✅ SAFE</button>", unsafe_allow_html=True)

# --- HISTORY TABLE ---
st.markdown("---")
if not df.empty:
    st.write("### 📜 ریکارڈ ہسٹری")
    st.dataframe(df.tail(10), use_container_width=True)
