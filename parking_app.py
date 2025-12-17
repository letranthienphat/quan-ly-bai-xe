import streamlit as st
import time
import datetime
import random
import pandas as pd

# --- 1. CORE ENGINE & 30+ FEATURES STATE ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'os_init' not in st.session_state:
    # Khởi tạo 30+ tham số cấu hình hệ thống
    st.session_state.os_init = True
    st.session_state.sys_vars = {
        "bright": 80, "vol": 50, "dark_mode": True, "firewall": True,
        "auto_update": True, "ram_boost": False, "dev_mode": False,
        "language": "Tiếng Việt", "region": "VN", "font_size": 14,
        "cursor_eff": True, "bt_status": "Off", "wifi_ssd": "Titan_5G",
        "encryption": "AES-256", "ai_assist": True, "backup_cloud": False,
        "vpn": False, "proxy": "None", "refresh_rate": "120Hz",
        "gpu_accel": True, "biometric": "FaceID", "stealth_mode": False,
        "packet_insp": False, "log_level": "Debug", "port_8080": "Closed",
        "haptic": True, "eco_mode": False, "overclock": False,
        "storage_clean": 100, "temp_unit": "Celsius", "clock_24h": True
    }
    st.session_state.parking_slots = [random.choice(["Trống", "Đã đỗ"]) for _ in range(20)]
    st.session_state.logs = ["Hệ thống khởi động thành công..."]

def nav(p):
    st.session_state.page = p
    st.rerun()

