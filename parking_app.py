import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math
import time
import random

# --- 1. BẢO MẬT ---
try:
    from cryptography.fernet import Fernet
    KEY = b'6f-Z-X_Ym8X6fB-G8j3G1_QW3u9zX9_yHwV0_abcdef=' 
    cipher = Fernet(KEY)
    has_crypto = True
except:
    has_crypto = False

def encrypt_val(text):
    if not has_crypto or not text: return str(text)
    return cipher.encrypt(str(text).encode()).decode()

def decrypt_val(text):
    if not has_crypto or not text: return str(text)
    try: return cipher.decrypt(text.encode()).decode()
    except: return text

# --- 2. HÀM DỮ LIỆU ---
def get_cloud_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        return df.dropna(how="all") if df is not None else pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])
    except:
        return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

def save_to_cloud(df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(data=df)
        return True
    except: return False

# --- 3. CẤU HÌNH GIAO DIỆN & SESSION STATE (QUAN TRỌNG CHO TÍNH NĂNG ẨN) ---
st.set_page_config(page_title="Android Parking OS", layout="wide", page_icon="🤖")

if 'ver_clicks' not in st.session_state: st.session_state.ver_clicks = 0
if 'dev_mode' not in st.session_state: st.session_state.dev_mode = False
if 'dev_clicks' not in st.session_state: st.session_state.dev_clicks = 0

# --- 4. SIDEBAR PHONG CÁCH ANDROID ---
with st.sidebar:
    st.title("🤖 Android Parking OS")
    menu = st.radio("ỨNG DỤNG", ["🏠 Trang chính", "📥 Vào bãi", "📤 Thanh toán", "⚙️ Hệ thống"])
    
    st.divider()
    # Easter Egg 1: Nhấn nhiều lần vào phiên bản
    if st.button(f"Phiên bản: 16.0.2-release"):
        st.session_state.ver_clicks += 1
        if st.session_state.ver_clicks >= 5:
            st.balloons()
            st.info("🎯 Bạn đã tìm thấy logo Android Parking ẩn!")
            st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
            st.session_state.ver_clicks = 0

# --- 5. LOGIC CHI TIẾT ---

if menu == "🏠 Trang chính":
    st.header("🏢 Trạng thái bãi xe")
    df = get_cloud_data()
    if df.empty: st.info("Bãi xe đang trống.")
    else:
        df_v = df.copy()
        df_v['slot'] = df_v['slot'].apply(decrypt_val)
        st.dataframe(df_v, use_container_width=True)

elif menu == "📥 Vào bãi":
    st.header("📥 Ghi nhận xe")
    # Easter Egg 2: Mã USSD bí mật trong ô Biển số
    lp = st.text_input("Nhập biển số:").upper().strip()
    
    if lp == "*#06#":
        st.code("IMEI Hệ thống: 357892100456XXX\nTrạng thái: Đang hoạt động")
    elif lp == "*#99#":
        st.warning("🚀 Đang kích hoạt chế độ tăng tốc phần cứng...")
        time.sleep(1)
        st.success("Đã tối ưu hóa bộ nhớ đệm!")
    
    with st.form("entry"):
        slot = st.text_input("Vị trí:")
        v_type = st.selectbox("Loại xe", ["Ô tô", "Xe máy", "Xe điện"])
        if st.form_submit_button("XÁC NHẬN"):
            df = get_cloud_data()
            new = {'lp':lp, 'entry':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'slot':encrypt_val(slot), 'type':v_type, 'desc':""}
            save_to_cloud(pd.concat([df, pd.DataFrame([new])], ignore_index=True))
            st.success("Đã ghi vào bộ nhớ hệ thống.")

elif menu == "📤 Thanh toán":
    st.header("📤 Xuất bãi")
    df = get_cloud_data()
    if not df.empty:
        target = st.selectbox("Chọn xe:", df['lp'].unique())
        if st.button("THANH TOÁN & MỞ CỔNG"):
            save_to_cloud(df[df['lp'] != target])
            st.snow()
            st.rerun()

# --- TAB HỆ THỐNG: NƠI KÍCH HOẠT NHÀ PHÁT TRIỂN ---
elif menu == "⚙️ Hệ thống":
    st.header("⚙️ Thông tin thiết bị")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Tên thiết bị:** Parking Cloud Server")
        st.write("**Bộ vi xử lý:** Streamlit Virtual CPU")
        
        # Easter Egg 3: Nhấn 7 lần để làm Nhà phát triển
        build_text = "Số hiệu bản dựng: PK-2025-V16"
        if st.button(build_text):
            st.session_state.dev_clicks += 1
            remaining = 7 - st.session_state.dev_clicks
            if remaining > 0 and remaining < 4:
                st.toast(f"Bạn còn cách chế độ Nhà phát triển {remaining} bước nữa.")
            elif remaining <= 0:
                if not st.session_state.dev_mode:
                    st.session_state.dev_mode = True
                    st.toast("🎯 BẠN ĐÃ TRỞ THÀNH NHÀ PHÁT TRIỂN!")
                    st.balloons()

    # HIỆN MENU ẨN KHI ĐÃ LÀ NHÀ PHÁT TRIỂN
    if st.session_state.dev_mode:
        st.divider()
        st.subheader("🛠 TÙY CHỌN NHÀ PHÁT TRIỂN (DEVELOPER OPTIONS)")
        
        with st.expander("Các tính năng nâng cao đã mở khóa"):
            # Tính năng 1: Ép buộc Render CSS (Giao diện ma trận)
            if st.checkbox("Bật gỡ lỗi bố cục (Matrix Mode)"):
                st.markdown("""<style> * { color: #00FF00 !important; background-color: black !important; border: 1px solid #00FF00 !important; } </style>""", unsafe_allow_html=True)
            
            # Tính năng 2: Xem Logs hệ thống thời gian thực (Giả lập)
            if st.button("Xem nhật ký hạt nhân (Kernel Logs)"):
                logs = [f"[INFO] {datetime.datetime.now()} - Cloud Sync thành công",
                        "[DEBUG] Fernet Encryption active",
                        "[SYSTEM] Bãi xe đang hoạt động ổn định"]
                for log in logs: st.text(log)
            
            # Tính năng 3: Tải file cấu hình JSON
            st.download_button("Xuất cấu hình hệ thống (.json)", 
                               data=get_cloud_data().to_json(),
                               file_name="system_config.json")
            
            # Tính năng 4: Tắt chế độ nhà phát triển
            if st.button("Tắt chế độ Nhà phát triển"):
                st.session_state.dev_mode = False
                st.session_state.dev_clicks = 0
                st.rerun()

    st.write("---")
    st.write("Dữ liệu được lưu vĩnh viễn trên Google Sheets.")
