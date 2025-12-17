import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math
from cryptography.fernet import Fernet

# --- 1. KHỞI TẠO BẢO MẬT ---
KEY = b'6f-Z-X_Ym8X6fB-G8j3G1_QW3u9zX9_yHwV0_abcdef=' 
cipher = Fernet(KEY)

def encrypt_val(text):
    return cipher.encrypt(str(text).encode()).decode() if text else ""

def decrypt_val(text):
    try: return cipher.decrypt(text.encode()).decode() if text else ""
    except: return text

# --- 2. KẾT NỐI DỮ LIỆU (CÓ CHẾ ĐỘ DỰ PHÒNG) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0).dropna(how="all")
        return df
    except:
        # Nếu lỗi kết nối Sheets, dùng dữ liệu tạm trong phiên làm việc
        return st.session_state.db

# --- 3. GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Parking Pro", layout="wide")

# Sidebar menu luôn phải hiện diện
with st.sidebar:
    st.title("🅿️ MENU QUẢN LÝ")
    menu = st.radio("CHỌN CHỨC NĂNG:", ["📥 XE VÀO", "🏠 TRẠNG THÁI BÃI", "📤 XE RA", "🔧 SỬA XE"])

# --- 4. CÁC Ô NHẬP LIỆU (LUÔN HIỆN) ---
if menu == "📥 XE VÀO":
    st.header("📥 NHẬP XE MỚI")
    
    # Dùng form để đảm bảo các ô nhập liệu luôn hiện ra
    with st.form("form_nhap", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            lp_input = st.text_input("Biển số xe:").upper()
            slot_input = st.text_input("Vị trí đậu:")
        with c2:
            type_input = st.selectbox("Loại xe:", ["Xe máy", "Ô tô", "Xe điện"])
            desc_input = st.text_area("Ghi chú:")
        
        submitted = st.form_submit_button("LƯU DỮ LIỆU")
        
        if submitted:
            if lp_input and slot_input:
                new_data = {
                    'lp': lp_input,
                    'entry': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'slot': encrypt_val(slot_input),
                    'type': type_input,
                    'desc': encrypt_val(desc_input)
                }
                # Lưu vào bộ nhớ tạm trước
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
                
                # Thử đẩy lên Google Sheets
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    conn.update(data=st.session_state.db)
                    st.success("✅ Đã lưu lên Google Sheets!")
                except:
                    st.warning("⚠️ Đã lưu tạm (Lỗi kết nối Google Sheets)")
            else:
                st.error("Vui lòng điền Biển số và Vị trí!")

elif menu == "🏠 TRẠNG THÁI BÃI":
    st.header("🏢 DANH SÁCH XE ĐANG ĐẬU")
    df = get_data()
    if df.empty:
        st.info("Hiện tại bãi đang trống. Hãy qua mục 'XE VÀO' để nhập xe.")
    else:
        df_view = df.copy()
        df_view['slot'] = df_view['slot'].apply(decrypt_val)
        df_view['desc'] = df_view['desc'].apply(decrypt_val)
        st.table(df_view)
