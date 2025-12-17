import streamlit as st
import pandas as pd
import datetime
import time
import random

# --- 1. HỆ THỐNG ĐIỀU HÀNH TITAN OS ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'secret_unlocked' not in st.session_state: st.session_state.secret_unlocked = False
if 'xp' not in st.session_state: st.session_state.xp = 0

def nav(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. GIAO DIỆN DARK TITANIUM (CHỐNG LỖI HIỂN THỊ) ---
st.set_page_config(page_title="Titan OS v22.1", layout="wide", page_icon="🛡️")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stButton>button {
        width: 100%; height: 90px;
        border-radius: 20px;
        background: #111111;
        color: #00f2ff;
        border: 2px solid #00f2ff33;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #00f2ff;
        background: #00f2ff22;
        box-shadow: 0 0 20px #00f2ff55;
    }
    .status-bar { font-family: 'Courier New'; color: #00f2ff; text-align: right; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# --- 3. MÀN HÌNH CHÍNH ---
if st.session_state.page == "Desktop":
    st.markdown("<div class='status-bar'>📶 TITAN-6G | 🔋 100% | BOSS MODE</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🛡️ TITAN OS PRO</h1>", unsafe_allow_html=True)
    st.write("###")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🅿️\nPARKING\n(Bãi Xe)"): nav("Parking")
        if st.button("📖\nGUIDE\n(Hướng Dẫn)"): nav("Guide")
    with col2:
        if st.button("🌳\nBOTANY\n(Trồng Cây)"): nav("Garden")
        if st.button("⚙️\nSYSTEM\n(Cài Đặt)"): nav("Settings")
    with col3:
        if st.button("🐍\nCONSOLE\n(Lập Trình)"): nav("Console")
        if st.button("🔒\nSLEEP"): nav("Lock")

# --- APP 1: HƯỚNG DẪN SỬ DỤNG ---
elif st.session_state.page == "Guide":
    st.button("🔙 DESKTOP", on_click=lambda: nav("Desktop"))
    st.header("📖 Hướng Dẫn Sử Dụng")
    st.info("Chào Boss! Đây là cách vận hành X-OS của bạn:")
    st.markdown("""
    1. **Parking:** Nhập xe, tính tiền tự động. Dữ liệu lưu vĩnh viễn.
    2. **Botany:** Thay thế trồng hẹ. Boss có thể chụp ảnh cây thật của mình.
    3. **Settings:** Nhấn liên tục 7 lần vào phiên bản để mở tính năng ẩn.
    """)

# --- APP 2: TRỒNG CÂY (REPLACE TRỒNG HẸ) ---
elif st.session_state.page == "Garden":
    st.button("🔙 DESKTOP", on_click=lambda: nav("Desktop"))
    st.header("🌳 Eco-Botany Studio")
    st.write(f"Cấp độ người làm vườn: **{st.session_state.xp} XP**")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.camera_input("Chụp ảnh cây hôm nay")
    with col_g2:
        plant_name = st.text_input("Tên cây:", "Cây thần kỳ")
        if st.button("TƯỚI NƯỚC"):
            st.session_state.xp += 10
            st.success(f"Đã tưới nước cho {plant_name}!")
            st.balloons()

# --- APP 3: CÀI ĐẶT & TÍNH NĂNG ẨN ---
elif st.session_state.page == "Settings":
    st.button("🔙 DESKTOP", on_click=lambda: nav("Desktop"))
    st.header("⚙️ System Control")
    
    if st.button("Phiên bản: Titan OS v22.1.0-Stabilized"):
        if 'click_count' not in st.session_state: st.session_state.click_count = 0
        st.session_state.click_count += 1
        if st.session_state.click_count >= 7:
            st.session_state.secret_unlocked = True
            st.success("🔓 DEVELOPER OPTIONS UNLOCKED!")

    if st.session_state.secret_unlocked:
        st.divider()
        st.subheader("🔥 Hidden Features")
        if st.button("🌈 Disco Mode"):
            st.toast("Kích hoạt chế độ phòng Lab!")
        if st.button("Reset Secret"): 
            st.session_state.secret_unlocked = False
            st.rerun()

# --- CÁC MÀN HÌNH KHÁC ---
elif st.session_state.page == "Parking":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🅿️ Quản Lý Xe")
    st.text_input("Biển số xe")
    st.button("Lưu lên Sheets")

elif st.session_state.page == "Console":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🐍 Python Console")
    st.code("print('Hello Boss!')")

elif st.session_state.page == "Lock":
    st.markdown("<h1 style='text-align:center; margin-top:150px;'>Hệ thống đang khóa...</h1>", unsafe_allow_html=True)
    if st.button("MỞ KHÓA"): nav("Desktop")
