import streamlit as st
import time
import datetime
import random

# --- 1. KHỞI TẠO HỆ THỐNG ---
if 'installed_apps' not in st.session_state:
    st.session_state.installed_apps = ["Parking", "Botany", "Settings", "Store", "Guide"]
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'theme_color' not in st.session_state: st.session_state.theme_color = "#00f2ff"
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

# Danh sách 30 App giả lập trong Store
ALL_APPS = {
    "Parking": "🅿️", "Botany": "🌳", "Settings": "⚙️", "Store": "🏪", "Guide": "📖",
    "Browser": "🌐", "Finance": "💎", "Notes": "📝", "Camera": "📷", "Calculator": "🔢",
    "Weather": "☁️", "Maps": "📍", "Clock": "⏰", "Music": "🎵", "Video": "🎬",
    "Chat": "💬", "Mail": "✉️", "Calendar": "📅", "Health": "❤️", "Files": "📁",
    "News": "📰", "Stocks": "📈", "Games": "🎮", "Translate": "🔤", "Recorder": "🎙️",
    "Flashlight": "🔦", "Contacts": "👤", "Terminal": "💻", "Backup": "☁️", "AI-Assistant": "🤖"
}

def nav(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. GIAO DIỆN GALAXY UI ---
st.set_page_config(page_title="Titan Galaxy OS", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: white; }}
    .stButton>button {{
        width: 100%; height: 90px; border-radius: 20px;
        background: #111; color: {st.session_state.theme_color};
        border: 2px solid {st.session_state.theme_color}22;
        font-size: 14px; font-weight: bold; transition: 0.3s;
    }}
    .stButton>button:hover {{
        border-color: {st.session_state.theme_color};
        box-shadow: 0 0 15px {st.session_state.theme_color}55;
        transform: scale(1.05);
    }}
    .status-bar {{ text-align: right; color: {st.session_state.theme_color}; padding: 10px; font-family: monospace; }}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ĐIỀU HƯỚNG ---

# MÀN HÌNH CHÍNH (DESKTOP)
if st.session_state.page == "Desktop":
    st.markdown(f"<div class='status-bar'>📶 GALAXY-NET | 🔋 95% | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)
    st.title("🛡️ TITAN GALAXY")
    
    # Hiển thị các App đã cài đặt
    cols = st.columns(5)
    for idx, app_name in enumerate(st.session_state.installed_apps):
        icon = ALL_APPS.get(app_name, "📦")
        with cols[idx % 5]:
            if st.button(f"{icon}\n{app_name}"):
                nav(app_name)
    
    st.divider()
    if st.button("➕ VÀO CỬA HÀNG ĐỂ CÀI THÊM APP"): nav("Store")

# APP: STORE (CỬA HÀNG GIẢ LẬP)
elif st.session_state.page == "Store":
    st.button("🔙 THOÁT CỬA HÀNG", on_click=lambda: nav("Desktop"))
    st.header("🏪 Titan Store - Multiverse")
    st.write("Chọn ứng dụng để cài đặt vào màn hình chính:")
    
    for app_id, icon in ALL_APPS.items():
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.write(f"{icon} **{app_id}** - Ứng dụng hệ thống v26.0")
        with col_b:
            if app_id in st.session_state.installed_apps:
                st.write("✅ Đã cài")
            else:
                if st.button(f"Cài đặt", key=app_id):
                    st.session_state.installed_apps.append(app_id)
                    st.toast(f"Đang cài đặt {app_id}...")
                    time.sleep(1)
                    st.rerun()

# APP: BROWSER (GOOGLE SEARCH)
elif st.session_state.page == "Browser":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🌐 Titan Web Browser")
    q = st.text_input("Tìm kiếm trên Google:")
    if st.button("TÌM KIẾM"):
        st.link_button("Mở kết quả Google", f"https://www.google.com/search?q={q}")

# APP: BOTANY (TRỒNG CÂY)
elif st.session_state.page == "Botany":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("🌳 Eco Garden")
    st.write("Vườn cây ảo của Boss")
    st.camera_input("Chụp ảnh cây thực tế")
    if st.button("Tưới nước"): st.balloons()

# APP: SETTINGS (CÀI ĐẶT ẨN)
elif st.session_state.page == "Settings":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("⚙️ Cài Đặt Hệ Thống")
    
    # Tính năng ẩn nâng cao
    st.subheader("Bí mật hệ điều hành")
    if st.button("Kiểm tra thông tin hạt nhân (Kernel)"):
        if 'k_clicks' not in st.session_state: st.session_state.k_clicks = 0
        st.session_state.k_clicks += 1
        if st.session_state.k_clicks >= 7:
            st.session_state.theme_color = "#ff00ff"
            st.success("🌈 ĐÃ MỞ KHÓA GIAO DIỆN ĐA VŨ TRỤ (MÀU HỒNG NEON)!")
    
    if st.button("🗑️ Gỡ cài đặt tất cả App (Reset OS)"):
        st.session_state.installed_apps = ["Parking", "Botany", "Settings", "Store", "Guide"]
        st.rerun()

# CÁC APP KHÁC (GIẢ LẬP GIAO DIỆN)
else:
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header(f"🖥️ Ứng dụng: {st.session_state.page}")
    st.info(f"Chào Boss! Ứng dụng {st.session_state.page} đang được tối ưu hóa dữ liệu từ Cloud.")
    st.write("Dữ liệu: [OK] | Kết nối: [SECURE]")
