import streamlit as st
import time
import datetime

# --- 1. KHỞI TẠO HỆ THỐNG ---
if 'installed_apps' not in st.session_state:
    st.session_state.installed_apps = {"Parking": "v1.0", "Botany": "v1.0", "Settings": "v1.0", "Store": "v1.0"}
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'theme_color' not in st.session_state: st.session_state.theme_color = "#00f2ff"

# Danh sách 30 App với phiên bản mới nhất
APP_DATABASE = {
    "Parking": {"icon": "🅿️", "ver": "v2.0", "desc": "Quản lý xe chuyên nghiệp bằng AI."},
    "Botany": {"icon": "🌳", "ver": "v2.1", "desc": "Theo dõi sức khỏe cây cảnh thực tế."},
    "Finance": {"icon": "💎", "ver": "v1.5", "desc": "Biểu đồ thu nhập và chi tiêu."},
    "Browser": {"icon": "🌐", "ver": "v3.0", "desc": "Duyệt Web an toàn qua Titan-Net."},
    "Games": {"icon": "🎮", "ver": "v1.2", "desc": "Kho trò chơi giải trí nhẹ nhàng."},
    "AI-Chat": {"icon": "🤖", "ver": "v4.0", "desc": "Trợ lý ảo hỗ trợ công việc."},
    "Maps": {"icon": "📍", "ver": "v1.1", "desc": "Định vị bãi xe của Boss."},
    "Music": {"icon": "🎵", "ver": "v2.0", "desc": "Phát nhạc thư giãn khi làm việc."},
    "Weather": {"icon": "☁️", "ver": "v1.0", "desc": "Dự báo thời tiết cho cây cảnh."},
    "Settings": {"icon": "⚙️", "ver": "v1.0", "desc": "Cài đặt và tính năng ẩn."}
}

# --- 2. GIAO DIỆN NÂNG CẤP (GLASSMORPHISM) ---
st.set_page_config(page_title="Titan Galaxy V27", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: white; }}
    /* Thẻ App trong Store */
    .app-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {st.session_state.theme_color}33;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 10px;
        transition: 0.3s;
    }}
    .app-card:hover {{ border-color: {st.session_state.theme_color}; background: rgba(255, 255, 255, 0.1); }}
    .status-bar {{ text-align: right; color: {st.session_state.theme_color}; padding: 10px; font-family: monospace; }}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ĐIỀU HƯỚNG (SỬA LỖI CALLBACK) ---
# Không dùng st.rerun() trong callback nữa, thay bằng xử lý tại phần hiển thị

# MÀN HÌNH CHÍNH (DESKTOP)
if st.session_state.page == "Desktop":
    st.markdown(f"<div class='status-bar'>📶 GALAXY-NET | 🔋 98% | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)
    st.title("🛡️ TITAN OMEGA OS")
    
    cols = st.columns(5)
    # Duyệt qua các app đã cài
    for idx, (app_name, version) in enumerate(st.session_state.installed_apps.items()):
        icon = APP_DATABASE.get(app_name, {"icon": "📦"})["icon"]
        with cols[idx % 5]:
            if st.button(f"{icon}\n{app_name}\n({version})", key=f"desktop_{app_name}"):
                st.session_state.page = app_name
                st.rerun()
    
    st.divider()
    if st.button("🏪 TRUY CẬP TITAN STORE"):
        st.session_state.page = "Store"
        st.rerun()

# MÀN HÌNH CỬA HÀNG (STORE 2.0)
elif st.session_state.page == "Store":
    st.button("🔙 THOÁT CỬA HÀNG") # Sẽ quay lại desktop ở cuối loop
    st.title("🏪 Titan Store - Galaxy Market")
    
    for name, info in APP_DATABASE.items():
        with st.container():
            st.markdown(f"""<div class='app-card'>""", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 4, 2])
            with c1:
                st.markdown(f"<h1>{info['icon']}</h1>", unsafe_allow_html=True)
            with c2:
                st.subheader(name)
                st.write(info['desc'])
                st.caption(f"Phiên bản mới nhất: {info['ver']}")
            with c3:
                # Logic Cài đặt / Cập nhật / Mở
                if name not in st.session_state.installed_apps:
                    if st.button(f"CÀI ĐẶT", key=f"ins_{name}"):
                        st.session_state.installed_apps[name] = info['ver']
                        st.toast(f"Đã cài xong {name}!")
                        st.rerun()
                else:
                    current_v = st.session_state.installed_apps[name]
                    if current_v != info['ver']:
                        if st.button(f"🔥 CẬP NHẬT", key=f"upd_{name}"):
                            st.session_state.installed_apps[name] = info['ver']
                            st.toast(f"Đã nâng cấp {name} lên {info['ver']}")
                            st.rerun()
                    else:
                        st.success("✅ Đã cài")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Nút thoát thủ công nếu cần
    if st.button("QUAY LẠI MÀN HÌNH CHÍNH"):
        st.session_state.page = "Desktop"
        st.rerun()

# APP: TRÌNH DUYỆT (BROWSER)
elif st.session_state.page == "Browser":
    st.header("🌐 Titan Browser")
    q = st.text_input("Tìm kiếm Google...")
    if q: st.link_button("Xem kết quả", f"https://www.google.com/search?q={q}")
    if st.button("BACK"):
        st.session_state.page = "Desktop"
        st.rerun()

# CÁC MÀN HÌNH KHÁC (GIẢ LẬP)
else:
    st.header(f"🖥️ {st.session_state.page}")
    st.info(f"Phiên bản {st.session_state.installed_apps.get(st.session_state.page, 'v1.0')} đang chạy ổn định.")
    if st.button("🔙 VỀ MÀN HÌNH CHÍNH"):
        st.session_state.page = "Desktop"
        st.rerun()
