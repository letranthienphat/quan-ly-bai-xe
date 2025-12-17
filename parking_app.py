import streamlit as st
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

# --- 2. KẾT NỐI DỮ LIỆU ---
def get_data():
    try:
        from streamlit_gsheets import GSheetsConnection
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0).dropna(how="all")
        return df
    except:
        return st.session_state.get('db', pd.DataFrame(columns=['lp', 'entry', 'slot', 'type', 'desc']))

def update_data(new_df):
    try:
        from streamlit_gsheets import GSheetsConnection
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(data=new_df)
        return True
    except:
        st.session_state.db = new_df
        return False

# --- 3. GIAO DIỆN ---
st.set_page_config(page_title="Parking Pro v15.6", layout="wide")

with st.sidebar:
    st.title("🅿️ Quản Lý Bãi Xe")
    menu = st.radio("CHỨC NĂNG:", ["📥 XE VÀO", "🏠 TRẠNG THÁI BÃI", "📤 XE RA", "🔧 SỬA XE", "⚙️ CÀI ĐẶT"])
    st.divider()
    fee_rate = st.number_input("Giá vé gốc (VND/h)", value=10000, step=1000)

# --- 4. LOGIC TAB XE RA (NÂNG CẤP CHẾ ĐỘ THANH TOÁN) ---
if menu == "📤 XE RA":
    st.header("📤 THANH TOÁN & XUẤT BÃI")
    df = get_data()
    
    if df.empty:
        st.info("Bãi đang trống.")
    else:
        list_lp = df['lp'].unique().tolist()
        target_lp = st.selectbox("Chọn biển số xe ra:", list_lp)
        
        # Lấy thông tin xe
        row = df[df['lp'] == target_lp].iloc[0]
        entry_t = datetime.datetime.strptime(row['entry'], "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        duration = now - entry_t
        hours = math.ceil(duration.total_seconds() / 3600)
        
        st.info(f"🚩 Xe vào lúc: {row['entry']} | Thời gian đậu: {hours} giờ")

        # --- TÍNH NĂNG CHỌN CHẾ ĐỘ THANH TOÁN ---
        st.subheader("💳 Hình thức thanh toán")
        mode = st.radio("Chọn chế độ:", 
                        ["Tự động (Theo giờ)", "Bán tự động (Nhập số tiền)", "Thủ công (Tùy chỉnh)"], 
                        horizontal=True)
        
        final_fee = 0
        
        if mode == "Tự động (Theo giờ)":
            final_fee = hours * fee_rate
            st.metric("SỐ TIỀN CẦN THU", f"{final_fee:,.0f} VND")
            st.caption(f"Công thức: {hours}h x {fee_rate:,.0f} VND")
            
        elif mode == "Bán tự động (Nhập số tiền)":
            suggested = hours * fee_rate
            final_fee = st.number_input(f"Nhập số tiền thu (Gợi ý: {suggested:,.0f})", value=int(suggested), step=1000)
            st.metric("SỐ TIỀN THU THỰC TẾ", f"{final_fee:,.0f} VND")
            
        elif mode == "Thủ công (Tùy chỉnh)":
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                final_fee = st.number_input("Số tiền thu (VND)", value=0, step=5000)
            with col_m2:
                reason = st.text_input("Lý do miễn phí/giảm giá", "Khách VIP / Ghi nợ")
            st.warning(f"Chế độ thủ công: {reason}")

        st.divider()
        if st.button("XÁC NHẬN THANH TOÁN & MỞ CỔNG", use_container_width=True):
            with st.spinner("Đang xử lý giao dịch..."):
                new_df = df[df['lp'] != target_lp]
                if update_data(new_df):
                    st.success(f"Giao dịch thành công! Số tiền: {final_fee:,.0f} VND. Mời xe {target_lp} ra bãi.")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()

# --- CÁC TAB KHÁC GIỮ NGUYÊN NHƯ V15.5 ---
elif menu == "📥 XE VÀO":
    st.header("📥 NHẬP XE MỚI")
    with st.form("form_in", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            lp = st.text_input("Biển số:").upper().strip()
            slot = st.text_input("Vị trí:")
        with c2:
            v_type = st.selectbox("Loại xe:", ["Xe máy", "Ô tô", "Xe điện"])
            desc = st.text_area("Ghi chú:")
        if st.form_submit_button("LƯU"):
            df_n = get_data()
            if lp and slot:
                new_r = {'lp':lp, 'entry':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'slot':encrypt_val(slot), 'type':v_type, 'desc':encrypt_val(desc)}
                if update_data(pd.concat([df_n, pd.DataFrame([new_r])], ignore_index=True)):
                    st.success("Đã lưu!")
                    st.balloons()
            else: st.error("Thiếu thông tin!")

elif menu == "🏠 TRẠNG THÁI BÃI":
    st.header("🏢 DANH SÁCH XE")
    df = get_data()
    if df.empty: st.info("Bãi trống.")
    else:
        df_v = df.copy()
        df_v['slot'] = df_v['slot'].apply(decrypt_val)
        df_view = df_v[['lp', 'entry', 'slot', 'type']]
        st.dataframe(df_view, use_container_width=True)

elif menu == "🔧 SỬA XE":
    st.header("🔧 SỬA THÔNG TIN")
    df = get_data()
    if not df.empty:
        lp_s = st.selectbox("Chọn xe:", df['lp'].unique())
        idx = df.index[df['lp'] == lp_s][0]
        n_slot = st.text_input("Vị trí mới", value=decrypt_val(df.at[idx, 'slot']))
        if st.button("CẬP NHẬT"):
            df.at[idx, 'slot'] = encrypt_val(n_slot)
            update_data(df)
            st.success("Xong!")
            st.rerun()

elif menu == "⚙️ CÀI ĐẶT":
    st.header("⚙️ CẤU HÌNH HỆ THỐNG")
    st.write("Phiên bản: 15.6 - Payment Pro")
    st.checkbox("Tự động tính tiền", value=True)
    st.checkbox("Mã hóa dữ liệu", value=has_crypto)
