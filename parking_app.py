import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math
import time
import random

# --- 1. CORE SYSTEM & SECURITY ---
try:
    from cryptography.fernet import Fernet
    KEY = b'6f-Z-X_Ym8X6fB-G8j3G1_QW3u9zX9_yHwV0_abcdef=' 
    cipher = Fernet(KEY)
    has_crypto = True
except:
    has_crypto = False

def decrypt_val(text):
    if not has_crypto or not text: return str(text)
    try: return cipher.decrypt(text.encode()).decode()
    except: return text

# --- 2. OS STATE MANAGEMENT ---
if 'current_app' not in st.session_state: st.session_state.current_app = "Desktop"
if 'dev_unlocked' not in st.session_state: st.session_state.dev_unlocked = False
if 'matrix_mode' not in st.session_state: st.session_state.matrix_mode = False

def open_app(app_name):
    st.session_state.current_app = app_name

# --- 3. DATA ENGINE ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        return df.dropna(how="all") if df is not None else pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])
    except:
        return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

# --- 4. NEBULA DARK UI DESIGN (KHẮC PHỤC MẤT CHỮ) ---
st.set_page_config(page_title="Nebula OS Pro", layout="wide", page_icon="🌌")

st.markdown("""
<style>
    /* Nền tối sâu và chữ Neon */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
    }
    /* Tùy chỉnh nút bấm kiểu Glassmorphism */
    .stButton>button {
        background: rgba(255, 255, 255, 0.05);
        color: #00d4ff;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        height: 120px;
        backdrop-filter: blur(10px);
        transition: 0.4s;
        font-size: 18px;
    }
    .stButton>button:hover {
        background: rgba(0, 212, 255, 0.2);
        color: #ffffff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
        transform: translateY(-5px);
    }
    /* Thanh Taskbar phía dưới */
    .taskbar {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(0, 0, 0, 0.8);
        padding: 10px;
        text-align: center;
        border-top: 1px solid #00d4ff;
        font-family: 'Courier New', Courier, monospace;
        color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. LOGIC MÀN HÌNH ---

# MÀN HÌNH CHÍNH (DESKTOP)
if st.session_state.current_app == "Desktop":
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🌌 NEBULA OS</h1>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center;'>Hệ thống đang chạy tốt | {datetime.datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
    
    # Easter Egg: Một ô nhập lệnh bí mật ngay màn hình chính
    cmd = st.text_input("Terminal Command:", placeholder="Nhập lệnh hoặc quét vân tay...").strip()
    if cmd == "root.unlock":
        st.session_state.dev_unlocked = True
        st.toast("🔓 QUYỀN TRUY CẬP TỐI CAO ĐÃ MỞ!")
    elif cmd == "matrix.exe":
        st.session_state.matrix_mode = not st.session_state.matrix_mode
        st.rerun()

    if st.session_state.matrix_mode:
        st.markdown("<style> * { color: #00ff00 !important; font-family: 'Courier New' !important; } </style>", unsafe_allow_html=True)

    st.write("###")
    # Icon Grid 4 cột cho xịn
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📥\nINBOUND\n(Vào Bãi)"): open_app("In")
    with c2:
        if st.button("🏢\nSTORAGE\n(Bãi Xe)"): open_app("Status")
    with c3:
        if st.button("📤\nOUTBOUND\n(Xe Ra)"): open_app("Out")
    with c4:
        if st.button("⚙️\nSYSTEM\n(Cài Đặt)"): open_app("Settings")

# --- APP: NHẬP XE (INBOUND) ---
elif st.session_state.current_app == "In":
    if st.button("🔙 HOME"): open_app("Desktop")
    st.header("📥 Ghi nhận dữ liệu mới")
    with st.container(border=True):
        lp = st.text_input("BIỂN SỐ XE").upper()
        slot = st.text_input("VỊ TRÍ")
        if st.button("GHI VÀO CLOUD"):
            st.success(f"Đã nạp {lp} vào hệ thống!")
            st.balloons()

# --- APP: TRẠNG THÁI (STORAGE) ---
elif st.session_state.current_app == "Status":
    if st.button("🔙 HOME"): open_app("Desktop")
    st.header("🏢 Cơ sở dữ liệu hiện tại")
    df = get_data()
    st.table(df) # Dùng table cho rõ chữ trong Dark Mode

# --- APP: THANH TOÁN (OUTBOUND) ---
elif st.session_state.current_app == "Out":
    if st.button("🔙 HOME"): open_app("Desktop")
    st.header("📤 Giải phóng bộ nhớ & Xuất bãi")
    df = get_data()
    if not df.empty:
        target = st.selectbox("Chọn xe:", df['lp'].unique())
        if st.button("THANH TOÁN"):
            st.snow()
            st.success("Giao dịch hoàn tất!")

# --- APP: CÀI ĐẶT (SYSTEM) ---
elif st.session_state.current_app == "Settings":
    if st.button("🔙 HOME"): open_app("Desktop")
    st.header("⚙️ Control Panel")
    
    # Tính năng ẩn cực nhiều ở đây
    st.subheader("🛠 Developer Tools")
    if not st.session_state.dev_unlocked:
        st.write("Quyền hạn: Guest")
    else:
        st.write("Quyền hạn: **SUPER USER (BOSS)**")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button("☢️ Reset Database"): st.warning("Đã gửi lệnh xóa!")
            if st.button("📡 Sync Force"): st.info("Đang ép xung đồng bộ...")
        with col_y:
            st.color_picker("Thay đổi màu chủ đạo OS", "#00d4ff")
            st.write("Tốc độ CPU: 4.2GHz (Overclocked)")

    st.divider()
    # Nhấn vào đây 10 lần sẽ hiện tin nhắn ẩn (giống Android)
    if 'info_clicks' not in st.session_state: st.session_state.info_clicks = 0
    if st.button(f"Thông tin Kernel: v18.0.0-PRO"):
        st.session_state.info_clicks += 1
        if st.session_state.info_clicks >= 7:
            st.error("💀 BẠN ĐANG ĐI QUÁ SÂU VÀO HỆ THỐNG!")
            st.info("Hãy thử nhập lệnh 'root.unlock' ở màn hình chính.")

# --- FOOTER ---
st.markdown(f"""
    <div class="taskbar">
        CORE-ID: {random.randint(1000,9999)} | 🟢 CLOUD ACTIVE | MEMORY: {random.randint(40,60)}% | 📍 VIETNAM
    </div>
""", unsafe_allow_html=True)
