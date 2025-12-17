import streamlit as st
import pandas as pd
import datetime
import math

# --- 1. KIỂM TRA VÀ CẤU HÌNH BẢO MẬT ---
try:
    from cryptography.fernet import Fernet
    KEY = b'6f-Z-X_Ym8X6fB-G8j3G1_QW3u9zX9_yHwV0_abcdef=' 
    cipher = Fernet(KEY)
    has_crypto = True
except ImportError:
    has_crypto = False

def encrypt_val(text):
    if not has_crypto or not text: return str(text)
    return cipher.encrypt(str(text).encode()).decode()

def decrypt_val(text):
    if not has_crypto or not text: return str(text)
    try: return cipher.decrypt(text.encode()).decode()
    except: return text

# --- 2. KẾT NỐI DỮ LIỆU ---
# Khởi tạo db tạm nếu không kết nối được Sheets
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

def get_data():
    try:
        from streamlit_gsheets import GSheetsConnection
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0).dropna(how="all")
        return df
    except Exception:
        return st.session_state.db

# --- 3. GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Parking Pro v15.4", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🅿️ MENU QUẢN LÝ")
    menu = st.radio("CHỨC NĂNG:", ["📥 XE VÀO", "🏠 TRẠNG THÁI BÃI", "📤 XE RA", "🔧 SỬA XE"])
    st.divider()
    if not has_crypto:
        st.warning("⚠️ Đang chạy chế độ không mã hóa (Thiếu thư viện)")

# --- 4. XỬ LÝ CÁC TAB ---
if menu == "📥 XE VÀO":
    st.header("📥 NHẬP XE MỚI")
    with st.form("form_nhap", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            lp = st.text_input("Biển số xe:").upper().strip()
            slot = st.text_input("Vị trí đậu:")
        with c2:
            v_type = st.selectbox("Loại xe:", ["Xe máy", "Ô tô", "Xe điện"])
            desc = st.text_area("Ghi chú:")
        
        if st.form_submit_button("LƯU DỮ LIỆU"):
            if lp and slot:
                new_data = {
                    'lp': lp,
                    'entry': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'slot': encrypt_val(slot),
                    'type': v_type,
                    'desc': encrypt_val(desc)
                }
                # Cập nhật dữ liệu
                df_now = get_data()
                updated_df = pd.concat([df_now, pd.DataFrame([new_data])], ignore_index=True)
                
                try:
                    from streamlit_gsheets import GSheetsConnection
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    conn.update(data=updated_df)
                    st.success("✅ Đã lưu lên Google Sheets!")
                except:
                    st.session_state.db = updated_df
                    st.warning("⚠️ Đã lưu tạm vào máy (Chưa cấu hình Google Sheets)")
                st.balloons()
            else:
                st.error("Thiếu thông tin biển số hoặc vị trí!")

elif menu == "🏠 TRẠNG THÁI BÃI":
    st.header("🏢 DANH SÁCH XE")
    df = get_data()
    if df.empty:
        st.info("Bãi trống.")
    else:
        df_view = df.copy()
        df_view['slot'] = df_view['slot'].apply(decrypt_val)
        df_view['desc'] = df_view['desc'].apply(decrypt_val)
        st.dataframe(df_view, use_container_width=True)
