import streamlit as st
import time
import datetime
import random

# --- 1. CORE OS INITIALIZATION ---
if 'page' not in st.session_state: st.session_state.page = "Lock"
if 'pin_code' not in st.session_state: st.session_state.pin_code = "1234"
if 'os_version' not in st.session_state: st.session_state.os_version = "29.0"
if 'theme_color' not in st.session_state: st.session_state.theme_color = "#00f2ff"
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'limit_min' not in st.session_state: st.session_state.limit_min = 60

# Kho lưu trữ ứng dụng đầy đủ (App Registry)
APP_REGISTRY = {
    "Parking": {"icon": "🅿️", "desc": "Quản lý bãi xe chuyên nghiệp v29", "cat": "Work"},
    "Botany": {"icon": "🌳", "desc": "Nhật ký trồng cây thông minh", "cat": "Eco"},
    "Store": {"icon": "🏪", "desc": "Cửa hàng ứng dụng Galaxy", "cat": "System"},
    "Finance": {"icon": "💎", "desc": "Theo dõi thu nhập bãi xe", "cat": "Work"},
    "Browser": {"icon": "🌐", "desc": "Duyệt web Titan-Net", "cat": "Tools"},
    "Settings": {"icon": "⚙️", "desc": "Cấu hình & Bảo mật cao cấp", "cat": "System"},
    "Security": {"icon": "🛡️", "desc": "Quét virus & Mã hóa dữ liệu", "cat": "System"},
    "Guide": {"icon": "📖", "desc": "Hướng dẫn sử dụng toàn tập", "cat": "System"},
    "Camera": {"icon": "📷", "desc": "Chụp ảnh cây & hiện trường", "cat": "Tools"},
    "Weather": {"icon": "☁️", "desc": "Thời tiết cho nhà nông", "cat": "Eco"},
}

if 'installed_apps' not in st.session_state:
    st.session_state.installed_apps = ["Parking", "Botany", "Store", "Settings", "Guide"]

def nav(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. GIAO DIỆN MULTIVERSE UI ---
st.set_page_config(page_title="Titan Multiverse OS", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: white; font-family: 'Segoe UI', sans-serif; }}
    .status-bar {{ 
        display: flex; justify-content: space-between; padding: 5px 20px;
        background: rgba(20,20,20,0.9); border-bottom: 1px solid {st.session_state.theme_color}44;
        position: fixed; top: 0; left:0; width: 100%; z-index: 1000;
    }}
    .app-card {{
        background: #111; border: 1px solid #333; padding: 15px;
        border-radius: 15px; margin-bottom: 10px; transition: 0.3s;
    }}
    .app-card:hover {{ border-color: {st.session_state.theme_color}; box-shadow: 0 0 15px {st.session_state.theme_color}33; }}
</style>
""", unsafe_allow_html=True)

# --- 3. STATUS BAR ---
elapsed = (time.time() - st.session_state.start_time) / 60
battery = max(0, 100 - int((elapsed / st.session_state.limit_min) * 100))
st.markdown(f"""<div class='status-bar'>
    <span>🛰️ TITAN-SAT | 💾 RAM: {random.randint(40,70)}%</span>
    <span>🔋 {battery}% | 🔑 SECURE | {datetime.datetime.now().strftime('%H:%M')}</span>
</div>""", unsafe_allow_html=True)
st.write("###")

# --- 4. NAVIGATION LOGIC ---

# MÀN HÌNH KHÓA (LOCK)
if st.session_state.page == "Lock":
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>🔒 TITAN OS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        pin = st.text_input("ENTER PIN", type="password")
        if st.button("UNLOCK SYSTEM"):
            if pin == st.session_state.pin_code: nav("Desktop")
            else: st.error("Sai mã PIN!")
        st.caption("Default PIN: 1234")

# MÀN HÌNH CHÍNH (DESKTOP)
elif st.session_state.page == "Desktop":
    if battery <= 0: nav("BatteryLow")
    st.title("🌌 TITAN DESKTOP")
    
    # Hiển thị App Drawer (Grid)
    cols = st.columns(4)
    for idx, app_name in enumerate(st.session_state.installed_apps):
        app_info = APP_REGISTRY.get(app_name, {"icon": "📦"})
        with cols[idx % 4]:
            if st.button(f"{app_info['icon']}\n{app_name}"): nav(app_name)

# MÀN HÌNH CỬA HÀNG (STORE 3.0)
elif st.session_state.page == "Store":
    st.button("🔙 BACK TO HOME", on_click=lambda: nav("Desktop"))
    st.header("🏪 Titan Store - Infinity Market")
    
    for name, info in APP_REGISTRY.items():
        with st.container():
            st.markdown("<div class='app-card'>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 4, 2])
            with c1: st.markdown(f"## {info['icon']}")
            with c2: 
                st.write(f"**{name}**")
                st.caption(info['desc'])
            with c3:
                if name in st.session_state.installed_apps:
                    st.success("Installed")
                elif st.button(f"Install", key=f"store_{name}"):
                    st.session_state.installed_apps.append(name)
                    st.toast(f"Đã cài {name}!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# MÀN HÌNH BẢO MẬT (SECURITY)
elif st.session_state.page == "Security":
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header("🛡️ Titan Security Center")
    if st.button("QUÉT VIRUS HỆ THỐNG"):
        with st.status("Đang quét Kernel..."):
            time.sleep(2)
            st.success("Hệ thống sạch 100%!")
    st.divider()
    new_pin = st.text_input("Đổi mã PIN mới", type="password")
    if st.button("CẬP NHẬT PIN"):
        st.session_state.pin_code = new_pin
        st.success("Đã đổi mã PIN!")

# CÁC APP KHÁC (STUB)
else:
    st.button("🔙 EXIT APP", on_click=lambda: nav("Desktop"))
    app_info = APP_REGISTRY.get(st.session_state.page, {"icon": "📦", "desc": "Unknown"})
    st.header(f"{app_info['icon']} {st.session_state.page}")
    st.write(app_info['desc'])
    
    if st.session_state.page == "Settings":
        st.subheader("Personalization")
        st.session_state.theme_color = st.color_picker("OS Accent Color", st.session_state.theme_color)
        st.session_state.limit_min = st.slider("Battery Life (Min)", 5, 200, st.session_state.limit_min)

    if st.session_state.page == "Botany":
        st.camera_input("Plant Daily Photo")
        if st.button("Water Plant"): st.balloons()

    if st.session_state.page == "Browser":
        q = st.text_input("Search Google")
        if q: st.link_button("View Results", f"https://www.google.com/search?q={q}")
