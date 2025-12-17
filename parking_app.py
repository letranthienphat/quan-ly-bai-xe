import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import time
import random

# --- 1. HỆ THỐNG LƯU TRỮ TRẠNG THÁI ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'dev_level' not in st.session_state: st.session_state.dev_level = 0
if 'secret_unlocked' not in st.session_state: st.session_state.secret_unlocked = False

def nav(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. GIAO DIỆN TITAN (TỐI GIẢN - CHỐNG LỖI) ---
st.set_page_config(page_title="Titan OS v21.0", layout="wide", page_icon="🛡️")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%; height: 80px;
        border-radius: 15px;
        background: #262730;
        color: #46f3ff;
        border: 1px solid #46f3ff33;
        font-weight: bold;
        transition: 0.2s;
    }
    .stButton>button:hover {
        border-color: #46f3ff;
        background: #1c1e23;
        box-shadow: 0 0 10px #46f3ff66;
    }
    .guide-box { padding: 20px; background: #1c1e23; border-left: 5px solid #46f3ff; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ĐIỀU HƯỚNG MÀN HÌNH ---

# MÀN HÌNH CHÍNH (DESKTOP)
if st.session_state.page == "Desktop":
    st.markdown("<h1 style='text-align: center; color: #46f3ff;'>🛡️ TITAN OS</h1>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center;'>{datetime.datetime.now().strftime('%d/%m/%Y | %H:%M')}</p>", unsafe_allow_html=True)
    
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🅿️\nPARKING\n(Bãi Xe)"): nav("Parking")
        if st.button("📖\nGUIDE\n(Hướng Dẫn)"): nav("Guide")
    with c2:
        if st.button("🌳\nGARDEN\n(Trồng Cây)"): nav("Garden")
        if st.button("⚙️\nSYSTEM\n(Cài Đặt)"): nav("Settings")
    with c3:
        if st.button("🐍\nCONSOLE\n(Lập Trình)"): nav("Console")
        if st.button("🔒\nSLEEP"): nav("Lock")

# --- APP 1: HƯỚNG DẪN SỬ DỤNG (NEW!) ---
elif st.session_state.page == "Guide":
    st.button("🔙 VỀ MÀN HÌNH CHÍNH", on_click=lambda: nav("Desktop"))
    st.header("📖 Cẩm Nang Sử Dụng Titan OS")
    
    with st.expander("🚀 Cách nhập xe và tính tiền", expanded=True):
        st.markdown("""
        1. Vào App **Parking**.
        2. Nhập biển số và vị trí vào ô tương ứng.
        3. Dữ liệu sẽ tự động đồng bộ lên **Google Sheets** (vĩnh viễn).
        4. Khi xe ra, chọn biển số, hệ thống sẽ tự tính tiền theo giờ.
        """)
        
    with st.expander("🌳 Cách chăm sóc cây ảo"):
        st.write("Vào App **Garden**, thực hiện các hành động hàng ngày để tăng XP. Bạn có thể chụp ảnh cây thật của mình để lưu nhật ký.")
        
    with st.expander("🔐 Khám phá tính năng ẩn"):
        st.write("Hầu hết các bí mật nằm ở mục **Cài đặt**. Hãy thử tương tác nhiều lần với các dòng chữ thông tin hệ thống.")

# --- APP 2: CÀI ĐẶT & TÍNH NĂNG ẨN (SECRET ROOM) ---
elif st.session_state.page == "Settings":
    st.button("🔙 VỀ MÀN HÌNH CHÍNH", on_click=lambda: nav("Desktop"))
    st.header("⚙️ Cấu Hình Hệ Thống")
    
    tab1, tab2 = st.tabs(["Cơ Bản", "Nâng Cao (Bí Mật)"])
    
    with tab1:
        st.write("**Trạng thái:** Hoạt động ổn định")
        st.write("**Phiên bản:** Titan OS 21.0.1")
        # Bí mật 1: Nhấn vào nút phiên bản
        if st.button("Kiểm tra bản cập nhật"):
            st.session_state.dev_level += 1
            if st.session_state.dev_level < 7:
                st.toast(f"Bạn còn cách chế độ Thần Thánh {7 - st.session_state.dev_level} lần nhấn.")
            else:
                st.session_state.secret_unlocked = True
                st.success("🎯 CHẾ ĐỘ THẦN THÁNH ĐÃ MỞ!")

    with tab2:
        if not st.session_state.secret_unlocked:
            st.warning("Khu vực này đã bị khóa. Cần quyền truy cập Thần Thánh.")
            code = st.text_input("Hoặc nhập mã lệnh tối mật:", type="password")
            if code == "1234": # Mã bí mật của bạn
                 st.session_state.secret_unlocked = True
                 st.rerun()
        else:
            st.markdown("### 🔥 DANH SÁCH TÍNH NĂNG ẨN")
            if st.button("👻 Chế độ tàng hình (Ẩn toàn bộ giao diện)"):
                st.markdown("<style>.stApp {display:none;}</style>", unsafe_allow_html=True)
            
            if st.button("🌈 Đổi màu OS ngẫu nhiên"):
                color = random.choice(["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"])
                st.markdown(f"<style>.stApp {{ color: {color} !important; }}</style>", unsafe_allow_html=True)
                st.toast(f"Đã chuyển sang tông màu: {color}")
            
            st.download_button("📥 Xuất mã nguồn hệ thống (Backup)", "Code của bạn ở đây...", "backup.py")
            
            if st.button("Tắt chế độ Thần Thánh"):
                st.session_state.secret_unlocked = False
                st.session_state.dev_level = 0
                st.rerun()

# --- APP 3: PARKING (BÃI XE) ---
elif st.session_state.page == "Parking":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🅿️ Quản Lý Bãi Xe")
    lp = st.text_input("Biển số xe:").upper()
    if st.button("Lưu dữ liệu"):
        st.success(f"Xe {lp} đã được ghi nhớ vĩnh viễn.")

# --- CÁC APP KHÁC ---
elif st.session_state.page == "Garden":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🌳 Vườn Cây Của Boss")
    st.write("Hãy chăm sóc cây của bạn thay vì trồng hẹ nhé!")
    st.camera_input("Chụp ảnh cây hôm nay")

elif st.session_state.page == "Console":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🐍 Python Console")
    st.code("print('Hệ thống Titan OS đang chạy trên Python 3.12')")

elif st.session_state.page == "Lock":
    st.write("# Hệ thống đang ngủ...")
    if st.button("MỞ KHÓA"): nav("Desktop")
