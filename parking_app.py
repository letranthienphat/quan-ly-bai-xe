import streamlit as st
import time
import datetime
import random
import pandas as pd

# --- 1. HỆ THỐNG QUẢN LÝ TRẠNG THÁI (CORE ENGINE) ---
# Khởi tạo 30+ biến hệ thống ngay từ đầu
if 'os' not in st.session_state:
    st.session_state.os = {
        "page": "Lock",
        "pin": "1234",
        "theme": "#00f2ff",
        "is_dark": True,
        "installed": ["Parking", "Botany", "Store", "Settings", "Security", "Monitor"],
        "gold": 500,
        "storage_used": 42.5,
        "cpu_usage": 15,
        "ram_usage": 1200,
        "firewall": True,
        "wifi": "Titan_Hyper_5G",
        "notifications": [],
        "dev_mode": False,
        "update_ready": False,
        "auto_save": True,
        "location": "Hanoi, VN",
        "language": "Tiếng Việt",
        "font_size": 16,
        "overclock": False,
        "vpn": False,
        "stealth": False,
        "biometric": "On",
        "eco_mode": False,
        "last_reboot": str(datetime.datetime.now())
    }

# Hàm chuyển trang an toàn (Sửa lỗi no-op)
def change_page(target):
    st.session_state.os["page"] = target

# --- 2. GIAO DIỆN HỆ THỐNG ---
st.set_page_config(page_title="Titan OS v33", layout="wide")

# CSS cho Giao diện Glassmorphism
st.markdown(f"""
<style>
    .stApp {{ background: { '#050505' if st.session_state.os['is_dark'] else '#f0f2f6' }; color: {st.session_state.os['theme']}; }}
    .status-bar {{ 
        display: flex; justify-content: space-between; padding: 5px 20px;
        background: rgba(0,0,0,0.8); border-bottom: 1px solid {st.session_state.os['theme']}44;
        position: fixed; top: 0; left: 0; width: 100%; z-index: 1000;
    }}
    .app-box {{
        background: rgba(255,255,255,0.05); border: 1px solid #333;
        padding: 20px; border-radius: 15px; text-align: center; transition: 0.3s;
    }}
    .app-box:hover {{ border-color: {st.session_state.os['theme']}; transform: scale(1.02); }}
</style>
""", unsafe_allow_html=True)

# --- 3. STATUS BAR (THÔNG TIN THỰC THỜI) ---
st.markdown(f"""<div class='status-bar'>
    <span>🛰️ {st.session_state.os['wifi']} | 💰 {st.session_state.os['gold']}G</span>
    <span>💾 RAM: {random.randint(1100, 1300)}MB | 🔋 100% | {datetime.datetime.now().strftime('%H:%M')}</span>
</div>""", unsafe_allow_html=True)
st.write("###")

# --- 4. LOGIC ĐIỀU HƯỚNG ---

# MÀN HÌNH KHÓA
if st.session_state.os["page"] == "Lock":
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>🔓 TITAN CORE</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        pin = st.text_input("MÃ PIN", type="password", key="pin_in")
        if st.button("XÁC NHẬN"):
            if pin == st.session_state.os["pin"]:
                change_page("Desktop")
                st.rerun()
            else: st.error("Sai PIN!")

# MÀN HÌNH CHÍNH (DESKTOP)
elif st.session_state.os["page"] == "Desktop":
    st.title("🌌 TITAN DESKTOP")
    
    # 30+ App Grid (Mô phỏng bằng vòng lặp cài đặt)
    cols = st.columns(4)
    for idx, app in enumerate(st.session_state.os["installed"]):
        with cols[idx % 4]:
            if st.button(f"📦 {app}", key=f"btn_{app}"):
                change_page(app)
                st.rerun()

# ỨNG DỤNG: CÀI ĐẶT (30+ TÍNH NĂNG)
elif st.session_state.os["page"] == "Settings":
    st.button("🔙 BACK", on_click=lambda: change_page("Desktop"))
    st.header("⚙️ System Control Center")
    
    t1, t2, t3, t4 = st.tabs(["Cá nhân hóa", "Bảo mật", "Hiệu năng", "Nâng cao"])
    
    with t1:
        st.session_state.os["theme"] = st.color_picker("Màu chủ đạo OS", st.session_state.os["theme"])
        st.session_state.os["is_dark"] = st.toggle("Chế độ tối", st.session_state.os["is_dark"])
        st.session_state.os["language"] = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English", "Python"])
        st.session_state.os["font_size"] = st.slider("Cỡ chữ hệ thống", 12, 24, st.session_state.os["font_size"])
        st.write(f"Vị trí hiện tại: {st.session_state.os['location']}")
        
    with t2:
        st.session_state.os["firewall"] = st.toggle("Tường lửa thông minh", st.session_state.os["firewall"])
        st.session_state.os["vpn"] = st.toggle("Titan VPN", st.session_state.os["vpn"])
        st.session_state.os["biometric"] = st.radio("Sinh trắc học", ["On", "Off"])
        st.session_state.os["stealth"] = st.checkbox("Chế độ ẩn danh")
        if st.button("Đổi mã PIN"): st.info("Tính năng đang bảo trì...")

    with t3:
        st.session_state.os["dev_mode"] = st.toggle("Developer Mode", st.session_state.os["dev_mode"])
        if st.session_state.os["dev_mode"]:
            st.session_state.os["overclock"] = st.checkbox("Ép xung CPU (+30%)")
            st.write("Cổng gỡ lỗi: 8080 (Mở)")
        st.session_state.os["eco_mode"] = st.toggle("Tiết kiệm pin cực độ")
        st.session_state.os["auto_save"] = st.checkbox("Tự động lưu dữ liệu bãi xe")

    with t4:
        st.write(f"Phiên bản Kernel: {st.session_state.os['os_version' if 'os_version' in st.session_state.os else '33.0']}")
        st.write(f"Khởi động lần cuối: {st.session_state.os['last_reboot']}")
        if st.button("RESET TO FACTORY"):
            st.session_state.clear()
            st.rerun()

# ỨNG DỤNG: BÃI XE (PARKING) - CẢI TIẾN
elif st.session_state.os["page"] == "Parking":
    st.button("🔙 EXIT", on_click=lambda: change_page("Desktop"))
    st.header("🅿️ Quản lý bãi xe Thông minh")
    
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        st.write("Sơ đồ bãi xe (Thời gian thực)")
        slots = [random.choice(["🚗", "🅿️"]) for _ in range(20)]
        for i in range(0, 20, 5):
            st.write(f"{slots[i]} | {slots[i+1]} | {slots[i+2]} | {slots[i+3]} | {slots[i+4]}")
    with col_p2:
        st.metric("Tổng chỗ trống", slots.count("🅿️"))
        st.button("In báo cáo ngày")

# CÁC APP KHÁC (GIẢ LẬP)
else:
    st.button("🔙 HOME", on_click=lambda: change_page("Desktop"))
    st.header(f"🖥️ {st.session_state.os['page']}")
    st.info(f"Hệ thống đang chạy module {st.session_state.os['page']} ổn định.")
    st.progress(random.randint(20, 90))
