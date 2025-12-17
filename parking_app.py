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
        if df is None or df.empty:
            return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])
        return df.dropna(how="all")
    except:
        return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

def save_to_cloud(df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(data=df)
        return True
    except: return False

# --- 3. GIAO DIỆN ---
st.set_page_config(page_title="AI Parking Cloud Pro", layout="wide", page_icon="🚀")

# Khởi tạo trạng thái ẩn
if 'boss_mode' not in st.session_state: st.session_state.boss_mode = False

with st.sidebar:
    st.title("🅿️ HỆ THỐNG BÃI XE")
    menu = st.radio("CHỨC NĂNG:", ["🏠 TRẠNG THÁI", "📥 XE VÀO", "📤 XE RA", "🔧 SỬA XE", "⚙️ CÀI ĐẶT"])
    
    # Một "Easter Egg" nhỏ ở Sidebar: Nếu nhấn vào đây 5 lần sẽ hiện thông báo bí mật
    if st.button("🚀 Phiên bản 15.9"):
        st.toast("Bạn đang sử dụng bản đặc biệt dành cho Boss!")

# --- 4. LOGIC CÁC TAB ---

if menu == "📥 XE VÀO":
    st.header("📥 NHẬP XE")
    with st.form("form_in", clear_on_submit=True):
        c1, c2 = st.columns(2)
        lp = c1.text_input("Biển số:").upper().strip()
        slot = c1.text_input("Vị trí:")
        v_type = c2.selectbox("Loại xe:", ["Xe máy", "Ô tô", "Xe điện"])
        desc = c2.text_area("Ghi chú:")
        if st.form_submit_button("LƯU"):
            df = get_cloud_data()
            new = {'lp':lp, 'entry':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                   'slot':encrypt_val(slot), 'type':v_type, 'desc':encrypt_val(desc)}
            if save_to_cloud(pd.concat([df, pd.DataFrame([new])], ignore_index=True)):
                st.success("Đã lưu vĩnh viễn!")
                st.balloons()

elif menu == "🏠 TRẠNG THÁI":
    st.header("🏢 DANH SÁCH")
    df = get_cloud_data()
    if df.empty: st.info("Bãi trống.")
    else:
        df_v = df.copy()
        df_v['slot'] = df_v['slot'].apply(decrypt_val)
        st.dataframe(df_v, use_container_width=True)

elif menu == "📤 XE RA":
    st.header("📤 THANH TOÁN")
    df = get_cloud_data()
    if not df.empty:
        target = st.selectbox("Chọn xe:", df['lp'].unique())
        if st.button("XÁC NHẬN RA"):
            save_to_cloud(df[df['lp'] != target])
            st.snow() # Hiệu ứng tuyết rơi cho khác biệt
            st.rerun()

elif menu == "🔧 SỬA XE":
    st.header("🔧 CHỈNH SỬA")
    df = get_cloud_data()
    if not df.empty:
        lp_s = st.selectbox("Chọn xe:", df['lp'].unique())
        idx = df.index[df['lp'] == lp_s][0]
        n_slot = st.text_input("Vị trí mới", value=decrypt_val(df.at[idx, 'slot']))
        if st.button("CẬP NHẬT"):
            df.at[idx, 'slot'] = encrypt_val(n_slot)
            save_to_cloud(df)
            st.success("Xong!")

# --- TAB CÀI ĐẶT: NƠI CHỨA CÁC TÍNH NĂNG ẨN ---
elif menu == "⚙️ CÀI ĐẶT":
    st.header("⚙️ CÀI ĐẶT & TÍNH NĂNG BÍ MẬT")
    
    # Tính năng 1: Chế độ Boss (Phải nhập mã mới hiện)
    st.subheader("🔓 Kích hoạt quyền hạn")
    secret_code = st.text_input("Nhập mã bí mật để mở khóa tính năng ẩn:", type="password")
    
    if secret_code == "6666": # Đây là mã bí mật của bạn
        st.session_state.boss_mode = True
        st.success("🎯 CHẾ ĐỘ BOSS ĐÃ BẬT!")
    
    if st.session_state.boss_mode:
        st.divider()
        st.subheader("🔥 CÁC TÍNH NĂNG SIÊU CẤP")
        
        col_a, col_b = st.columns(2)
        with col_a:
            # Tính năng ẩn 1: Dự báo doanh thu bằng AI (Giả lập)
            if st.button("📊 Dự báo doanh thu ngày mai"):
                prediction = random.randint(500, 2000) * 1000
                st.info(f"AI dự đoán doanh thu ngày mai: {prediction:,.0f} VND")
            
            # Tính năng ẩn 2: Xóa sạch bãi xe (Dành cho tình huống khẩn cấp)
            if st.button("⚠️ RESET TOÀN BỘ BÃI XE"):
                if save_to_cloud(pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])):
                    st.warning("Đã xóa sạch dữ liệu trên Cloud!")
        
        with col_b:
            # Tính năng ẩn 3: Chế độ "Dark Web" (Đổi màu giao diện qua CSS)
            if st.toggle("🌙 Chế độ ban đêm siêu cấp"):
                st.markdown("""<style>div.stApp { background-color: #1e1e1e; color: #00ff00; }</style>""", unsafe_allow_html=True)
                st.write("Hệ thống đã chuyển sang chế độ bảo mật cao.")
            
            # Tính năng ẩn 4: Tải báo cáo nhanh
            st.download_button("📥 Tải Database dự phòng (.csv)", 
                               data=get_cloud_data().to_csv().encode('utf-8'),
                               file_name="backup_parking.csv")

    st.divider()
    st.subheader("📡 Trạng thái hệ thống")
    if st.button("🔍 Kiểm tra kết nối Sheets"):
        df_check = get_cloud_data()
        st.write(f"Tìm thấy: {len(df_check)} xe đang đậu.")
        st.write(f"Cấu trúc cột: {list(df_check.columns)}")
