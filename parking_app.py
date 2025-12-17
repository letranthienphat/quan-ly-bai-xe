import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import time
import random

# --- 1. CORE OS ENGINE ---
if 'page' not in st.session_state: st.session_state.page = "LockScreen"
if 'booted' not in st.session_state: st.session_state.booted = False

def navigate(p): st.session_state.page = p

# --- 2. GIAO DIỆN X-OS (CYBERPUNK STYLE) ---
st.set_page_config(page_title="X-OS Multiverse", layout="wide", page_icon="🧬")

st.markdown("""
<style>
    .stApp { background: #000000; color: #ff00ff; }
    /* Icon App hình tròn độc lạ */
    .stButton>button {
        border-radius: 50% !important;
        width: 120px !important; height: 120px !important;
        background: rgba(255, 0, 255, 0.1) !important;
        border: 2px solid #ff00ff !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 14px !important;
        box-shadow: 0 0 15px #ff00ff !important;
    }
    .stButton>button:hover {
        background: #ff00ff !important;
        color: #000 !important;
        box-shadow: 0 0 40px #ff00ff !important;
    }
    .status-bar { font-family: 'Courier New'; font-size: 12px; color: #00ff00; text-align: right; }
</style>
""", unsafe_allow_html=True)

# --- 3. MÀN HÌNH KHÓA (GIAO DIỆN ĐỘC LẠ 1) ---
if st.session_state.page == "LockScreen":
    st.markdown("<h1 style='text-align: center; margin-top: 100px; color: #ff00ff;'>X - O S</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: white;'>{datetime.datetime.now().strftime('%H:%M')}</h2>", unsafe_allow_html=True)
    st.write("###")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("UNLOCK\nSYSTEM"):
            with st.spinner("Đang quét sinh trắc học..."):
                time.sleep(1)
                navigate("Desktop")
                st.rerun()

# --- 4. MÀN HÌNH CHÍNH (DESKTOP) ---
elif st.session_state.page == "Desktop":
    st.markdown("<div class='status-bar'>📶 5G | 🔋 98% | BOSS MODE</div>", unsafe_allow_html=True)
    st.title("🧬 Multiverse Desktop")
    
    st.write("---")
    # Lưới ứng dụng
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🅿️\nBãi Xe"): navigate("Parking")
    with c2:
        if st.button("🌿\nTrồng Hẹ"): navigate("HeApp")
    with c3:
        if st.button("🐍\nPython\nTerminal"): navigate("Terminal")
    with c4:
        if st.button("🎲\nGame\nMay Rủi"): navigate("Game")

    st.divider()
    if st.button("🔒 Khóa máy"): navigate("LockScreen"); st.rerun()

# --- 5. CÁC ỨNG DỤNG (APPS) ---

# APP 1: QUẢN LÝ BÃI XE (PARKING)
elif st.session_state.page == "Parking":
    st.button("⬅️ Back", on_click=lambda: navigate("Desktop"))
    st.header("🅿️ HỆ THỐNG BÃI XE")
    tab1, tab2 = st.tabs(["Vào Bãi", "Trạng Thái"])
    with tab1:
        lp = st.text_input("Biển số").upper()
        if st.button("Xác nhận"): st.success(f"Đã lưu {lp}")
    with tab2:
        st.info("Dữ liệu đang được đồng bộ từ Cloud...")

# APP 2: TRỒNG HẸ (ỨNG DỤNG DÀNH RIÊNG CHO BẠN)
elif st.session_state.page == "HeApp":
    st.button("⬅️ Back", on_click=lambda: navigate("Desktop"))
    st.header("🌿 Nhật Ký Trồng Hẹ")
    st.write("Theo dõi sự phát triển của vườn hẹ của bạn.")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.metric("Ngày trồng", "30/08/2025")
        st.metric("Trạng thái", "Đang phát triển tốt")
    with col_h2:
        water = st.slider("Lượng nước tưới (%)", 0, 100, 50)
        if st.button("Ghi chú hôm nay"): st.toast("Đã ghi nhận: Hẹ xanh mướt!")

# APP 3: TERMINAL (DÀNH CHO DÂN LẬP TRÌNH PYTHON)
elif st.session_state.page == "Terminal":
    st.button("⬅️ Back", on_click=lambda: navigate("Desktop"))
    st.header("🐍 Python Code Runner")
    code = st.text_area("Nhập code Python của bạn tại đây:", value="print('Hello từ X-OS!')")
    if st.button("EXECUTE"):
        st.markdown("### Output:")
        st.code(">>> " + code + "\nSuccess: Code executed in virtual environment.")

# APP 4: GAME GIẢI TRÍ (MAY RỦI)
elif st.session_state.page == "Game":
    st.button("⬅️ Back", on_click=lambda: navigate("Desktop"))
    st.header("🎲 Trò chơi May Rủi")
    if st.button("QUAY SỐ"):
        num = random.randint(1, 100)
        if num > 80: st.balloons(); st.success(f"Con số may mắn: {num} - BẠN ĐÃ THẮNG!")
        else: st.error(f"Con số: {num} - Chúc bạn may mắn lần sau!")
