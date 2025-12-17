import streamlit as st
import pandas as pd
import datetime
import time
import random

# --- 1. HỆ THỐNG ĐIỀU HÀNH TITAN OS ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'secret_mode' not in st.session_state: st.session_state.secret_mode = False
if 'xp' not in st.session_state: st.session_state.xp = 0

def nav(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. GIAO DIỆN DARK TITANIUM (CHỐNG LỖI HIỂN THỊ) ---
st.set_page_config(page_title="Titan OS v21.1", layout="wide", page_icon="🛡️")

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
        transform: translateY(-3px);
    }
    .status-bar { font-family: 'Courier New'; color: #00f2ff; text-align: right; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC XỬ LÝ MÀN HÌNH ---

# MÀN HÌNH CHÍNH (DESKTOP)
if st.session_state.page == "Desktop":
    st.markdown("<div class='status-bar'>📶 TITAN-6G | 🔋 100% | BOSS MODE</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🛡️ TITAN OS PRO</h1>", unsafe_allow_html=True)
    
    st.write("###")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🅿️\nPARKING\n(Bãi Xe)"): nav("Parking")
        if st.button("📖\nGUIDE\n(Hướng Dẫn)"): nav("Guide")
    with c2:
        if st.button("🌳\nBOTANY\n(Trồng Cây)"): nav("Garden")
        if st.button("⚙️\nSYSTEM\n(Cài Đặt)"): nav("Settings")
    with c3:
        if st.button("🐍\nPY-SHELL\n(Lập Trình)"): nav("Console")
        if st.button("🔒\nSLEEP"): nav("Lock")

# APP 1: HƯỚNG DẪN SỬ DỤNG
elif st.session_state.page == "Guide":
    st.button("🔙 DESKTOP", on_click=lambda: nav("Desktop"))
    st.header("📖 Hướng Dẫn Sử Dụng Hệ Thống")
    st.info("Chào Boss! Đây là cách vận hành X-OS của bạn:")
    st.markdown("""
    - **Parking:** Nhập xe vào bãi, dữ liệu sẽ lưu Cloud vĩnh viễn.
    - **Botany:** Thay thế trồng hẹ. Boss có thể chụp ảnh cây thật để lưu nhật ký lớn lên của cây.
    - **Settings:** Nơi chứa các 'Trứng phục sinh'. Hãy thử nhấn liên tục vào phiên bản hệ thống.
    """)

# APP 2: TRỒNG CÂY (REPLACE TRỒNG HẸ)
elif st.session_state.page == "Garden":
    st.button("🔙 DESKTOP", on_click=lambda: nav("Desktop"))
    st.header("🌳 Eco-Botany Studio")
    st.write(f"Cấp độ người làm vườn: **{st.session_state.xp} XP**")
    
    c1, c2 = st.columns(2)
    with c1:
        st.camera_input("Chụp ảnh cây hôm nay (Lưu nhật ký)")
    with c2:
        plant_type = st.text_input("Tên cây đang trồng:", "Cây thần kỳ")
        action = st.selectbox("Hành động:", ["Tưới nước", "Bón phân", "Bắt sâu", "Nói chuyện"])
        if st.button("THỰC HIỆN"):
            st.session_state.xp += 10
            st.success(f"Đã {action} cho {plant_type}!")
            st.balloons()

# APP 3: CÀI ĐẶT & TÍNH NĂNG ẨN
elif st.session_state.page == "Settings":
    st.button("🔙 DESKTOP", on_click=lambda: nav("Desktop"))
    st.header("⚙️ System Control")
    
    ver_text = "Phiên bản: Titan OS v21.1.0-Release"
    if st.button(ver_text):
        if 'click_count' not in st.session_state: st.session_state.click_count = 0
        st.session_state.click_count += 1
        if st.session_state.click_count >= 7:
            st.session_state.secret_mode = True
            st.success("🔓 DEVELOPER OPTIONS UNLOCKED!")

    if st.session_state.secret_mode:
        st.divider()
        st.subheader("🔥 Hidden Features")
        if st.button("🌈 Disco Mode"):
            st.markdown("<style>.stApp { background-color: #2b0000 !important; }</style>", unsafe_allow_html=True)
            st.toast("Kích hoạt chế độ phòng Lab!")
        st.download_button("📥 Dump System Data", "Dữ liệu bí mật...", "secrets.txt")
        if st.button("Reset Secret"): st.session_state.secret_mode = False; st.rerun()

# CÁC MÀN HÌNH KHÁC
elif st.session_state.page == "Parking":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🅿️ Quản Lý Xe")
    st.text_input("Biển số xe")
    st.button("Lưu lên Sheets")

elif st.session_state.page == "Console":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🐍 Python Console")
    st.code("print('Boss đang lập trình...')")

elif st.session_state.page == "Lock":
    st.markdown("<h1 style='text-align:center; margin-top:150px;'>Hệ thống đang khóa...</h1>", unsafe_allow_html=True)
    if st.button("MỞ KHÓA"): nav("Desktop")
