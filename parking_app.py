import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math
import time

# --- 1. CẤU HÌNH BẢO MẬT & KẾT NỐI ---
# Sử dụng KEY cố định để giải mã dữ liệu cũ trên Sheet
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

# --- 2. HÀM XỬ LÝ DỮ LIỆU CLOUD (VĨNH VIỄN) ---
def get_cloud_data():
    """Lấy dữ liệu trực tiếp từ Google Sheets, không dùng cache"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # ttl=0 để đảm bảo luôn lấy dữ liệu mới nhất nếu có nhiều người cùng dùng
        df = conn.read(ttl=0).dropna(how="all")
        # Kiểm tra cấu trúc cột
        for col in ['lp', 'entry', 'slot', 'type', 'desc']:
            if col not in df.columns: df[col] = ""
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối Sheets: {e}")
        return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

def save_to_cloud(df):
    """Ghi đè toàn bộ DataFrame lên Google Sheets để lưu vĩnh viễn"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(data=df)
        return True
    except Exception as e:
        st.sidebar.error(f"Lỗi lưu dữ liệu: {e}")
        return False

# --- 3. GIAO DIỆN ---
st.set_page_config(page_title="Hệ thống Bãi Xe Cloud", layout="wide")

with st.sidebar:
    st.title("🅿️ QUẢN LÝ CLOUD")
    menu = st.radio("CHỨC NĂNG:", ["📥 XE VÀO", "🏠 TRẠNG THÁI BÃI", "📤 XE RA", "🔧 SỬA XE"])
    st.divider()
    if st.button("🔄 LÀM MỚI (SYNC)"):
        st.rerun()

# --- 4. LOGIC NGHIỆP VỤ ---

if menu == "📥 XE VÀO":
    st.header("📥 NHẬP XE VÀO BÃI")
    with st.form("form_in", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            lp = st.text_input("Biển số xe:").upper().strip()
            slot = st.text_input("Vị trí đậu (Slot):")
        with c2:
            v_type = st.selectbox("Loại xe:", ["Xe máy", "Ô tô", "Xe điện", "Khác"])
            desc = st.text_area("Đặc điểm nhận dạng:")
        
        if st.form_submit_button("XÁC NHẬN LƯU LÊN CLOUD"):
            if lp and slot:
                df = get_cloud_data()
                if lp in df['lp'].astype(str).values:
                    st.error(f"Xe {lp} hiện đang có trong bãi!")
                else:
                    new_row = {
                        'lp': lp, 
                        'entry': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'slot': encrypt_val(slot), 
                        'type': v_type, 
                        'desc': encrypt_val(desc)
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    if save_to_cloud(df):
                        st.success(f"✅ Đã lưu vĩnh viễn xe {lp} vào Google Sheets!")
                        st.balloons()
            else: st.error("Vui lòng nhập đủ Biển số và Vị trí!")

elif menu == "🏠 TRẠNG THÁI BÃI":
    st.header("🏢 DANH SÁCH XE TRÊN CLOUD")
    df = get_cloud_data()
    if df.empty:
        st.info("Hiện tại không có dữ liệu xe trên Cloud.")
    else:
        df_view = df.copy()
        df_view['slot'] = df_view['slot'].apply(decrypt_val)
        df_view['desc'] = df_view['desc'].apply(decrypt_val)
        st.dataframe(df_view, use_container_width=True)
        st.caption("Dữ liệu được cập nhật thời gian thực từ Google Sheets.")

elif menu == "📤 XE RA":
    st.header("📤 THANH TOÁN & XUẤT BÃI")
    df = get_cloud_data()
    if df.empty:
        st.info("Bãi trống.")
    else:
        list_lp = df['lp'].unique().tolist()
        target_lp = st.selectbox("Chọn xe ra:", list_lp)
        
        row = df[df['lp'] == target_lp].iloc[0]
        entry_t = datetime.datetime.strptime(row['entry'], "%Y-%m-%d %H:%M:%S")
        hours = math.ceil((datetime.datetime.now() - entry_t).total_seconds() / 3600)
        
        st.metric("SỐ TIỀN THU (10k/h)", f"{hours * 10000:,.0f} VND")
        
        if st.button("XÁC NHẬN THANH TOÁN & XÓA KHỎI SHEET"):
            df = df[df['lp'] != target_lp]
            if save_to_cloud(df):
                st.success(f"Đã cập nhật Sheets. Xe {target_lp} đã ra!")
                time.sleep(1)
                st.rerun()

elif menu == "🔧 SỬA XE":
    st.header("🔧 CẬP NHẬT THÔNG TIN")
    df = get_cloud_data()
    if not df.empty:
        edit_lp = st.selectbox("Chọn biển số cần sửa:", df['lp'].unique())
        idx = df.index[df['lp'] == edit_lp][0]
        with st.container(border=True):
            new_slot = st.text_input("Sửa vị trí đậu:", value=decrypt_val(df.at[idx, 'slot']))
            if st.button("LƯU THAY ĐỔI VĨNH VIỄN"):
                df.at[idx, 'slot'] = encrypt_val(new_slot)
                if save_to_cloud(df):
                    st.success("Đã cập nhật dữ liệu mới lên Cloud!")
                    st.rerun()
