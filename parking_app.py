import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math

# --- 1. CORE LOGIC ---
if 'current_app' not in st.session_state: st.session_state.current_app = "Desktop"

def open_app(app_name):
    st.session_state.current_app = app_name

# --- 2. GIAO DIỆN DARK NEON (FIX HIỂN THỊ) ---
st.set_page_config(page_title="Nebula OS v18.1", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #00d4ff; }
    /* Nút bấm khổng lồ và luôn nổi bật */
    .stButton>button {
        width: 100% !important;
        height: 150px !important;
        background: linear-gradient(145deg, #1a1a1a, #252525) !important;
        color: #00d4ff !important;
        border: 2px solid #00d4ff !important;
        border-radius: 25px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2) !important;
        display: block !important;
    }
    .stButton>button:hover {
        background: #00d4ff !important;
        color: #000000 !important;
        box-shadow: 0 0 30px #00d4ff !important;
    }
    /* Chữ tiêu đề */
    h1, h2, h3 { color: #ffffff !important; text-shadow: 0 0 10px #00d4ff; }
</style>
""", unsafe_allow_html=True)

# --- 3. MÀN HÌNH CHÍNH (DESKTOP) ---
if st.session_state.current_app == "Desktop":
    st.markdown("<h1 style='text-align: center;'>🌌 NEBULA OS V18.1</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: #888;'>HỆ THỐNG ĐANG SẴN SÀNG</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # Chia cột rõ ràng để hiện nút
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 VÀO BÃI\n(Inbound)"): open_app("In")
        if st.button("🏢 BÃI XE\n(Storage)"): open_app("Status")
        
    with col2:
        if st.button("📤 XE RA\n(Outbound)"): open_app("Out")
        if st.button("⚙️ CÀI ĐẶT\n(System)"): open_app("Settings")

    st.write("---")
    # Ô lệnh bí mật đẩy xuống dưới cùng để không che nút
    cmd = st.text_input("Terminal Command (Mật mã):", type="password")
    if cmd == "6666": 
        st.success("BOSS MODE ACTIVATED!")
        st.balloons()

# --- CÁC APP CON (NỘI DUNG) ---
elif st.session_state.current_app == "In":
    if st.button("🔙 QUAY LẠI MÀN HÌNH CHÍNH"): open_app("Desktop")
    st.header("📥 NHẬP XE MỚI")
    lp = st.text_input("BIỂN SỐ:").upper()
    if st.button("XÁC NHẬN LƯU"): st.success(f"Đã nạp {lp}")

elif st.session_state.current_app == "Status":
    if st.button("🔙 QUAY LẠI MÀN HÌNH CHÍNH"): open_app("Desktop")
    st.header("🏢 TRẠNG THÁI BÃI")
    st.info("Danh sách xe sẽ hiện ở đây...")

elif st.session_state.current_app == "Out":
    if st.button("🔙 QUAY LẠI MÀN HÌNH CHÍNH"): open_app("Desktop")
    st.header("📤 THANH TOÁN")
    st.write("Chọn xe cần thanh toán...")

elif st.session_state.current_app == "Settings":
    if st.button("🔙 QUAY LẠI MÀN HÌNH CHÍNH"): open_app("Desktop")
    st.header("⚙️ CÀI ĐẶT HỆ THỐNG")
    st.write("Số hiệu bản dựng: PK-2025-V18.1")
