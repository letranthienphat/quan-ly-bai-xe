import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math
import time

# --- 1. CẤU HÌNH HỆ THỐNG & BẢO MẬT ---
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

# --- 2. QUẢN LÝ TRẠNG THÁI MÀN HÌNH (OS LOGIC) ---
if 'current_app' not in st.session_state:
    st.session_state.current_app = "Desktop"

def open_app(app_name):
    st.session_state.current_app = app_name

# --- 3. KẾT NỐI DỮ LIỆU ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        return df.dropna(how="all") if df is not None else pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])
    except:
        return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

# --- 4. GIAO DIỆN PHONG CÁCH OS ---
st.set_page_config(page_title="Parking OS Pro", layout="wide", page_icon="💻")

# CSS tùy chỉnh để làm icon và hiệu ứng Desktop
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 15px; height: 100px; font-size: 20px; font-weight: bold; background-color: #f0f2f6; border: 2px solid #d1d5db; transition: 0.3s; }
    .stButton>button:hover { background-color: #3b82f6; color: white; transform: scale(1.05); }
    .desktop-icon { font-size: 40px; margin-bottom: 10px; }
    .taskbar { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); padding: 10px; text-align: center; border-top: 1px solid #ddd; z-index: 1000; }
</style>
""", unsafe_allow_html=True)

# --- MÀN HÌNH CHÍNH (DESKTOP) ---
if st.session_state.current_app == "Desktop":
    st.title("💻 Welcome to Parking OS")
    st.write(f"🕒 {datetime.datetime.now().strftime('%H:%M - %d/%m/%Y')}")
    st.write("---")
    
    # Tạo lưới Icon 3x2
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥\nNhập Xe Vào"): open_app("Check-in")
        if st.button("🔧\nCấu Hình"): open_app("Settings")
        
    with col2:
        if st.button("🏢\nBãi Xe"): open_app("Status")
        if st.button("📊\nThống Kê"): st.toast("Tính năng đang phát triển!")
        
    with col3:
        if st.button("📤\nThanh Toán"): open_app("Check-out")
        if st.button("🔐\nĐăng Xuất"): st.warning("Vui lòng đóng trình duyệt để đăng xuất.")

# --- APP: NHẬP XE ---
elif st.session_state.current_app == "Check-in":
    st.button("⬅️ Quay lại", on_click=lambda: open_app("Desktop"))
    st.header("📥 Ứng dụng: Nhập Xe Vào")
    # ... (Giữ logic nhập xe của bạn ở đây)
    st.info("Giao diện nhập xe chuyên nghiệp.")
    lp = st.text_input("Biển số:").upper()
    if st.button("LƯU DỮ LIỆU"):
        st.success(f"Đã ghi nhận xe {lp}")

# --- APP: TRẠNG THÁI BÃI ---
elif st.session_state.current_app == "Status":
    st.button("⬅️ Quay lại", on_click=lambda: open_app("Desktop"))
    st.header("🏢 Ứng dụng: Trạng Thái Bãi")
    df = get_data()
    st.dataframe(df, use_container_width=True)

# --- APP: THANH TOÁN ---
elif st.session_state.current_app == "Check-out":
    st.button("⬅️ Quay lại", on_click=lambda: open_app("Desktop"))
    st.header("📤 Ứng dụng: Thanh Toán")
    st.write("Chọn xe cần thanh toán...")

# --- APP: CÀI ĐẶT ---
elif st.session_state.current_app == "Settings":
    st.button("⬅️ Quay lại", on_click=lambda: open_app("Desktop"))
    st.header("⚙️ Hệ Thống & Tùy Chọn")
    st.write("Số hiệu bản dựng: PK-2025-V17")
    if st.checkbox("Chế độ nhà phát triển"):
        st.success("Đã kích hoạt quyền Root!")

# --- TASKBAR CỐ ĐỊNH PHÍA DƯỚI ---
st.markdown(f"""
    <div class="taskbar">
        <b>Parking OS v17.0</b> | Trạng thái: Online | Pin: 99% 🔋
    </div>
""", unsafe_allow_html=True)
