import streamlit as st
import time
import datetime
import random

# --- 1. CORE OS INITIALIZATION ---
if 'page' not in st.session_state: st.session_state.page = "Lock"
if 'is_infected' not in st.session_state: st.session_state.is_infected = False
if 'installed_apps' not in st.session_state: 
    st.session_state.installed_apps = ["Parking", "Botany", "Store", "Settings", "Music", "Games"]
if 'gold' not in st.session_state: st.session_state.gold = 1000  # Tiền ảo để mua App/Game

# Danh mục App khổng lồ
APP_DATABASE = {
    "Parking": "🅿️", "Botany": "🌳", "Store": "🏪", "Settings": "⚙️", 
    "Music": "🎵", "Games": "🎮", "Finance": "💎", "Browser": "🌐",
    "Maps": "📍", "Clock": "⏰", "Weather": "☁️", "Health": "❤️",
    "Notes": "📝", "Mail": "✉️", "Chat": "💬", "Camera": "📷",
    "Calculator": "🔢", "News": "📰", "Stocks": "📈", "Files": "📁"
}

def nav(p):
    st.session_state.page = p
    st.rerun()

# --- 2. GIAO DIỆN INFINITY UI ---
st.set_page_config(page_title="Titan Infinity OS", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background: radial-gradient(circle, #0a0a0a 0%, #000 100%); color: #00f2ff; }}
    .status-bar {{ padding: 10px 25px; background: rgba(0,0,0,0.8); border-bottom: 1px solid #00f2ff44; display: flex; justify-content: space-between; position: fixed; top: 0; left:0; width: 100%; z-index: 1000; }}
    .app-icon {{ 
        transition: 0.3s; padding: 20px; border-radius: 20px; background: #111; 
        border: 1px solid #222; text-align: center; cursor: pointer;
    }}
    .app-icon:hover {{ border-color: #00f2ff; box-shadow: 0 0 20px #00f2ff44; transform: translateY(-5px); }}
    .widget {{ background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border-left: 5px solid #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 3. STATUS BAR & WIDGETS ---
st.markdown(f"""<div class='status-bar'>
    <span>🛰️ CLUSTER-OS | 💰 {st.session_state.gold} Gold</span>
    <span>🔋 99% | {datetime.datetime.now().strftime('%H:%M')}</span>
</div>""", unsafe_allow_html=True)
st.write("###")

# --- 4. NAVIGATION LOGIC ---

# MÀN HÌNH KHÓA
if st.session_state.page == "Lock":
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>🔒 TITAN INFINITY</h1>", unsafe_allow_html=True)
    if st.button("NHẬP VÂN TAY ĐỂ MỞ KHÓA"): nav("Desktop")

# MÀN HÌNH CHÍNH (DESKTOP)
elif st.session_state.page == "Desktop":
    col_w1, col_w2 = st.columns([2, 1])
    with col_w1:
        st.title("🌌 Welcome, Boss!")
        # Grid Apps
        cols = st.columns(4)
        for idx, app in enumerate(st.session_state.installed_apps):
            icon = APP_DATABASE.get(app, "📦")
            with cols[idx % 4]:
                if st.button(f"{icon}\n{app}"): nav(app)
    
    with col_w2:
        st.markdown("<div class='widget'>", unsafe_allow_html=True)
        st.subheader("📊 Widget")
        st.write(f"Cây của bạn: **Đang khát nước!**")
        st.write(f"Bãi xe: **5 xe đang đỗ**")
        st.progress(65)
        st.markdown("</div>", unsafe_allow_html=True)

# APP: GAMES (NEW!)
elif st.session_state.page == "Games":
    st.button("🔙 EXIT GAME", on_click=lambda: nav("Desktop"))
    st.header("🎮 Mini Game: Hứng Cây")
    st.write("Nhấn nút để thu hoạch cây và kiếm Gold!")
    if st.button("🌾 THU HOẠCH!"):
        gain = random.randint(10, 50)
        st.session_state.gold += gain
        st.success(f"Bạn nhận được {gain} Gold!")
        st.balloons()

# APP: MUSIC (NEW!)
elif st.session_state.page == "Music":
    st.button("🔙 EXIT MUSIC", on_click=lambda: nav("Desktop"))
    st.header("🎵 Titan Spotify")
    song = st.selectbox("Chọn bài hát:", ["Lofi cho bãi xe", "Sơn Tùng MTP - Trồng Hẹ", "Tiếng mưa tưới cây"])
    if st.button("PLAY"):
        st.write(f"🎶 Đang phát: **{song}**")
        st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk") # Link nhạc lofi mẫu

# APP: STORE (NÂNG CẤP)
elif st.session_state.page == "Store":
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header("🏪 Titan Store")
    for app, icon in APP_DATABASE.items():
        if app not in st.session_state.installed_apps:
            c1, c2 = st.columns([4, 1])
            with c1: st.write(f"{icon} **{app}**")
            with c2: 
                if st.button(f"Mua (50 Gold)", key=app):
                    if st.session_state.gold >= 50:
                        st.session_state.gold -= 50
                        st.session_state.installed_apps.append(app)
                        st.rerun()
                    else: st.error("Hết tiền!")

# APP: SETTINGS (CHỐNG VIRUS)
elif st.session_state.page == "Settings":
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header("⚙️ Settings")
    if st.button("Diệt Virus & Làm sạch RAM"):
        with st.status("Cleaning..."):
            time.sleep(2)
            st.session_state.is_infected = False
            st.success("Hệ thống đã mượt!")

# CÁC APP KHÁC
else:
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header(f"🖥️ {st.session_state.page}")
    st.write("Tính năng đang được cập nhật từ Cloud...")
