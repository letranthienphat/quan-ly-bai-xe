import streamlit as st
import pandas as pd
import datetime
import time
import random

# --- 1. KHỞI TẠO HỆ THỐNG BIẾN TOÀN CỤC ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'limit_minutes' not in st.session_state: st.session_state.limit_minutes = 30 # Mặc định 30p
if 'is_recharging' not in st.session_state: st.session_state.is_recharging = False

# --- 2. LOGIC TÍNH PIN GIẢ LẬP THEO THỜI GIAN ---
current_time = time.time()
elapsed = (current_time - st.session_state.start_time) / 60  # Đổi ra phút
battery = max(0, 100 - int((elapsed / st.session_state.limit_minutes) * 100))

# Kiểm tra hết pin
if battery <= 0 and not st.session_state.is_recharging:
    st.session_state.page = "BatteryLow"

# --- 3. GIAO DIỆN TITAN BIO-TECH ---
st.set_page_config(page_title="Titan Bio-Tech OS", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: #00ffcc; }}
    .stButton>button {{
        width: 100%; height: 80px; border-radius: 15px;
        background: #111; color: #00ffcc; border: 1px solid #00ffcc44;
        font-weight: bold; font-size: 16px; transition: 0.3s;
    }}
    .stButton>button:hover {{ border-color: #00ffcc; background: #00ffcc22; box-shadow: 0 0 15px #00ffcc44; }}
    .status-bar {{ font-family: 'Courier New'; text-align: right; padding: 10px; color: #00ffcc; border-bottom: 1px solid #00ffcc22; }}
</style>
""", unsafe_allow_html=True)

# --- 4. ĐIỀU HƯỚNG MÀN HÌNH ---

# MÀN HÌNH HẾT PIN (NGHỈ MẮT)
if st.session_state.page == "BatteryLow":
    st.markdown("<h1 style='text-align:center; color:red; margin-top:100px;'>🪫 HẾT PIN SINH HỌC!</h1>", unsafe_allow_html=True)
    st.warning(f"Bạn đã sử dụng máy liên tục {st.session_state.limit_minutes} phút. Hãy nghỉ mắt 5 phút để bảo vệ sức khỏe.")
    st.info("Hệ thống đang sạc lại năng lượng...")
    if st.button("🔌 BẮT ĐẦU SẠC PIN (Nghỉ 10 giây để thử nghiệm)"):
        st.session_state.is_recharging = True
        with st.status("Đang nạp năng lượng...", expanded=True) as status:
            time.sleep(10) # Giả lập thời gian nghỉ
            st.session_state.start_time = time.time()
            st.session_state.page = "Desktop"
            st.session_state.is_recharging = False
            status.update(label="Sạc đầy! Chào Boss quay lại.", state="complete")
        st.rerun()

# MÀN HÌNH CHÍNH
elif st.session_state.page == "Desktop":
    st.markdown(f"<div class='status-bar'>🛡️ TITAN BIO | 📶 6G | 🔋 {battery}% | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)
    st.title("🛡️ TITAN OS v23")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🅿️\nPARKING\n(Bãi Xe)"): st.session_state.page = "Parking"; st.rerun()
        if st.button("📖\nGUIDE\n(Hướng Dẫn)"): st.session_state.page = "Guide"; st.rerun()
    with col2:
        if st.button("🌳\nBOTANY\n(Trồng Cây)"): st.session_state.page = "Garden"; st.rerun()
        if st.button("⚙️\nSETTINGS\n(Cài Đặt)"): st.session_state.page = "Settings"; st.rerun()
    with col3:
        if st.button("🛡️\nBIO-SEC\n(Quét QR)"): st.toast("Đang khởi động Camera..."); time.sleep(1)
        if st.button("🌙\nSLEEP"): st.session_state.page = "Lock"; st.rerun()

# CÀI ĐẶT THỜI GIAN (TÍNH NĂNG BẠN YÊU CẦU)
elif st.session_state.page == "Settings":
    if st.button("🔙 VỀ DESKTOP"): st.session_state.page = "Desktop"; st.rerun()
    st.header("⚙️ Cài đặt Hệ thống & Sức khỏe")
    
    st.subheader("🔋 Quản lý Pin Sinh Học")
    new_limit = st.slider("Đặt thời gian sử dụng trước khi nghỉ mắt (phút):", 1, 120, st.session_state.limit_minutes)
    if st.button("LƯU CẤU HÌNH"):
        st.session_state.limit_minutes = new_limit
        st.session_state.start_time = time.time() # Reset pin khi đổi cài đặt
        st.success(f"Đã cài đặt: Hệ thống sẽ báo nghỉ sau {new_limit} phút.")

    st.divider()
    st.subheader("🔥 Tính năng ẩn")
    if st.toggle("Kích hoạt chế độ Tiết kiệm Pin (Chữ mờ đi)"):
        st.markdown("<style>.stApp { opacity: 0.6; }</style>", unsafe_allow_html=True)

# TRỒNG CÂY (NÂNG CẤP)
elif st.session_state.page == "Garden":
    if st.button("🔙 BACK"): st.session_state.page = "Desktop"; st.rerun()
    st.header("🌳 Vườn Cây Thông Minh")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.camera_input("Chụp ảnh cây của Boss")
    with col_g2:
        st.write("Cây của bạn đang hấp thụ CO2 tốt.")
        if st.button("TƯỚI CÂY"): st.balloons()

# BÃI XE (PARKING)
elif st.session_state.page == "Parking":
    if st.button("🔙 BACK"): st.session_state.page = "Desktop"; st.rerun()
    st.header("🅿️ Quản Lý Xe Cloud")
    st.text_input("Biển số xe")
    st.button("Gửi dữ liệu")

# HƯỚNG DẪN (GUIDE)
elif st.session_state.page == "Guide":
    if st.button("🔙 BACK"): st.session_state.page = "Desktop"; st.rerun()
    st.header("📖 Cẩm Nang Titan OS")
    st.write("1. **Pin:** Tụt theo thời gian thực dựa trên cài đặt của Boss.")
    st.write("2. **Nghỉ mắt:** Khi pin về 0%, máy sẽ khóa để Boss đi nghỉ.")
    st.write("3. **Bãi xe:** Tự động lưu lên Google Sheets.")
