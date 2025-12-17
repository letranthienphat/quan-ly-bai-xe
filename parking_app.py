import streamlit as st
import pandas as pd
import datetime
import math

# --- 1. CẤU HÌNH BẢO MẬT (KIỂM TRA THƯ VIỆN) ---
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
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

def get_data():
    try:
        from streamlit_gsheets import GSheetsConnection
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0).dropna(how="all")
        # Đảm bảo các cột quan trọng luôn tồn tại
        for col in ['lp', 'entry', 'slot', 'type', 'desc']:
            if col not in df.columns: df[col] = ""
        return df
    except Exception:
        return st.session_state.db

def update_data(new_df):
    try:
        from streamlit_gsheets import GSheetsConnection
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(data=new_df)
        return True
    except:
        st.session_state.db = new_df
        return False

# --- 3. GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Hệ thống Bãi Xe Pro", layout="wide")

with st.sidebar:
    st.title("🅿️ MENU QUẢN LÝ")
    menu = st.radio("CHỨC NĂNG:", ["📥 XE VÀO", "🏠 TRẠNG THÁI BÃI", "📤 XE RA", "🔧 SỬA XE"])

# --- 4. LOGIC CÁC TAB ---

# --- TAB XE VÀO ---
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
                df_now = get_data()
                if lp in df_now['lp'].astype(str).values:
                    st.error(f"Xe {lp} đã có trong bãi!")
                else:
                    new_row = {'lp': lp, 'entry': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                'slot': encrypt_val(slot), 'type': v_type, 'desc': encrypt_val(desc)}
                    updated_df = pd.concat([df_now, pd.DataFrame([new_row])], ignore_index=True)
                    if update_data(updated_df): st.success("✅ Đã lưu lên Google Sheets!")
                    else: st.warning("⚠️ Đã lưu tạm vào máy.")
                    st.balloons()
            else: st.error("Thiếu thông tin biển số hoặc vị trí!")

# --- TAB TRẠNG THÁI ---
elif menu == "🏠 TRẠNG THÁI BÃI":
    st.header("🏢 DANH SÁCH XE")
    df = get_data()
    if df.empty: st.info("Bãi trống.")
    else:
        df_view = df.copy()
        df_view['slot'] = df_view['slot'].apply(decrypt_val)
        df_view['desc'] = df_view['desc'].apply(decrypt_val)
        st.dataframe(df_view, use_container_width=True)

# --- TAB XE RA (SỬA LỖI MÀN HÌNH ĐEN) ---
elif menu == "📤 XE RA":
    st.header("📤 THANH TOÁN & XE RA")
    df = get_data()
    if df.empty:
        st.info("Bãi đang trống, không có xe để thanh toán.")
    else:
        list_lp = df['lp'].unique().tolist()
        target_lp = st.selectbox("Chọn biển số xe ra:", list_lp)
        
        row = df[df['lp'] == target_lp].iloc[0]
        entry_t = datetime.datetime.strptime(row['entry'], "%Y-%m-%d %H:%M:%S")
        hours = math.ceil((datetime.datetime.now() - entry_t).total_seconds() / 3600)
        st.write(f"⏱️ **Thời gian đã đậu:** {hours} giờ")
        st.metric("TỔNG TIỀN THANH TOÁN", f"{hours * 10000:,.0f} VND")
        
        if st.button("XÁC NHẬN XE RA"):
            new_df = df[df['lp'] != target_lp]
            if update_data(new_df): st.success(f"Xe {target_lp} đã ra khỏi bãi!")
            st.rerun()

# --- TAB SỬA XE (SỬA LỖI MÀN HÌNH ĐEN) ---
elif menu == "🔧 SỬA XE":
    st.header("🔧 CHỈNH SỬA THÔNG TIN")
    df = get_data()
    if df.empty:
        st.info("Bãi đang trống, không có xe để chỉnh sửa.")
    else:
        list_lp = df['lp'].unique().tolist()
        edit_lp = st.selectbox("Chọn biển số cần sửa:", list_lp)
        idx = df.index[df['lp'] == edit_lp][0]
        
        with st.container(border=True):
            new_slot = st.text_input("Vị trí đậu mới:", value=decrypt_val(df.at[idx, 'slot']))
            new_desc = st.text_area("Ghi chú mới:", value=decrypt_val(df.at[idx, 'desc']))
            if st.button("LƯU CẬP NHẬT"):
                df.at[idx, 'slot'] = encrypt_val(new_slot)
                df.at[idx, 'desc'] = encrypt_val(new_desc)
                if update_data(df): st.success("Đã cập nhật dữ liệu thành công!")
                time.sleep(1)
                st.rerun()
