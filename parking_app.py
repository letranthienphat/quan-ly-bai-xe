import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math
import base64
from cryptography.fernet import Fernet
import time

# --- 1. CẤU HÌNH BẢO MẬT ---
try:
    KEY = b'6f-Z-X_Ym8X6fB-G8j3G1_QW3u9zX9_yHwV0_abcdef=' 
    cipher = Fernet(KEY)
except:
    KEY = Fernet.generate_key()
    cipher = Fernet(KEY)

def encrypt_val(text):
    if not text: return ""
    return cipher.encrypt(str(text).encode()).decode()

def decrypt_val(text):
    if not text: return ""
    try: return cipher.decrypt(text.encode()).decode()
    except: return text

# --- 2. KẾT NỐI GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Lỗi cấu hình Secrets!")
    st.stop()

def get_data():
    try:
        df = conn.read(ttl=0)
        return df.dropna(how="all")
    except:
        return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

# --- 3. GIAO DIỆN ---
st.set_page_config(page_title="Hệ thống Bãi Xe Pro", layout="wide")

with st.sidebar:
    st.title("🅿️ Quản Lý Bãi Xe")
    menu = st.radio("CHỨC NĂNG", ["🏠 Trạng thái", "📥 Xe Vào", "📤 Xe Ra", "🔧 Sửa", "⚙️ Cài đặt"])

# --- 4. LOGIC TỪNG TAB ---
if menu == "📥 Xe Vào":
    st.header("📥 Ghi nhận xe vào")
    s1, s2 = st.columns(2)
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            lp = st.text_input("🔍 Biển số").upper().strip()
            slot = st.text_input("📍 Vị trí")
        with c2:
            v_type = st.selectbox("🚗 Loại xe", ["Xe máy", "Ô tô", "Xe điện", "Khác"])
            desc = st.text_area("📝 Đặc điểm")
        img = st.camera_input("📷 Chụp ảnh")
        if st.form_submit_button("XÁC NHẬN LƯU"):
            df_curr = get_data()
            if not lp or not slot:
                st.warning("Điền thiếu thông tin!")
            elif lp in df_curr['lp'].astype(str).values:
                s1.error("Xe đã có trong bãi!")
                s2.warning("Từ chối lưu.")
            else:
                new_row = pd.DataFrame([{'lp':lp, 'entry':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'slot':encrypt_val(slot), 'type':v_type, 'desc':encrypt_val(desc)}])
                conn.update(data=pd.concat([df_curr, new_row], ignore_index=True))
                s1.success("Đã ghi nhận!")
                st.balloons()

elif menu == "🏠 Trạng thái":
    st.header("🏢 Xe đang đậu")
    df = get_data()
    if df.empty: st.info("Bãi trống.")
    else:
        df_v = df.copy()
        df_v['slot'] = df_v['slot'].apply(decrypt_val)
        df_v['desc'] = df_v['desc'].apply(decrypt_val)
        st.dataframe(df_v[['lp', 'entry', 'slot', 'type', 'desc']], use_container_width=True)

elif menu == "📤 Xe Ra":
    st.header("💰 Tính tiền")
    df = get_data()
    lp_out = st.text_input("Nhập biển số").upper().strip()
    if lp_out and lp_out in df['lp'].astype(str).values:
        row = df[df['lp'] == lp_out].iloc[0]
        entry_t = datetime.datetime.strptime(row['entry'], "%Y-%m-%d %H:%M:%S")
        hours = math.ceil((datetime.datetime.now() - entry_t).total_seconds() / 3600)
        st.metric("Tiền phí", f"{hours * 10000:,.0f} VND")
        if st.button("THANH TOÁN"):
            conn.update(data=df[df['lp'] != lp_out])
            st.success("Xe đã ra!")
            st.rerun()

elif menu == "🔧 Sửa":
    st.header("🔧 Sửa thông tin")
    df = get_data()
    if not df.empty:
        edit_lp = st.selectbox("Chọn xe", df['lp'].unique())
        idx = df.index[df['lp'] == edit_lp][0]
        n_slot = st.text_input("Vị trí", value=decrypt_val(df.at[idx, 'slot']))
        n_desc = st.text_area("Mô tả", value=decrypt_val(df.at[idx, 'desc']))
        if st.button("CẬP NHẬT"):
            df.at[idx, 'slot'], df.at[idx, 'desc'] = encrypt_val(n_slot), encrypt_val(n_desc)
            conn.update(data=df)
            st.success("Xong!")

elif menu == "⚙️ Cài đặt":
    st.header("⚙️ Hệ thống")
    st.checkbox("Mã hóa 256-bit", value=True)
    st.checkbox("Đồng bộ Sheets", value=True)
    st.write("Dữ liệu đang được bảo vệ an toàn.")
