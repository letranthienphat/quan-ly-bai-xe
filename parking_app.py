import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import time
import random

# --- 1. CORE OS ENGINE (ZENITH CORE) ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'tree_health' not in st.session_state: st.session_state.tree_health = 100

def navigate(p): 
    st.session_state.page = p
    st.rerun()

# --- 2. GIAO DIỆN ZENITH (DARK EMERALD STYLE) ---
st.set_page_config(page_title="Zenith OS v20.0", layout="wide", page_icon="🧬")

st.markdown("""
<style>
    /* Nền đen xanh lục bảo cực sang trọng và rõ chữ */
    .stApp { background: linear-gradient(180deg, #001a1a 0%, #000000 100%); color: #00ffcc; }
    
    /* Icon App kiểu Neumorphism phát sáng */
    .stButton>button {
        border-radius: 20px !important;
        width: 100% !important; height: 100px !important;
        background: rgba(0, 255, 204, 0.05) !important;
        border: 1px solid #00ffcc !important;
        color: #ffffff !important;
        font-weight: bold !important;
        transition: 0.3s !important;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.2) !important;
    }
    .stButton>button:hover {
        background: #00ffcc !important;
        color: #001a1a !important;
        box-shadow: 0 0 30px #00ffcc !important;
        transform: translateY(-5px);
    }
    .status-bar { font-family: 'Monaco'; font-size: 13px; color: #00ffcc; border-bottom: 1px solid #00ffcc33; padding: 5px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. STATUS BAR (GIỐNG SMARTPHONE) ---
st.markdown(f"<div class='status-bar'>🔋 99% | 📶 ZENITH-NET | 🛡️ SECURE MODE | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)

# --- 4. LOGIC MÀN HÌNH ---

# MÀN HÌNH CHÍNH (DESKTOP)
if st.session_state.page == "Desktop":
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>ZENITH OS</h1>", unsafe_allow_html=True)
    
    # Grid Ứng Dụng
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🅿️\nPARKING PRO\n(Bãi Xe)"): navigate("Parking")
        if st.button("🌳\nECO GARDEN\n(Trồng Cây)"): navigate("Garden")
    with col2:
        if st.button("🐍\nPY-TERMINAL\n(Lập Trình)"): navigate("Terminal")
        if st.button("⚙️\nSETTINGS\n(Cài Đặt)"): navigate("Settings")
    with col3:
        if st.button("🌌\nSPACE TRASH\n(Dọn Rác)"):
            with st.spinner("Đang dọn dẹp hệ thống..."):
                time.sleep(2)
                st.success("Đã giải phóng 1.2GB bộ nhớ ảo!")
        if st.button("🔒\nLOGOUT"): navigate("Lock")

# --- APP: ECO GARDEN (ỨNG DỤNG TRỒNG CÂY MỚI) ---
elif st.session_state.page == "Garden":
    st.button("🔙 THOÁT RA DESKTOP", on_click=lambda: navigate("Desktop"))
    st.header("🌳 Eco-Garden: Smart Farming")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("### Trạng thái cây")
        st.metric("Sức khỏe", f"{st.session_state.tree_health}%")
        st.metric("Điểm kinh nghiệm (XP)", st.session_state.xp)
        
    with c2:
        tree_type = st.selectbox("Chọn loại cây bạn đang trồng:", ["Cây ăn quả", "Cây cảnh", "Cây lấy bóng mát", "Hoa"])
        action = st.radio("Hành động chăm sóc:", ["Tưới nước", "Bón phân", "Bắt sâu", "Nói chuyện với cây"], horizontal=True)
        
        if st.button("THỰC HIỆN CHĂM SÓC"):
            st.session_state.xp += 10
            st.session_state.tree_health = min(100, st.session_state.tree_health + 5)
            st.success(f"Bạn đã {action} cho {tree_type}. Cây cảm thấy rất hạnh phúc!")
            st.balloons()

    st.divider()
    st.subheader("📸 Nhật ký hình ảnh")
    st.camera_input("Chụp ảnh tiến độ lớn lên của cây")

# --- APP: PARKING PRO (BÃI XE) ---
elif st.session_state.page == "Parking":
    st.button("🔙 BACK", on_click=lambda: navigate("Desktop"))
    st.header("🅿️ QUẢN LÝ BÃI XE CLOUD")
    # Giữ nguyên logic kết nối Sheets của bạn ở đây...
    st.info("Hệ thống bãi xe đang trực tuyến.")
    st.text_input("Tìm kiếm biển số nhanh (USSD Mode)...")

# --- APP: PY-TERMINAL ---
elif st.session_state.page == "Terminal":
    st.button("🔙 BACK", on_click=lambda: navigate("Desktop"))
    st.header("🐍 Python Zenith Terminal")
    code = st.text_area("Coder Mode: Chỉ dùng 1 file duy nhất", value="# Viết code của bạn tại đây\nprint('Zenith OS is amazing')")
    if st.button("RUN CODE"):
        st.code(">>> Đang thực thi...\nKết quả: [Hệ thống giả lập hoàn tất]")

# --- MÀN HÌNH KHÓA ---
elif st.session_state.page == "Lock":
    st.markdown("<h2 style='text-align: center; margin-top:150px;'>Hệ thống đã khóa</h2>", unsafe_allow_html=True)
    if st.button("MỞ KHÓA BẰNG MẬT MÃ"): navigate("Desktop")

# --- APP: SETTINGS (CÀI ĐẶT ẨN) ---
elif st.session_state.page == "Settings":
    st.button("🔙 BACK", on_click=lambda: navigate("Desktop"))
    st.header("⚙️ System Configuration")
    if st.toggle("Kích hoạt giao diện 3D (Experimental)"):
        st.warning("Đang render... vui lòng đợi.")
    
    st.divider()
    st.write("Số hiệu bản dựng: ZEN-999-PRO")
    # Easter Egg: Nhấn vào dòng chữ 7 lần
    if 'dev_count' not in st.session_state: st.session_state.dev_count = 0
    if st.button("Thông tin thiết bị"):
        st.session_state.dev_count += 1
        if st.session_state.dev_count >= 7:
            st.error("⚠️ BẠN ĐÃ MỞ KHÓA QUYỀN TRUY CẬP CORE!")
            st.session_state.dev_count = 0
