import streamlit as st
import sqlite3
import pandas as pd
import datetime
import math
import os

# --- CẤU HÌNH ---
DB_NAME = 'parking_cloud.db'
FEE_PER_HOUR = 10000
IMG_DIR = "captured_images"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS parked (
                    lp TEXT PRIMARY KEY, entry_time TEXT, slot TEXT, 
                    type TEXT, desc TEXT, img_path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, lp TEXT, 
                    entry TEXT, exit TEXT, fee REAL, type TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- UI ---
st.set_page_config(page_title="Hệ thống Bãi Xe v11", layout="wide", page_icon="🅿️")

# CSS để giao diện trông hiện đại hơn
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🅿️ Quản Lý Bãi Xe Thông Minh (Cloud Version)")

tabs = st.tabs(["🏠 Trạng thái bãi", "📥 Xe Vào", "📤 Xe Ra", "📊 Thống kê"])

# --- TAB 1: TRẠNG THÁI ---
with tabs[0]:
    st.subheader("📋 Danh sách xe đang đậu")
    df = pd.read_sql_query("SELECT lp, entry_time, slot, type, desc FROM parked", conn)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        col_view1, col_view2 = st.columns([1, 2])
        with col_view1:
            selected_lp = st.selectbox("Chọn xe để xem ảnh chi tiết", df['lp'].tolist())
        with col_view2:
            c = conn.cursor()
            c.execute("SELECT img_path FROM parked WHERE lp=?", (selected_lp,))
            img_p = c.fetchone()[0]
            if img_p and os.path.exists(img_p):
                st.image(img_p, caption=f"Ảnh bằng chứng xe {selected_lp}", width=500)
            else:
                st.info("Xe này không có ảnh đính kèm.")
    else:
        st.info("Hiện không có xe nào trong bãi.")

# --- TAB 2: XE VÀO (TÍCH HỢP CAMERA) ---
with tabs[1]:
    st.subheader("📝 Đăng ký xe mới")
    with st.form("entry_form"):
        c1, c2 = st.columns(2)
        with c1:
            lp = st.text_input("Biển số xe").upper()
            slot = st.text_input("Vị trí (Slot)")
            v_type = st.selectbox("Loại xe", ["Ô tô", "Xe máy", "Xe đạp", "Khác"])
        with c2:
            desc = st.text_area("Mô tả thêm")
        
        st.write("📸 **Hình ảnh xe**")
        source = st.radio("Nguồn ảnh:", ["Dùng Camera", "Tải file từ máy"])
        
        img_file = None
        if source == "Dùng Camera":
            img_file = st.camera_input("Chụp ảnh biển số")
        else:
            img_file = st.file_uploader("Chọn ảnh từ thiết bị", type=['jpg', 'png', 'jpeg'])
            
        submit = st.form_submit_button("XÁC NHẬN CHO XE VÀO")
        
        if submit:
            if not lp or not slot:
                st.error("Vui lòng điền đủ Biển số và Vị trí!")
            else:
                img_path = ""
                if img_file:
                    img_path = f"{IMG_DIR}/{lp}_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
                    with open(img_path, "wb") as f:
                        f.write(img_file.getbuffer())
                
                try:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    conn.execute("INSERT INTO parked VALUES (?,?,?,?,?,?)", (lp, now, slot, v_type, desc, img_path))
                    conn.commit()
                    st.success(f"✅ Đã ghi nhận xe {lp} vào bãi!")
                    st.rerun()
                except:
                    st.error("Lỗi: Biển số này đã tồn tại trong bãi!")

# --- TAB 3: XE RA ---
with tabs[2]:
    st.subheader("💰 Thanh toán")
    lp_out = st.text_input("Nhập biển số xe cần ra").upper()
    if lp_out:
        c = conn.cursor()
        c.execute("SELECT * FROM parked WHERE lp=?", (lp_out,))
        data = c.fetchone()
        if data:
            entry_t = datetime.datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.now()
            diff = now - entry_t
            hours = math.ceil(diff.total_seconds() / 3600)
            total_fee = hours * FEE_PER_HOUR
            
            c1, c2 = st.columns(2)
            c1.metric("Giờ vào", data[1])
            c1.metric("Thời gian đậu", f"{hours} giờ")
            c1.metric("Tổng tiền", f"{total_fee:,.0f} VND")
            
            if data[5]:
                c2.image(data[5], caption="Ảnh lúc vào", width=300)
                
            if st.button("XÁC NHẬN THANH TOÁN & CHO XE RA"):
                conn.execute("INSERT INTO history (lp, entry, exit, fee, type) VALUES (?,?,?,?,?)",
                             (lp_out, data[1], now.strftime("%Y-%m-%d %H:%M:%S"), total_fee, data[3]))
                conn.execute("DELETE FROM parked WHERE lp=?", (lp_out,))
                conn.commit()
                st.success(f"Xe {lp_out} đã hoàn tất thanh toán!")
                st.rerun()
        else:
            st.error("Không tìm thấy xe này!")

# --- TAB 4: THỐNG KÊ ---
with tabs[3]:
    st.subheader("📊 Kết quả kinh doanh")
    df_h = pd.read_sql_query("SELECT * FROM history", conn)
    if not df_h.empty:
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Tổng doanh thu", f"{df_h['fee'].sum():,.0f} VND")
        col_m2.metric("Số lượt xe", len(df_h))
        
        st.bar_chart(df_h.groupby('type')['fee'].sum())
        st.write("📜 Lịch sử giao dịch gần nhất")
        st.table(df_h.tail(10))
    else:
        st.write("Chưa có dữ liệu lịch sử.")