# --- 2. THEME ENGINE ---
st.set_page_config(page_title="Titan Omnipotence OS", layout="wide")
bg = "#000000" if st.session_state.sys_vars["dark_mode"] else "#ffffff"
txt = "#00f2ff" if st.session_state.sys_vars["dark_mode"] else "#333333"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .stButton>button {{ border-radius: 5px; border: 1px solid {txt}44; background: transparent; color: {txt}; }}
    .status-bar {{ display: flex; justify-content: space-between; padding: 5px 20px; background: #111; border-bottom: 1px solid {txt}22; position: fixed; top: 0; width: 100%; z-index: 999; }}
    .card {{ padding: 15px; border: 1px solid #333; border-radius: 10px; background: rgba(255,255,255,0.05); margin-bottom: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- 3. STATUS BAR ---
st.markdown(f"<div class='status-bar'><span>🛰️ KERNEL V32.0 | 🛡️ Firewall: {'ON' if st.session_state.sys_vars['firewall'] else 'OFF'}</span><span>🔋 100% | {datetime.datetime.now().strftime('%H:%M')}</span></div>", unsafe_allow_html=True)
st.write("###")

# --- 4. APP LOGIC ---

# 4.1 MÀN HÌNH CHÍNH
if st.session_state.page == "Desktop":
    st.title("🛡️ TITAN OMNIPOTENCE")
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("🅿️ PARKING PRO"): nav("Parking")
    with c2: 
        if st.button("⚙️ SETTINGS"): nav("Settings")
    with c3:
        if st.button("🛠️ TERMINAL"): nav("Terminal")
    with c4:
        if st.button("📊 MONITOR"): nav("Monitor")
    
    st.divider()
    st.write("### 🧩 Widgets")
    w1, w2 = st.columns(2)
    w1.metric("Nhiệt độ CPU", "42°C", "2°C")
    w2.metric("Bộ nhớ trống", f"{st.session_state.sys_vars['storage_clean']} GB", "-0.2 GB")

# 4.2 APP: SETTINGS (PHẦN NÀY CHỨA 30+ TÍNH NĂNG)
elif st.session_state.page == "Settings":
    st.button("🔙 HOME", on_click=lambda: nav("Desktop"))
    st.header("⚙️ Hệ Thống Cài Đặt Chuyên Sâu")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Hiển thị & Âm thanh", "Bảo mật & Mạng", "Hiệu năng & Dev", "Lưu trữ & Khác"])
    
    with tab1:
        st.session_state.sys_vars["bright"] = st.slider("Độ sáng màn hình", 0, 100, st.session_state.sys_vars["bright"])
        st.session_state.sys_vars["vol"] = st.slider("Âm lượng hệ thống", 0, 100, st.session_state.sys_vars["vol"])
        st.session_state.sys_vars["dark_mode"] = st.toggle("Chế độ Dark Mode", st.session_state.sys_vars["dark_mode"])
        st.session_state.sys_vars["font_size"] = st.number_input("Kích thước chữ (px)", 10, 30, st.session_state.sys_vars["font_size"])
        st.session_state.sys_vars["refresh_rate"] = st.selectbox("Tần số quét", ["60Hz", "90Hz", "120Hz", "144Hz"])
        st.session_state.sys_vars["temp_unit"] = st.radio("Đơn vị nhiệt độ", ["Celsius", "Fahrenheit"])
        st.session_state.sys_vars["clock_24h"] = st.checkbox("Sử dụng định dạng 24h", st.session_state.sys_vars["clock_24h"])

    with tab2:
        st.session_state.sys_vars["firewall"] = st.toggle("Tường lửa Titan", st.session_state.sys_vars["firewall"])
        st.session_state.sys_vars["encryption"] = st.selectbox("Thuật toán mã hóa", ["AES-128", "AES-256", "RSA-4096"])
        st.session_state.sys_vars["vpn"] = st.toggle("Titan VPN (Private)", st.session_state.sys_vars["vpn"])
        st.session_state.sys_vars["biometric"] = st.selectbox("Xác thực sinh trắc", ["Vân tay", "FaceID", "Mống mắt"])
        st.session_state.sys_vars["stealth_mode"] = st.toggle("Chế độ ẩn danh (Stealth)", st.session_state.sys_vars["stealth_mode"])
        st.session_state.sys_vars["packet_insp"] = st.checkbox("Kiểm tra gói tin sâu (DPI)", st.session_state.sys_vars["packet_insp"])
        st.session_state.sys_vars["wifi_ssd"] = st.text_input("Tên Wifi đang kết nối", st.session_state.sys_vars["wifi_ssd"])

    with tab3:
        st.session_state.sys_vars["dev_mode"] = st.toggle("Developer Mode", st.session_state.sys_vars["dev_mode"])
        if st.session_state.sys_vars["dev_mode"]:
            st.session_state.sys_vars["overclock"] = st.checkbox("Overclock CPU (+20%)")
            st.session_state.sys_vars["gpu_accel"] = st.toggle("Tăng tốc phần cứng GPU")
            st.session_state.sys_vars["log_level"] = st.select_slider("Mức độ Log", options=["Info", "Warning", "Error", "Debug", "Trace"])
            st.session_state.sys_vars["port_8080"] = st.radio("Cổng 8080", ["Open", "Closed"])
        st.session_state.sys_vars["ram_boost"] = st.toggle("Tối ưu hóa RAM tự động")
        st.session_state.sys_vars["auto_update"] = st.checkbox("Tự động tải bản vá lỗi")

    with tab4:
        st.session_state.sys_vars["language"] = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English", "Pythonic"])
        st.session_state.sys_vars["ai_assist"] = st.toggle("Trợ lý AI Gemini Core")
        st.session_state.sys_vars["backup_cloud"] = st.toggle("Sao lưu Cloud hằng ngày")
        st.session_state.sys_vars["eco_mode"] = st.toggle("Tiết kiệm điện (Eco)")
        if st.button("🧹 DỌN RÁC HỆ THỐNG"):
            st.session_state.sys_vars["storage_clean"] = 100
            st.balloons()
            st.success("Đã dọn sạch rác!")

# 4.3 APP: PARKING PRO (CẢI TIẾN)
elif st.session_state.page == "Parking":
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header("🅿️ Hệ Thống Quản Lý Bãi Xe V32")
    cols = st.columns(5)
    for i, slot in enumerate(st.session_state.parking_slots):
        with cols[i % 5]:
            color = "red" if slot == "Đã đỗ" else "green"
            if st.button(f"Vị trí {i+1}\n({slot})", key=f"slot_{i}"):
                st.session_state.parking_slots[i] = "Đã đỗ" if slot == "Trống" else "Trống"
                st.rerun()

# 4.4 APP: MONITOR (THEO DÕI)
elif st.session_state.page == "Monitor":
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header("📊 System Monitor")
    data = pd.DataFrame({
        'Tiến trình': ['Kernel', 'UI Render', 'Firewall', 'Parking_DB', 'AI_Agent'],
        'CPU (%)': [random.randint(5,15) for _ in range(5)],
        'RAM (MB)': [random.randint(100,500) for _ in range(5)]
    })
    st.table(data)

# 4.5 APP: TERMINAL (DÀNH CHO BOSS)
elif st.session_state.page == "Terminal":
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header("🖥️ Titan Terminal")
    cmd = st.text_input("Nhập lệnh hệ thống (ví dụ: /help, /scan, /reboot)")
    if cmd == "/reboot": nav("Desktop")
    elif cmd == "/scan": st.write("Scanning... Clear!")
    st.code("root@titan_os:~# " + (cmd if cmd else ""))
