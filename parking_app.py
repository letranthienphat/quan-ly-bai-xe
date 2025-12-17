import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import math
import time

# --- 1. CẤU HÌNH BẢO MẬT ---
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

# --- 2. HÀM XỬ LÝ DỮ LIỆU ---
def get_cloud_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        
        # Xử lý lỗi "No columns to parse" bằng cách kiểm tra df rỗng
        if df is None or df.empty:
            return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])
            
        return df.dropna(how="all")
    except Exception as e:
        # Trả về DataFrame trống thay vì văng lỗi màn hình đen
        return pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc'])

def save_to_cloud(df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(data=df)
        return True, "Thành công"
    except Exception as e:
        return False, str(e)

# --- 3. GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Hệ thống Bãi Xe Pro", layout="wide")

with st.sidebar:
    st.title("🅿️ QUẢN LÝ BÃI XE")
    menu = st.radio("CHỨC NĂNG:", ["🏠 TRẠNG THÁI", "📥 XE VÀO", "📤 XE RA", "🔧 SỬA XE", "⚙️ CÀI ĐẶT"])
    st.divider()
    st.info("Phiên bản v15.8 (Auto-Fix)")

# --- 4. LOGIC CÁC TAB ---

# --- TAB XE VÀO ---
if menu == "📥 XE VÀO":
    st.header("📥 NHẬP XE MỚI")
    with st.form("form_in", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            lp = st.text_input("Biển số:").upper().strip()
            slot = st.text_input("Vị trí đậu:")
        with col2:
            v_type = st.selectbox("Loại xe:", ["Xe máy", "Ô tô", "Xe điện"])
            desc = st.text_area("Ghi chú:")
        
        if st.form_submit_button("LƯU LÊN CLOUD"):
            if lp and slot:
                df = get_cloud_data()
                new_row = {'lp':lp, 'entry':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                           'slot':encrypt_val(slot), 'type':v_type, 'desc':encrypt_val(desc)}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                success, msg = save_to_cloud(df)
                if success:
                    st.success(f"Đã lưu xe {lp}")
                    st.balloons()
                else: st.error(f"Lỗi lưu Sheets: {msg}")
            else: st.error("Vui lòng nhập đủ Biển số và Vị trí!")

# --- TAB TRẠNG THÁI ---
elif menu == "🏠 TRẠNG THÁI":
    st.header("🏢 DANH SÁCH XE")
    df = get_cloud_data()
    if df.empty:
        st.info("Bãi đang trống hoặc chưa kết nối được dữ liệu.")
    else:
        df_v = df.copy()
        df_v['slot'] = df_v['slot'].apply(decrypt_val)
        st.dataframe(df_v, use_container_width=True)

# --- TAB XE RA ---
elif menu == "📤 XE RA":
    st.header("📤 THANH TOÁN")
    df = get_cloud_data()
    if df.empty: st.info("Bãi trống.")
    else:
        target_lp = st.selectbox("Chọn xe ra:", df['lp'].unique())
        row = df[df['lp'] == target_lp].iloc[0]
        st.write(f"Vào lúc: {row['entry']}")
        if st.button("XÁC NHẬN RA"):
            df = df[df['lp'] != target_lp]
            save_to_cloud(df)
            st.success("Xe đã ra!")
            st.rerun()

# --- TAB SỬA XE ---
elif menu == "🔧 SỬA XE":
    st.header("🔧 CHỈNH SỬA")
    df = get_cloud_data()
    if not df.empty:
        lp_s = st.selectbox("Chọn xe:", df['lp'].unique())
        idx = df.index[df['lp'] == lp_s][0]
        n_slot = st.text_input("Sửa vị trí:", value=decrypt_val(df.at[idx, 'slot']))
        if st.button("CẬP NHẬT"):
            df.at[idx, 'slot'] = encrypt_val(n_slot)
            save_to_cloud(df)
            st.success("Đã sửa!")
            st.rerun()

# --- TAB CÀI ĐẶT (NÂNG CẤP MỚI) ---
elif menu == "⚙️ CÀI ĐẶT":
    st.header("⚙️ CÀI ĐẶT HỆ THỐNG")
    
    st.subheader("🔗 Trạng thái kết nối Sheets")
    df_check = get_cloud_data()
    if not df_check.columns.empty:
        st.success("✅ Kết nối ổn định. Đã tìm thấy các cột: " + ", ".join(df_check.columns))
    else:
        st.error("❌ Lỗi kết nối Sheets: No columns to parse from file")
        st.write("---")
        st.markdown("""
        **Cách sửa lỗi này:**
        1. Mở file Google Sheets của bạn.
        2. Tại **Hàng 1**, hãy gõ thủ công 5 tiêu đề cột: `lp`, `entry`, `slot`, `type`, `desc`.
        3. Đảm bảo file Sheets đã được chia sẻ ở chế độ **"Bất kỳ ai có liên kết đều có thể chỉnh sửa"**.
        4. Sau đó quay lại đây và nhấn nút **Làm mới hệ thống**.
        """)
    
    st.divider()
    st.subheader("🔐 Bảo mật")
    st.write(f"Trạng thái mã hóa Fernet: {'✅ Đang bật' if has_crypto else '❌ Tắt (Thiếu thư viện)'}")
    
    if st.button("🔄 LÀM MỚI HỆ THỐNG"):
        st.rerun()
