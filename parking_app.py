import streamlit as st
import pandas as pd
import datetime
import time
import webbrowser

# --- 1. CORE OS ENGINE ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'limit_min' not in st.session_state: st.session_state.limit_min = 45
if 'theme_color' not in st.session_state: st.session_state.theme_color = "#00f2ff"
if 'is_dark' not in st.session_state: st.session_state.is_dark = True

# --- 2. LOGIC PIN & SỨC KHỎE ---
elapsed = (time.time() - st.session_state.start_time) / 60
battery = max(0, 100 - int((elapsed / st.session_state.limit_min) * 100))

if battery <= 0:
    st.session_state.page = "RestMode"

# --- 3. GIAO DIỆN CYBER-TECH ---
st.set_page_config(page_title="Titan Omega OS v25", layout="wide")
theme_bg = "#050505" if st.session_state.is_dark else "#f0f2f6"
theme_txt = st.session_state.theme_color if st.session_state.is_dark else "#333333"

st.markdown(f"""
<style>
    .stApp {{ background-color: {theme_bg}; color: {theme_txt}; }}
    .stButton>button {{
        width: 100%; height: 70px; border-radius: 12px;
        background: {"#111" if st.session_state.is_dark else "#fff"}; 
        color: {st.session_state.theme_color}; 
        border: 1px solid {st.session_state.theme_color}44;
        font-weight: bold; transition: 0.3s;
    }}
    .status-bar {{ font-family: 'Courier New'; text-align: right; padding: 5px; color: {st.session_state.theme_color}; border-bottom: 1px solid #444; }}
    .search-box {{ background: #111; padding: 20px; border-radius: 15px; border: 1px solid {st.session_state.theme_color}; }}
</style>
""", unsafe_allow_html=True)

# --- 4. HỆ THỐNG ĐIỀU HƯỚNG ---

if st.session_state.page == "RestMode":
    st.error("🪫 HẾT PIN! Boss hãy nghỉ mắt 5 phút.")
    if st.button("🔌 SẠC PIN NHANH"):
        st.session_state.start_time = time.time()
        st.session_state.page = "Desktop"
        st.rerun()

elif st.session_state.page == "Desktop":
    st.markdown(f"<div class='status-bar'>🛡️ OMEGA v25 | 🔋 {battery}% | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)
    st.title("🛡️ TITAN OMEGA OS")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🅿️\nPARKING"): st.session_state.page = "Parking"; st.rerun()
    with c2:
        if st.button("🌳\nBOTANY"): st.session_state.page = "Garden"; st.rerun()
    with c3:
        if st.button("🌐\nBROWSER\n(Google)"): st.session_state.page = "Browser"; st.rerun()
    with c4:
        if st.button("⚙️\nSETTINGS"): st.session_state.page = "Settings"; st.rerun()

# --- APP: BROWSER (TÍNH NĂNG MỚI THEO YÊU CẦU) ---
elif st.session_state.page == "Browser":
    if st.button("🔙 THOÁT"): st.session_state.page = "Desktop"; st.rerun()
    st.header("🌐 Titan Search Engine")
    
    st.markdown("<div class='search-box'>", unsafe_allow_html=True)
    query = st.text_input("Nhập nội dung cần tìm trên Google:", placeholder="Ví dụ: Cách chăm sóc cây cảnh...")
    
    col_s1, col_s2 = st.columns([1, 4])
    with col_s1:
        search_clicked = st.button("🔍 TÌM KIẾM")
    
    if search_clicked and query:
        # Cách 1: Tạo link trực tiếp
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        st.success(f"Đã tìm thấy kết quả cho: {query}")
        
        # Hiển thị kết quả giả lập và nút mở tab mới
        st.info("Vì lý do bảo mật, Google sẽ mở trong một Tab mới để đảm bảo Boss không bị theo dõi.")
        st.link_button("👉 NHẤN VÀO ĐÂY ĐỂ XEM KẾT QUẢ GOOGLE", search_url)
        
        # Easter Egg: Nếu tìm từ khóa "X-OS"
        if "X-OS" in query.upper():
            st.warning("⚠️ Phát hiện truy cập vào dữ liệu tối mật của hệ điều hành!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- APP: SETTINGS (TÍNH NĂNG ẨN) ---
elif st.session_state.page == "Settings":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("⚙️ Hệ Thống")
    
    # Tính năng ẩn: Nhấn 7 lần vào chữ Pin
    if st.button(f"Trạng thái năng lượng: {battery}%"):
        if 'pin_clicks' not in st.session_state: st.session_state.pin_clicks = 0
        st.session_state.pin_clicks += 1
        if st.session_state.pin_clicks >= 7:
            st.session_state.theme_color = "#ff0055" # Đổi sang màu đỏ rực
            st.success("🔥 KÍCH HOẠT CHẾ ĐỘ OVERDRIVE (MÀU ĐỎ)!")
    
    st.divider()
    limit = st.slider("Cài đặt thời gian sử dụng (phút):", 5, 120, st.session_state.limit_min)
    if st.button("Lưu cấu hình"):
        st.session_state.limit_min = limit
        st.session_state.start_time = time.time()
        st.rerun()

# Các app khác giữ nguyên cấu trúc
elif st.session_state.page == "Parking":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("🅿️ Bãi Xe Cloud")
    st.text_input("Biển số")

elif st.session_state.page == "Garden":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("🌳 Vườn Cây")
    st.camera_input("Chụp ảnh cây")
