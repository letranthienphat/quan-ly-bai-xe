import streamlit as st
import time
import datetime
import random

# --- 1. KERNEL INITIALIZATION ---
if 'page' not in st.session_state: st.session_state.page = "Lock"
if 'is_infected' not in st.session_state: st.session_state.is_infected = False
if 'virus_type' not in st.session_state: st.session_state.virus_type = None
if 'installed_apps' not in st.session_state: 
    st.session_state.installed_apps = ["Parking", "Botany", "Store", "Settings"]

# --- 2. CƠ CHẾ VIRUS NGẪU NHIÊN (TRÒ ĐÙA) ---
# Tỉ lệ 10% mỗi lần load trang sẽ bị dính virus nếu chưa có app bảo mật
if 'Security' not in st.session_state.installed_apps and random.random() < 0.1:
    st.session_state.is_infected = True
    st.session_state.virus_type = random.choice(["Ransomware", "Adware", "Glitch"])

def nav(p):
    st.session_state.page = p
    st.rerun()

# --- 3. GIAO DIỆN HỆ THỐNG ---
st.set_page_config(page_title="Titan Chaos OS v30", layout="wide")

# CSS cho hiệu ứng Virus
if st.session_state.is_infected:
    if st.session_state.virus_type == "Glitch":
        st.markdown("<style>.stApp { filter: hue-rotate(90deg) invert(1); transform: skewX(2deg); }</style>", unsafe_allow_html=True)
    elif st.session_state.virus_type == "Adware":
        st.toast("🔥 BẠN ĐÃ TRÚNG THƯỞNG 1 TỶ ĐỒNG! CLICK NGAY!", icon="💰")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ffcc; }
    .status-bar { padding: 5px 20px; background: #111; border-bottom: 1px solid #333; display: flex; justify-content: space-between; }
    .virus-overlay { background: red; color: white; padding: 20px; text-align: center; border-radius: 10px; border: 5px solid white; animation: blink 0.5s infinite; }
    @keyframes blink { 0% {opacity: 1;} 50% {opacity: 0.2;} 100% {opacity: 1;} }
</style>
""", unsafe_allow_html=True)

# --- 4. XỬ LÝ KỊCH BẢN VIRUS ---
if st.session_state.is_infected and st.session_state.page != "Store":
    st.markdown("<div class='virus-overlay'>", unsafe_allow_html=True)
    if st.session_state.virus_type == "Ransomware":
        st.error("🚨 HỆ THỐNG ĐÃ BỊ KHÓA BỞI HACKER 'CON HẸ'!")
        st.write("Hãy nạp 100 cái bắp cải để mở khóa dữ liệu bãi xe.")
    elif st.session_state.virus_type == "Adware":
        st.warning("⚠️ QUẢNG CÁO: Mua phân bón cây giá rẻ tại đây!!!")
        st.image("https://www.w3schools.com/w3images/hamburger.jpg", width=200) # Ảnh rác
    
    st.write("###")
    if st.button("DIỆT VIRUS NGAY (Vào Store)"):
        nav("Store")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. MÀN HÌNH CHÍNH & APPS ---
if st.session_state.page == "Lock":
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>🔒 TITAN OS</h1>", unsafe_allow_html=True)
    if st.button("UNLOCK (1234)"): nav("Desktop")

elif st.session_state.page == "Desktop":
    st.markdown(f"<div class='status-bar'><span>🛡️ Status: {'⚠️ INFECTED' if st.session_state.is_infected else '✅ CLEAN'}</span><span>{datetime.datetime.now().strftime('%H:%M')}</span></div>", unsafe_allow_html=True)
    st.title("🛡️ TITAN OMEGA DESKTOP")
    
    cols = st.columns(4)
    for idx, app in enumerate(st.session_state.installed_apps):
        with cols[idx % 4]:
            if st.button(f"📦 {app}"): nav(app)

elif st.session_state.page == "Store":
    st.header("🏪 Titan Store")
    st.write("Cài đặt phần mềm để bảo vệ hệ thống!")
    
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        st.write("🛡️ **Titan Antivirus Pro**")
        st.caption("Xóa bỏ mọi virus, ransomware và lỗi glitch.")
    with col_s2:
        if "Security" in st.session_state.installed_apps:
            st.success("Đã cài đặt")
            if st.button("QUÉT & DIỆT"):
                with st.spinner("Đang tiêu diệt Hacker..."):
                    time.sleep(2)
                    st.session_state.is_infected = False
                    st.session_state.virus_type = None
                    st.success("Hệ thống đã sạch!")
                    time.sleep(1)
                    st.rerun()
        else:
            if st.button("CÀI ĐẶT"):
                st.session_state.installed_apps.append("Security")
                st.toast("Đang tải bộ lọc bảo mật...")
                st.rerun()
    
    if st.button("🔙 VỀ DESKTOP"): nav("Desktop")

# --- CÁC APP KHÁC ---
elif st.session_state.page == "Settings":
    st.header("⚙️ Cài đặt")
    if st.button("Reset OS (Xóa sạch mọi thứ)"):
        st.session_state.installed_apps = ["Parking", "Botany", "Store", "Settings"]
        st.session_state.is_infected = False
        nav("Desktop")
    if st.button("🔙 BACK"): nav("Desktop")

else:
    st.header(f"🖥️ {st.session_state.page}")
    st.write("Ứng dụng đang chạy...")
    if st.button("🔙 EXIT"): nav("Desktop")
